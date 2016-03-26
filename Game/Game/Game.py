import pygame, os, math, random
from Level import Level
from Player import Player
from Sprite import Sprite
from Monster import Monster
from Menu import Menu
from pygame.locals import *

def key_event_handler(pressed_key):
	#when a key is pressed, do the thing.
	#returns true or false depending on if we should end the game.
	if (pressed_key == K_ESCAPE):
		return True
	elif (pressed_key == K_UP):
		if (level.is_walkable(player.x, player.y-1)):
			player_move(0, -1)
		else:
			print "OUCH!"
	elif (pressed_key == K_DOWN):
		if (level.is_walkable(player.x, player.y+1)):
			player_move(0, 1)
		else:
			print "OUCH!"
	elif (pressed_key == K_RIGHT):
		if (level.is_walkable(player.x+1,player.y)):
			player_move(1, 0)
		else:
			print "OUCH!"
	elif (pressed_key == K_LEFT):
		if (level.is_walkable(player.x-1, player.y)):
			player_move(-1, 0)
		else:
			print "OUCH!"
	elif (pressed_key == K_SPACE):
		menu.run_menu()
		background = level.render()
		restore_back()
	
	return False

def restore_back():
	screen = pygame.display.set_mode(background.get_size())
	print "screen"
	screen.blit(background,(0, 0))
	print "blit"
	pygame.display.flip()
	print "flip"

def player_move(dx, dy):
	player.x += dx
	player.y += dy
	player_sprite.move(dx * MAP_TILE_WIDTH, dy * MAP_TILE_HEIGHT)
	if (level.check_door(player.x, player.y)):
		change_level()

def end_step():
	global triggered_events
	#moves all the monsters
	for monster in mon.monster_instance:
		move_monster(monster)
		#print "The monster has moved!"
	#handle the triggered events from the main game loop
	triggered_events.update(add_events())
	if ("new_monster" in triggered_events):
		n = triggered_events.pop("new_monster", None)
		x = triggered_events.pop("x", None)
		y = triggered_events.pop("y", None)
		new_mon = mon.load_monster(n, x, y)
		moving_sprites.add(new_mon["sprite"])
		moving_sprites.switch_layer(0,1)
	collision_check(player.x, player.y)

def move_monster(mons):
	info = {"level":mons["stats"]["level"], "x":mons["x"], "y":mons["y"], "p_level":player.player["stats"]["level"], "p_x":player.x, "p_y":player.y, "redo":0}
	temp_x, temp_y = mon.move(info)
	while not level.is_walkable(temp_x, temp_y):
		info["redo"] += 1
		temp_x, temp_y = mon.move(info)
		for other_mons in mon.monster_instance:
			if (other_mons == mons):
				continue
			elif (other_mons['x'], other_mons['y'] == temp_x, temp_y):
				temp_x, temp_y = mon.move(info)
		#print temp_x, temp_y
	mons["sprite"].move((temp_x - mons["x"]) * MAP_TILE_WIDTH, (temp_y - mons["y"]) * MAP_TILE_HEIGHT)
	mons["x"], mons["y"] = (temp_x, temp_y)

def add_events():
	#probabilistically does stuff. Fun.
	#adds monsters, possibly changes terrain, etc.
	place_monster = 25
	MAX = 100
	trig = {}
	test_val = random.randint(0, MAX)
	if (test_val < place_monster):
		#print "placing monster..."
		x, y = 0, 0
		while is_occupied(x, y):
			x, y = random.randint(0, level.width), random.randint(0, level.height)
		trig = {"new_monster":mon.generate_monster(player.player['stats']['level']), "x":x, "y":y}
	return trig

def is_occupied(x, y):
	if (not level.is_walkable(x, y)):
		return True
	for mons in mon.monster_instance:
		if (mons['x'] == x and mons['y'] == y):
			return True
	return False

def change_level():
	global background
	global screen
	mon.remove_all_monsters()
	temp_sprite = player_sprite
	#sprites.
	new_dict = level.get_map_and_coords(player.x, player.y)
	level.load_map(new_dict["map_name"])
	x_sprite = new_dict['x'] - player.x
	y_sprite = new_dict['y'] - player.y
	player_move(x_sprite, y_sprite)
	background = level.render()
	restore_back()

def collision_check(x, y):
	for monster in mon.monster_instance:
		if monster['x'] == x and monster['y'] == y:
			print "You collided with " + monster['name']
#------------------------------------------------------------------
#----------------MAIN GAME CODE------------------------------------
#------------------------------------------------------------------
triggered_events = {}

if __name__ == "__main__":
	#Init pygame and create the blank screen
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	screen.fill((0, 0, 0))

	#Important global values and initializing of sprites, background, map, player
	MAP_TILE_WIDTH = 32
	MAP_TILE_HEIGHT = 32
	game_over = False
	level = Level()
	player = Player()
	mon = Monster()
	level.load_map('levels/test.map')
	clock = pygame.time.Clock()
	background = level.render()
	screen.blit(background, (0, 0))
	menu = Menu(player, {'width':background.get_width(),'height':background.get_height(),'sidebar_width':32})
	sprites = pygame.sprite.RenderUpdates()
	moving_sprites = pygame.sprite.LayeredUpdates()
	player_sprite = Sprite((player.x*MAP_TILE_WIDTH, player.y*MAP_TILE_HEIGHT), player.icon)
	moving_sprites.add(player_sprite)
	moving_sprites.switch_layer(0, 1)
	pygame.display.flip()

	while not game_over:
		#update the screen to include any changes we made by moving, etc.
		sprites.clear(screen, background)
		moving_sprites.clear(screen, background)
		#sprites.update()
		dirty = sprites.draw(screen)
		moving_dirty = moving_sprites.draw(screen)
		pygame.display.update(dirty)
		pygame.display.update(moving_dirty)
		#However many frames per second.
		clock.tick(16)
		#handle any events that may occur.
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				game_over = True
			elif event.type == pygame.locals.KEYDOWN:
				game_over = key_event_handler(event.key)
				#run_AI()
				end_step()

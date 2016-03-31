import pygame, os, math, random
from Level import Level
from Game_Structs import Player, Monster
from Sprite import Sprite
from Manager import Manager
from Menu import Menu
from pygame.locals import *

def key_event_handler(pressed_key):
	#when a key is pressed, do the thing.
	#returns true or false depending on if we should end the game.
	if (pressed_key == K_ESCAPE):
		return True
	elif (pressed_key == K_UP):
		if (level.is_walkable(player.x, player.y-1)):
			player.move(0, -1)
		else:
			print "OUCH!"
	elif (pressed_key == K_DOWN):
		if (level.is_walkable(player.x, player.y+1)):
			player.move(0, 1)
		else:
			print "OUCH!"
	elif (pressed_key == K_RIGHT):
		if (level.is_walkable(player.x+1,player.y)):
			player.move(1, 0)
		else:
			print "OUCH!"
	elif (pressed_key == K_LEFT):
		if (level.is_walkable(player.x-1, player.y)):
			player.move(-1, 0)
		else:
			print "OUCH!"
	elif (pressed_key == K_SPACE):
		#runs the menu
		menu.run_menu()
		background = level.render()
		restore_back()
	
	return False

def restore_back():
	global screen
	global background
	screen.fill((0, 0, 0))
	#print "screen"
	screen.blit(background,(0, 0))
	#print "blit"
	pygame.display.flip()
	#print "flip"

def player_move(dx, dy):
	#inputs are the amount you want it to move, not the coordinates.
	player.x += dx
	player.y += dy
	player_sprite.move(dx * MAP_TILE_WIDTH, dy * MAP_TILE_HEIGHT)
	if (level.check_door(player.x, player.y)):
		change_level()

def end_step():
	global triggered_events
	#moves all the monsters
	for mon in monsters:
		move_monster(mon)
	#handle the triggered events from the main game loop
	triggered_events.update(add_events())
	if ("new_monster" in triggered_events):
		new_mon = triggered_events.pop("new_monster", None)
		new_mon.set_pos((triggered_events.pop("x", None), triggered_events.pop("y", None)))
		monsters.append(new_mon)
		moving_sprites.add(new_mon.sprite)
		moving_sprites.switch_layer(0,1)
	collision_check(player.x, player.y)

def move_monster(mons):
	#generate a grid around the monster, then value each square.
	#move to the best square afterwards.
	x, y = 0, 0
	top_val = []
	for grid_y in range(mons.y-1, mons.y+1):
		for grid_x in range(mons.x-1, mons.x+1):
			val = 0
			if level.is_walkable(grid_x, grid_y):
				val += 100
			else:
				val -= 1000
			if is_occupied(grid_x, grid_y) and (mons.x != grid_x and mons.y != grid_y):
				val -= 1000
			if player.stats['level'] >= mons.difficulty:
				val += abs(player.x - grid_x)
				val += abs(player.y - grid_y)
			else:
				val -= abs(player.x - grid_x)
				val -= abs(player.y - grid_y)
			if val > 0:
				for q in range(1, val):
					top_val.append((grid_x, grid_y))
	pos = random.choice(top_val)
	mons.move(pos[0] - mons.x, pos[1] - mons.y)

def add_events():
	#probabilistically does stuff. Fun.
	#adds monsters, possibly changes terrain, etc.
	place_monster = 3
	MAX = 100
	trig = {}
	test_val = random.randint(0, MAX)
	if (test_val < place_monster):
		x, y = 0, 0
		while is_occupied(x, y):
			x, y = random.randint(0, level.width), random.randint(0, level.height)
		trig = {"new_monster":manager.generate_monster(player.stats['level']), "x":x, "y":y}
	return trig

def is_occupied(x, y):
	if (not level.is_walkable(x, y)):
		return True
	for mons in monsters:
		if (mons.x == x and mons.y == y):
			return True
	return False

def change_level():
	global background
	global screen
	global moving_sprites
	monsters.empty()
	temp_sprite = player.sprite
	moving_sprites.empty()
	moving_sprites.add(temp_sprite)
	new_dict = level.get_map_and_coords(player.x, player.y)
	level.load_map(new_dict["map_name"])
	x = new_dict['x'] - player.x
	y = new_dict['y'] - player.y
	player.move(x, y)
	background = level.render()
	restore_back()

def collision_check(x, y):
	for m in monsters:
		if m.x == x and m.y == y:
			print "You collided with " + m.name
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
	manager = Manager()
	player = manager.load_player('players/base.plyr')
	monsters = []
	level.load_map('levels/test.map')
	clock = pygame.time.Clock()
	background = level.render()
	screen.blit(background, (0, 0))
	#menu = Menu(player, {'width':500,'height':500,'sidebar_width':32, 'button_height':24})
	moving_sprites = pygame.sprite.LayeredUpdates()
	#player_sprite = Sprite((player.x*MAP_TILE_WIDTH, player.y*MAP_TILE_HEIGHT), player.icon, "player")
	moving_sprites.add(player.sprite)
	moving_sprites.switch_layer(0, 1)
	pygame.display.flip()

	while not game_over:
		#update the screen to include any changes we made by moving, etc.
		moving_sprites.clear(screen, background)
		moving_dirty = moving_sprites.draw(screen)
		pygame.display.update(moving_dirty)
		#However many frames per second.
		clock.tick(16)
		#handle any events that may occur.
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				game_over = True
			elif event.type == pygame.locals.KEYDOWN:
				print event.key
				game_over = key_event_handler(event.key)
				#run_AI()
				end_step()

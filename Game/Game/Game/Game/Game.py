import pygame, os, math, random
from Manager import FileManager, TileManager, ScreenManager
from Menu import Menu
from pygame.locals import *

def key_event_handler(pressed_key):
	#when a key is pressed, do the thing.
	#returns true or false depending on if we should end the game.
	if (pressed_key == K_ESCAPE):
		return True
	elif (pressed_key == K_UP):
		if (screen.level.is_walkable(player.x, player.y-1)):
			player_move(0, -1)
		else:
			print "OUCH!"
	elif (pressed_key == K_DOWN):
		if (screen.level.is_walkable(player.x, player.y+1)):
			player_move(0, 1)
		else:
			print "OUCH!"
	elif (pressed_key == K_RIGHT):
		if (screen.level.is_walkable(player.x+1,player.y)):
			player_move(1, 0)
		else:
			print "OUCH!"
	elif (pressed_key == K_LEFT):
		if (screen.level.is_walkable(player.x-1, player.y)):
			player_move(-1, 0)
		else:
			print "OUCH!"
	elif (pressed_key == K_SPACE):
		#runs the menu
		menu.run_menu()
	
	return False


def player_move(dx, dy):
	player.move(dx, dy)
	#inputs are the amount you want it to move, not the coordinates.
	if (screen.check_door(player.x, player.y)):
		monsters[:] = []
		screen.remove_sprite_layer(1)
		print monsters
		new_pos = screen.change_map(player.x, player.y)
		player.move(new_pos[0] - player.x, new_pos[1] - player.y)

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
		screen.add_sprite(new_mon.sprite, 1)
	collision_check(player.x, player.y)

def move_monster(mons):
	#generate a grid around the monster, then value each square.
	#move to the best square afterwards.
	x, y = mons.x-1, mons.y-1
	top_val = []
	for grid_y in range(3):
		x = mons.x-1
		top_val.append([])
		for grid_x in range(3):
			val = 0
			#if screen.level.is_walkable(grid_x, grid_y):
			#	val += 10
			#else:
			#	val -= 1000
			if is_occupied(x, y):
				val -= 1000
			else:
				val += 10
			if player.stats['level'] >= mons.difficulty:
				val += abs(player.x - grid_x)
				val += abs(player.y - grid_y)
			else:
				val -= abs(player.x - grid_x)
				val -= abs(player.y - grid_y)
			if val > 0:
				#print (x, y)
				#print "walkable"
				#print val
				for q in range(1, val):
					top_val[grid_y].append((x, y))
			else:
				#print (x, y)
				#print "not walkable"
				top_val[grid_y].append((mons.x, mons.y))
			#print top_val[grid_y]
			x += 1
		#print top_val[grid_y]
		y += 1
	#print top_val
	final_grid = []
	for coord in top_val:
		final_grid += coord
	#print final_grid
	pos = random.choice(final_grid)
	print "pos is "
	print pos
	print "for " + mons.name
	mons.move(pos[0] - mons.x, pos[1] - mons.y)

def add_events():
	#probabilistically does stuff. Fun.
	#adds monsters, possibly changes terrain, etc.
	place_monster = 20
	MAX = 100
	trig = {}
	test_val = random.randint(0, MAX)
	if (test_val < place_monster):
		x, y = 0, 0
		while is_occupied(x, y):
			x, y = random.randint(0, screen.level.width), random.randint(0, screen.level.height)
		trig = {"new_monster":manager.generate_monster(player.stats['level']), "x":x, "y":y}
	return trig

def is_occupied(x, y):
	if (not screen.level.is_walkable(x, y)):
		return True
	for mons in monsters:
		if (mons.x == x and mons.y == y):
			return True
	return False


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

	#Important global values and initializing of sprites, background, map, player
	game_over = False
	screen = ScreenManager('levels/test.map')
	manager = FileManager()
	player = manager.load_player('players/base.plyr')
	monsters = []
	clock = pygame.time.Clock()
	screen.add_sprite(player.sprite, {'layer':0})

	while not game_over:
		#update the screen to include any changes we made by moving, etc.
		screen.update()
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

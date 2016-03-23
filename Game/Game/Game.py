import pygame, os, math
from Level import Level
from Player import Player
from Sprite import Sprite
from Monster import Monster
from pygame.locals import *

def key_event_handler(pressed_key):
	#when a key is pressed, do the thing.
	#returns true or false depending on if we should end the game.
	if (pressed_key == K_ESCAPE):
		return True
	elif (pressed_key == K_UP):
		if (level.is_walkable(player.x, player.y-1)):
			player.y -= 1
			player_sprite.move(0, -MAP_TILE_HEIGHT)
		else:
			print "OUCH!"
	elif (pressed_key == K_DOWN):
		if (level.is_walkable(player.x, player.y+1)):
			player.y += 1
			player_sprite.move(0, MAP_TILE_HEIGHT)
		else:
			print "OUCH!"
	elif (pressed_key == K_RIGHT):
		if (level.is_walkable(player.x+1,player.y)):
			player.x += 1
			player_sprite.move(MAP_TILE_WIDTH, 0)
		else:
			print "OUCH!"
	elif (pressed_key == K_LEFT):
		if (level.is_walkable(player.x-1, player.y)):
			player.x -= 1
			player_sprite.move(-MAP_TILE_WIDTH, 0)
		else:
			print "OUCH!"
	return False

def end_step():
	#moves all the monsters
	for monster in mon.monster_instance:
		info = {"level":monster["level"], "x":monster["x"], "y":monster["y"], "p_level":player.level, "map":level}
		monster["x"], monster["y"] = mon.move(info)
		monster["sprite"].move(math.copysign(1, (monster["x"] - info["x"])) * MAP_TILE_WIDTH, math.copysign(1, (monster["y"] - info["y"])) * MAP_TILE_HEIGHT)
	#handle the triggered events from the main game loop
	if ("new_monster" in triggered_events):
		n = triggered_events.pop("new_monster", None)
		x = triggered_events.pop("x", None)
		y = triggered_events.pop("y", None)
		new_mon = mon.load_monster(n, x, y)
		sprites.add(new_mon["sprite"])


#------------------------------------------------------------------
#----------------MAIN GAME CODE------------------------------------
#------------------------------------------------------------------
if __name__ == "__main__":
	#Init pygame and create the blank screen
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	screen.fill((0, 0, 0))

	#Important global values and initializing of sprites, background, map, player
	MAP_TILE_WIDTH = 32
	MAP_TILE_HEIGHT = 32
	game_over = False
	triggered_events = {"new_monster":"troglodyte", "x":3, "y":3}
	level = Level()
	player = Player()
	mon = Monster()
	level.load_map('levels/test.map')
	clock = pygame.time.Clock()
	background = level.render()
	screen.blit(background, (0, 0))
	sprites = pygame.sprite.RenderUpdates()
	player_sprite = Sprite((player.x*MAP_TILE_WIDTH, player.y*MAP_TILE_HEIGHT), player.icon)
	sprites.add(player_sprite)
	pygame.display.flip()

	while not game_over:
		#update the screen to include any changes we made by moving, etc.
		sprites.clear(screen, background)
		dirty = sprites.draw(screen)
		pygame.display.update(dirty)
		#15 frames per second.
		clock.tick(15)
		#handle any events that may occur.
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				game_over = True
			elif event.type == pygame.locals.KEYDOWN:
				game_over = key_event_handler(event.key)
				#run_AI()
			end_step()

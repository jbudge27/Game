import ConfigParser
import random
import math
from Sprite import Sprite
import pygame
from pygame.locals import *

class Monster(object):
	def __init__(self):
		#load sprites from sheet
		width = 32
		height = 32
		image = pygame.image.load("tiles/monsters.bmp").convert()
		image_width, image_height = image.get_size()
		tile_table = []
		for tile_x in range(0, image_width/width):
			line = []
			tile_table.append(line)
			for tile_y in range(0, image_height/height):
				rect = (tile_x*width, tile_y*height, width, height)
				line.append(image.subsurface(rect))
		self.sprites = tile_table
		#this is the instances of monsters in the level
		self.monster_instance = []
		#master list of possible monsters
		self.master_list = self.load_sheet()

	def load_monster(self, name, x, y):
		parser = ConfigParser.ConfigParser()
		parser.read("monsters/" + name + ".mon")
		new_mon = {}
		new_mon['name'] = parser.get("misc", "name")
		pos = parser.get("misc", "sprite").split(',')
		new_mon['sprite'] = Sprite((x*32, y*32), self.sprites[int(pos[0])][int(pos[1])])
		new_mon['x'] = x
		new_mon['y'] = y
		for section in parser.sections():
			if section == "misc":
				{}
			else:
				desc = dict(parser.items(section))
				new_mon[section] = desc
		for i in new_mon['stats']:
			new_mon['stats'][i] = int(new_mon['stats'][i])
		self.monster_instance.append(new_mon)
		return new_mon

	def load_sheet(self):
		#loads the master list.
		line = {}
		parser = ConfigParser.ConfigParser()
		parser.read("monsters/master.mon")
		for section in parser.sections():
			desc = dict(parser.items(section))
			line[section] = desc['names'].split('\n')
		print line
		return line

	def load_sprites(filename):
		image = pygame.image.load(filename).convert()
		image_width, image_height = image.get_size()
		tile_table = []
		for tile_x in range(0, image_width/width):
			line = []
			tile_table.append(line)
			for tile_y in range(0, image_height/height):
				rect = (tile_x*width, tile_y*height, width, height)
				line.append(image.subsurface(rect))
		return tile_table

	def move(self, info):
		move_x = 0
		move_y = 0
		if (info["level"] >= info["p_level"]):
			move_x = math.copysign(1, (info["p_x"] - info["x"]))
			move_y = math.copysign(1, (info["y"] - info["p_y"]))
		else:
			move_x = math.copysign(1, (info["x"] - info["p_x"]))
			move_y = math.copysign(1, (info["p_y"] - info["y"]))
		if (info['p_x'] == info['x']):
			move_x = 0
		if (info['p_y'] == info['y']):
			move_y = 0
		if (info['redo'] > 0):
			move_x = random.randint(-1, 2)
			move_y = random.randint(-1, 2)
		new_x = move_x + info["x"] 
		new_y = move_y + info["y"]
		#print str(new_x) + " from " + str(info['x'])
		#print str(new_y) + " from " + str(info['y'])
		return (int(new_x), int(new_y)) 

	def remove_all_monsters(self):
		self.monster_instance = []

	def generate_monster(self, p_level):
		available_monsters = {}
		for key in self.master_list:
			if int(key) > p_level:
				continue
			else:
				available_monsters[key] = self.master_list[key]
		print available_monsters
		sel = random.randint(0, (len(available_monsters) - 1))
		mon_sel = random.choice(available_monsters[str(sel)])
		#returns name of monster
		return mon_sel

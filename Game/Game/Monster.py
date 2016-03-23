import ConfigParser
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
			line[section] = desc
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
		while ~info["map"].is_walkable(new_x, new_y):
			new_x = math.copysign(1, (info["level"] - info['p_level'])) + info["x"] 
			new_y = math.copysign(1, (info["level"] - info['p_level'])) + info["y"]
		return (new_x, new_y) 

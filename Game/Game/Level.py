import ConfigParser
import pygame
from pygame.locals import *

class Level(object):
	def load_map(self, filename="levels/test.map"):
		self.map = []
		self.key = {}
		parser = ConfigParser.ConfigParser()
		parser.read(filename)
		self.map = parser.get("level", "map").split("\n")
		for section in parser.sections():
			if len(section) == 1:
				desc = dict(parser.items(section))
				self.key[section] = desc
		self.width = len(self.map[0])
		self.height = len(self.map)

	def load_tile(self, x, y):
		#print self.get_tile(x, y).get("tile")
		image = pygame.image.load(self.get_tile(x, y).get("tile"))
		#width, height = image.get_size()
		return image

	def get_tile(self, x, y):
		try:
			char = self.map[y][x]
		except IndexError:
			return {}
		try:
			return self.key[char]
		except KeyError:
			return {}

	def is_walkable(self, x, y):
		val = self.get_tile(x, y).get("walkable")
		return val in (True, 1, 'true', 'yes', "True", 'Yes', '1', 'on', 'On')

	def render(self):
		MAP_TILE_WIDTH = 32
		MAP_TILE_HEIGHT = 32
		#print self.width
		#print self.height
		image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
		overlays = {}
		for map_y, line in enumerate(self.map):
			for map_x, c in enumerate(line):
				tile_image = self.load_tile(map_x, map_y)
				image.blit(tile_image, (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
		return image


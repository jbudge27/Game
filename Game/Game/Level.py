import ConfigParser
import pygame
from TileManager import TileManager
from pygame.locals import *

class Level(object):
	def load_map(self, filename="levels/test.map"):
		self.map = []
		self.key = {}
		t = TileManager(32, 32)
		self.tiles = t["tiles/general.bmp"]
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
		pos = self.get_tile(x, y).get("tile").split(',')
		image = self.tiles[int(pos[0])][int(pos[1])]
		#image = pygame.image.load(self.tiles[int(pos[0])][int(pos[1])])
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
		#print "walkable is " + str(val)
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

	def get_map_and_coords(self, x, y):
		coords = self.get_tile(x, y).get("link_coordinates").split(",")
		map_name = self.get_tile(x,y).get("link")
		return {"map_name":map_name, "x":int(coords[0]), "y":int(coords[1])}

	def check_door(self, x, y):
		if self.get_tile(x, y).get("name") == "door":
			return True
		else:
			return False

import pygame
from pygame.locals import *

class TileManager:
	def __init__(self, width=32, height=32):
		self.width = width
		self.height = height
		self.cache = {}

	def __getitem__(self, filename):
		key = (filename, self.width, self.height)
		try:
			return self.cache[key]
		except KeyError:
			tile_table = self.load_tile_table(filename, self.width, self.height)
			self.cache[key] = tile_table
			return tile_table

	def load_tile_table(self, filename, width, height):
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

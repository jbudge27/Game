import ConfigParser

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
		return pygame.image.load(self.get_tile(x, y).get("tile"))

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
		return self.get_tile(x, y).get("walkable")

	def render(self):
		image = pygame.Surface((self.width*MAP_TILE_WIDTH, self.height*MAP_TILE_HEIGHT))
		overlays = {}
		for map_y, line in enumerate(self.map):
			for map_x, c in enumerate(line):
				tile_image = load_tile(c, line)
				image.blit(tile_image, map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT)
		return image


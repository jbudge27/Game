import pygame, random, copy
from pygame.locals import *
import ConfigParser
from Game_Structs import Player, Monster, Item, Level

class FileManager:
	def __init__(self):
		table = TileManager(32, 32)
		self.gen_tiles = table['tiles/general.bmp']
		self.mon_tiles = table['tiles/monsters.bmp']
		master_list = self.load_master()
		self.monster_list = master_list['monsters']
		self.monsters = []
		self.items = []
		for mon in self.monster_list:
			self.monsters.append(self.load_monster(mon, 0, 0))
		self.item_list = master_list['items']
		#for item in self.item_list:
		#	self.items.append(self.load_item())

	def load_player(self, filename):
		parser = ConfigParser.ConfigParser()
		parser.read(filename)
		line = {}
		#tiles = TileManager(32, 32)
		#images = tiles['tiles/general.bmp']
		image = self.gen_tiles[9][2]
		name = parser.get("misc", "name")
		x = int(parser.get("misc", "x"))
		y = int(parser.get("misc", "y"))
		#load all the data from the file into a workable array of dicts.
		for section in parser.sections():
			desc = dict(parser.items(section))
			line[section] = desc
		for i in line['stats']:
			line['stats'][i] = int(line['stats'][i])
		player = Player(name, x, y, image, line['stats'], {}, {}, {})
		#invent = line['items']['inventory'].split('\n')
		#for y in invent:
	#		player.add_item(self.load_item(y))
	#	for y in line['equip']:
	#		player.equip(self.load_item(y))
	#	for y in line['skills']:
	#		player.add_skill(self.load_skill(y))
		return player

	def load_monster(self, name, x, y):
		parser = ConfigParser.ConfigParser()
		parser.read("monsters/" + name + ".mon")
		name = parser.get("misc", "name")
		pos = parser.get("misc", "sprite").split(',')
		image = self.mon_tiles[int(pos[0])][int(pos[1])]
		line = {}
		for section in parser.sections():
			if section == "misc":
				{}
			else:
				desc = dict(parser.items(section))
				line[section] = desc
		for i in line['stats']:
			line['stats'][i] = int(line['stats'][i])
		other = {'exp':int(parser.get("misc", "exp_given")), 'difficulty':int(parser.get("misc", "difficulty"))}
		return Monster(name, x, y, image, line['stats'], other)

	def generate_monster(self, p_level):
		ch = []
		for mon in self.monsters:
			if p_level >= mon.difficulty:
				ch.append(mon)
		return copy.copy(random.choice(ch))

	def load_master(self):
		#loads the master list...of everything items/monster wise
		line = {}
		parser = ConfigParser.ConfigParser()
		parser.read("monsters/master.mon")
		for section in parser.sections():
			desc = dict(parser.items(section))
			line[section] = desc['names'].split('\n')
		return line

	def load_map(self, filename="levels/test.map"):
		map = []
		key = {}
		t = TileManager(32, 32)
		tiles = t["tiles/general.bmp"]
		parser = ConfigParser.ConfigParser()
		parser.read(filename)
		map = parser.get("level", "map").split("\n")
		for section in parser.sections():
			if len(section) == 1:
				desc = dict(parser.items(section))
				key[section] = desc
		return Level(map, key, tiles)

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

class ScreenManager:
	def __init__(self, map_name):
		self.screen = pygame.display.set_mode((500, 500))
		self.files = FileManager()
		self.level = self.files.load_map()
		self.back_map = self.render()
		self.feedback = pygame.Surface((self.back_map.get_width(), 250))
		self.sprites = pygame.sprite.LayeredUpdates()
		self.set_map()

	def update(self):
		self.sprites.clear(self.screen, self.back_map)
		dirty = self.sprites.draw(self.screen)
		pygame.display.update(dirty)

	def add_sprite(self, sprite, layer):
		self.sprites.add(sprite, layer)

	def remove_sprite(self, sprite):
		self.sprites.pop(sprite)

	def remove_sprite_layer(self, layer):
		self.sprites.remove_sprites_of_layer(layer)

	def change_map(self, x, y):
		coords = self.level.get_tile(x, y).get("link_coordinates").split(",")
		map_name = self.level.get_tile(x, y).get("link")
		self.level = self.files.load_map(map_name)
		self.back_map = self.render()
		self.set_map()
		return (int(coords[0]), int(coords[1]))

	def set_map(self):
		self.screen.fill((0,0,0))
		self.screen.blit(self.back_map, (0, 0))
		self.screen.blit(self.feedback, (0, self.back_map.get_height()))
		pygame.display.flip()

	def check_door(self, x, y):
		if self.level.get_tile(x, y).get("name") == "door":
			return True
		else:
			return False

	def render(self):
		MAP_TILE_WIDTH = 32
		MAP_TILE_HEIGHT = 32
		image = pygame.Surface((self.level.width*MAP_TILE_WIDTH, self.level.height*MAP_TILE_HEIGHT))
		overlays = {}
		for map_y, line in enumerate(self.level.map):
			for map_x, c in enumerate(line):
				tile_image = self.level.load_tile(map_x, map_y)
				image.blit(tile_image, (map_x*MAP_TILE_WIDTH, map_y*MAP_TILE_HEIGHT))
		return image

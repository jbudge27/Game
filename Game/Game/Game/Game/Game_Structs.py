import pygame
from pygame.locals import *
from Sprite import Sprite

class Utils:
	def __init__(self):
		self.MAP_TILE_WIDTH = 32
		self.MAP_TILE_HEIGHT = 32


class Monster(object):
	def __init__(self, name, init_x, init_y, image, stats, other):
		self.utils = Utils()
		self.name = name
		self.x = init_x
		self.y = init_y
		self.sprite = Sprite((self.x * self.utils.MAP_TILE_WIDTH, self.y * self.utils.MAP_TILE_HEIGHT), image, self.name)
		self.stats = stats
		self.exp_given = other['exp']
		self.difficulty = other['difficulty']

	def move(self, dx, dy):
		self.x += dx
		self.y += dy
		self.sprite.move(dx*self.utils.MAP_TILE_WIDTH, dy*self.utils.MAP_TILE_HEIGHT)

	def set_pos(self,abs_pos):
		self.x = abs_pos[0]
		self.y = abs_pos[1]
		self.sprite.move(abs_pos[0]*self.utils.MAP_TILE_WIDTH, abs_pos[1]*self.utils.MAP_TILE_HEIGHT)
		

class Item(object):
	def __init__(self, name, init_x, init_y, image, stats, flags, equip=None):
		self.utils = Utils()
		self.name = name
		self.x = init_x
		self.y = init_y 
		self.sprite = Sprite((self.x * self.utils.MAP_TILE_WIDTH, self.y * self.utils.MAP_TILE_HEIGHT), image, self.name)
		self.stats = stats
		self.flags = flags
		if equip is not None:
			self.equip = True
			self.equip_type = equip
			self.is_equipped = False
		else:
			self.equip = False

	def add_stat(self, stat_name):
		if stat_name in self.stats:
			return self.stats[stat_name]
		else:
			return 0

	def get_flag(self, flag_name):
		if flag_name in self.flags:
			return self.flags[flag_name]
		else:
			return False

class Player(object):
	def __init__(self, name, init_x, init_y, image, stats, equipment, inventory, skills):
		self.utils = Utils()
		self.name = name
		self.x = init_x
		self.y = init_y 
		self.sprite = Sprite((self.x * self.utils.MAP_TILE_WIDTH, self.y * self.utils.MAP_TILE_HEIGHT), image, self.name)
		self.stats = stats
		self.equipment = equipment
		self.inventory = inventory
		self.skills = skills

	def gain_stat(self, stat, gain):
		if stat in self.stats:
			self.stats[stat] += gain

	def equip(self, equipment):
		self.equipment[equipment.equip_type] = equipment
		equipment.is_equipped = True

	def unequip(self, equip_slot):
		self.equipment[equip_slot].is_equipped = False
		self.equipment.pop(equip_slot)
		
	def add_item(self, item):
		self.inventory.update(item)

	def remove_item(self, item):
		self.inventory.pop(item)

	def add_skill(self, skill):
		self.skills.update(skill)

	def remove_skill(self, skill):
		self.skills.pop(skill)

	def move(self, dx, dy):
		self.x += dx
		self.y += dy
		self.sprite.move(dx*self.utils.MAP_TILE_WIDTH, dy*self.utils.MAP_TILE_HEIGHT)

class Level(object):
	def __init__(self, map, key, tiles):
		self.map = map
		self.key = key
		self.tiles = tiles
		self.width = len(self.map[0])
		self.height = len(self.map)

	def load_tile(self, x, y):
		pos = self.get_tile(x, y).get("tile").split(',')
		image = self.tiles[int(pos[0])][int(pos[1])]
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


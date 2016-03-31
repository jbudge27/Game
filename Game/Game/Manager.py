import pygame, random, copy
from pygame.locals import *
from TileManager import TileManager
import ConfigParser
from Game_Structs import Player, Monster, Item

class Manager:
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


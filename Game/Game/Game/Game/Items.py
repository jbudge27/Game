import pygame
from pygame.locals import *
from TileManager import TileManager
from Sprite import Sprite
import ConfigParser

class Items(object):

	def __init__(self):
		table = TileManager(32, 32)
		self.sprites = table["tiles/general.bmp"]
		self.item_instance = []
		#master list of possible items
		self.master_list = self.load_sheet()

	def load_sheet(self):
		#loads the master list.
		line = {}
		parser = ConfigParser.ConfigParser()
		parser.read("monsters/items.mon")
		for section in parser.sections():
			desc = dict(parser.items(section))
			#line[section] = desc
			for key, w in desc.items():
				if key == 'stats':
					s = desc.pop(key).split(';')
					desc[key] = {}
					for n in s:
						m = n.split(',')
						print m
						desc[key][m[0]] = int(m[1])
				if key == 'flags':
					desc[key] = w.split('\n')
				if key == 'equip':
					desc[key] = bool(w)
				if key == 'mana':
					desc[key] = int(w)
				if key == 'sprite':
					pos = w.split(',')
					print pos
					desc[key] = self.sprites[int(pos[0])][int(pos[1])]
			line[section] = desc
			print line
			#s = line[section].pop('stats').split(';')
			#line[section]['stats'] = {}
			#print s
			#for n in s:
			#	m = n.split(',')
			#	print n
			#	print m
			#	l = int(m[1])
			#	line[section]['stats'].update({m[0]:l}) 
		#print line
		return line

	def __getitem__(self, item):
		try:
			return self.master_list[item]
		except KeyError:
			print "error getting item"

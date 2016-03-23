import ConfigParser
import pygame
from pygame.locals import *

class Player(object):
	def __init__(self, name="base"):
		filename = "players/" + name + ".plyr"
		self.load_player(filename)

	def load_player(self, filename):
		parser = ConfigParser.ConfigParser()
		parser.read(filename)
		self.player = {}
		self.icon = pygame.image.load(parser.get("misc", "icon"))
		self.name = parser.get("misc", "name")
		self.x = int(parser.get("misc", "x"))
		self.y = int(parser.get("misc", "y"))
		#load all the data from the file into a workable array of dicts.
		for section in parser.sections():
			desc = dict(parser.items(section))
			self.player[section] = desc
		#print self.player
		#turns all the stats into ints for ease of use later.
		#for sub in self.player['stats']:
		#	for key in sub:
		#		sub[key] = int(sub[key])
		#[dict([a, int(x)] for a, x in b.iteritems()) for b in self.player['stats']]
		for i in self.player['stats']:
			self.player['stats'][i] = int(self.player['stats'][i])
		print self.player
		#print self.x + ', ' + self.y



	def gain_stat(self, stat_name, gain):
		self.player["stats"][stat_name] += gain

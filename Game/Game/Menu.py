import pygame
from pygame.locals import *
from Player import Player

class Menu(object):
	def __init__(self, p, args = {}):
		self.screen = pygame.display.set_mode(200, 200)
		self.screen.fill((0, 0, 0))
		self.menu_back = pygame.Surface(args['width'], args['height'])
		menu_back.blit()

	def display(image):
		self.menu_back.blit(image)
		pygame.display.flip()

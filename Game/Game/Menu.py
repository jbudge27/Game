import pygame
from pygame.locals import *
from Player import Player
from Sprite import Sprite

class Menu(object):
	def __init__(self, p, args = {}):
		self.info = args
		self.player = p
		#self.screen = pygame.display.set_mode((args['width'], args['height']))
		#self.screen.fill((0, 0, 0))
		self.menu_back = pygame.Surface((args['width'], args['height']))
		self.sidebar = self.menu_back.subsurface(pygame.Rect(0, 0, args['sidebar_width'], args['height']))
		#self.display_image(self.menu_back, 0, 0)
		self.sprites = pygame.sprite.RenderUpdates()

	def display_image(self, image, x, y):
		conv = Sprite((x, y), image)
		self.sprites.add(conv)
		#self.screen.blit(image, (x, y))
		#pygame.display.flip()

	def write(self, text):
		#returns a surface with the specified text on it.
		font = pygame.font.Font(None, 36)
		t = font.render(text, 1, (255, 255, 255))
		return t

	def run_menu(self):
		keep_menu = True
		clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.info['width'], self.info['height']))
		self.menu_back = pygame.Surface((self.info['width'], self.info['height']))
		self.screen.blit(self.menu_back, (0, 0))
		self.display_image(self.write("The Menu"), 0, 0)
		pygame.display.flip()
		while keep_menu:
			self.sprites.clear(self.screen, self.menu_back)
			#sprites.update()
			dirty = self.sprites.draw(self.screen)
			pygame.display.update(dirty)
			clock.tick(16)
			#handle any events that may occur.
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT:
					keep_menu = False
				elif event.type == pygame.locals.MOUSEBUTTONDOWN:
					self.sprites.empty()
					pos = pygame.mouse.get_pos()
					self.display_image(self.write("Position clicked: " + str(pos)), 160, 40)

import pygame
from pygame.locals import *
from Player import Player
from Sprite import Sprite
from Items import Items

class Menu(object):
	def __init__(self, p, args = {}):
		self.info = args
		self.items = Items()
		self.player = p
		s_width = args['sidebar_width']
		b_height = args['button_height']
		width = args['width']
		height = args['height']
		self.submenu = "player"
		#create all the little subsections of the menu
		self.menu_back = pygame.Surface((width, height))
		self.sidebar = self.menu_back.subsurface(pygame.Rect(0, 0, s_width, height))
		self.buttons = self.menu_back.subsurface(pygame.Rect(s_width, 0, width - s_width, b_height))
		self.action_items = self.menu_back.subsurface(pygame.Rect(s_width, b_height, (width / 2) - s_width, height - b_height))
		self.menu_area = self.menu_back.subsurface(pygame.Rect(s_width, b_height, width - s_width, height - b_height))
		#print self.action_items.get_rect()
		#print self.menu_back.get_rect()
		#print self.sidebar.get_rect()
		#print self.buttons.get_rect()
		self.options = self.menu_back.subsurface(pygame.Rect((self.sidebar.get_width() + self.action_items.get_width()), b_height, width - (self.sidebar.get_width() + self.action_items.get_width()), height - b_height))
		#initialize sprite box
		self.sprites = pygame.sprite.RenderUpdates()
		#build buttons to click
		#self.sidebar.fill((255, 0, 0))
		#self.buttons.fill((0, 255, 0))
		#self.action_items.fill((0, 0, 255))
		#self.options.fill((255, 255, 0))
		items = self.make_button("Items", self.buttons, 0, 0)
		equip = self.make_button("Equipment", self.buttons, items.rect.width + 2, 0)
		skill = self.make_button("Skills", self.buttons, items.rect.width + equip.rect.width + 6, 0)
		play = self.make_button("Player", self.buttons, items.rect.width + equip.rect.width + skill.rect.width + 10, 0)
		#build submenu that defaults to - Player Info
		self.run_play()

	def run_play(self):
		self.clear_surface(self.menu_area)
		font_size = 16
		offset = font_size / 2
		i = 0
		for key, stat in self.player.player['stats'].items():
			self.write_to_section(key + ": " + str(stat), self.action_items, 15, offset + font_size * i, key)
			i += 1

	def run_equip(self):
		self.submenu = "equip"
		print "Not yet..."

	def run_skills(self):
		self.submenu = "skills"
		print "Not yet..."

	def run_items(self):
		self.submenu = "items"
		self.clear_surface(self.menu_area)
		font_size = 16
		offset = font_size / 2
		i = 0
		invent_list = self.player.player['items']['inventory'].split('\n')
		for key in invent_list:
			self.write_to_section(key, self.action_items, 15, offset + font_size * i, key)
			self.display_image(self.items[key]['sprite'], 150, offset + font_size + i, key + "_image")
			i += 1
		ops = self.make_button("Use", self.options, 15, 30)
		dis = self.make_button("Discard", self.options, 15, 50)

	def display_image(self, image, x, y, name):
		conv = Sprite((x, y), image, name)
		self.sprites.add(conv)

	def write(self, text):
		#returns a surface with the specified text on it.
		font = pygame.font.Font(None, 16)
		t = font.render(text, 1, (255, 255, 255))
		return t

	def write_to_section(self, text, surf, x, y, name):
		t = self.write(text)
		pos = surf.get_offset()
		sp = Sprite((x + pos[0], y + pos[1]), t, name)
		self.sprites.add(sp)
		#self.screen.blit(surf, surf.get_offset())
		#print "blit"
		#pygame.display.flip()

	def make_button(self, title, surf, x, y, image=None):
		pos = surf.get_offset()
		print 'offset for this surface is: ' + str(pos)
		font = pygame.font.Font(None, 16)
		f = font.render(title, 1, (0, 0, 0))
		t = pygame.Surface((f.get_width() + 2, f.get_height() + 2))
		t.fill((255, 255, 255))
		t.blit(f, (0, 0))
		sp = Sprite((x + pos[0], y + pos[1]), t, title)
		print "Sprite is at " + str(sp.rect.topleft)
		self.sprites.add(sp)
		return sp

	def clear_surface(self, surf):
		pos = surf.get_offset()
		surf_rect = surf.get_rect(topleft=pos)
		for m in self.sprites:
			if (surf_rect.contains(m.rect)):
				print m.name + " was removed from the surface."
				#print surf_rect.topleft
				#print surf_rect.width, surf_rect.height
				#print m.rect.topleft
				#print m.rect.width, m.rect.height
				self.sprites.remove(m)

	def run_menu(self):
		keep_menu = True
		clock = pygame.time.Clock()
		self.screen = pygame.display.set_mode((self.info['width'], self.info['height']))
		#self.menu_back = pygame.Surface((self.info['width'], self.info['height']))
		self.screen.blit(self.menu_back, (0, 0))
		#self.display_image(self.write("The Menu"), 0, 0)
		pygame.display.flip()
		while keep_menu:
			self.sprites.clear(self.screen, self.menu_back)
			#sprites.update()
			dirty = self.sprites.draw(self.screen)
			pygame.display.update(dirty)
			clock.tick(16)
			#pygame.display.flip()
			#handle any events that may occur.
			for event in pygame.event.get():
				if event.type == pygame.locals.QUIT:
					keep_menu = False
				elif event.type == pygame.locals.MOUSEBUTTONDOWN:
					#self.clear_surface(self.action_items)
					pos = pygame.mouse.get_pos()
					for m in self.sprites:
						if m.rect.collidepoint(pos):
							if (m.name == "Items"):
								self.run_items()
								break
							elif (m.name == "Equipment"):
								self.run_equip()
								break
							elif (m.name == "Skills"):
								self.run_skills()
								break
							elif (m.name == "Player"):
								self.run_play()
								break
					#self.display_image(self.write("Position clicked: " + str(pos)), 160, 40)
					#self.write_to_section("Position clicked: " + str(pos), self.action_items, 10, 10, "mouse_notification")
				elif event.type == pygame.locals.KEYDOWN:
					if event.key == K_ESCAPE:
						keep_menu = False
		#self.sprites.empty()

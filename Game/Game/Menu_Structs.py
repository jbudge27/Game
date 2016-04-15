import pygame
from pygame.locals import *

class Button(pygame.sprite.Sprite):
	def __init__(self, text, pos, width=100, height=20):
		pygame.sprite.Sprite.__init__(self)
		self.pos = pos
		self.rect = pygame.Rect(pos[0], pos[1], width, height) 
		font = pygame.font.Font(None, height-4) #four pixels of buffer space.
		t = font.render(text, 1, (0, 0, 0))
		#self.fill((255,255,255)) #white buttons.
		im = pygame.Surface(width, height)
		im.fill((255,255,255))
		im.blit(t, self.rect.topleft)
		self.image = im

	def pressed(self, (x, y)):
		if (self.rect.collidepoint((x, y))):
			return True
		else:
			return False

	def _get_pos(self):
		return (self.rect.midbottom[0]), (self.rect.midbottom[1])

	def _set_pos(self, pos):
		self.rect.topleft = pos[0], pos[1]
		self.depth = self.rect.midbottom[1]

	pos = property(_get_pos, _set_pos)

class Draggable(pygame.sprite.Sprite):
	def __init__(self, x, y, **kwargs):
		super(Sprite, self).__init__()
		#self.frames = frames
		#self.animation = self.stand_animation()
		im = kwargs.get('image')
		text = kwargs.get('text')
		if im is not None:
			self.image = im
		elif text is not None:
			font = pygame.font.Font(None, 16)
			t = font.render(text, 1, (0, 0, 0))
			self.image = pygame.Surface(t.get_width(), t.get_height())
			self.image.fill((255,255,255))
			self.image.blit(t)
		self.rect = image.get_rect()


	def set_pos(self, pos):
		self.rect.topleft = pos[0], pos[1]

	def drag(self, dx, dy):
		self.rect.move_ip(dx, dy)

class Text_Area(pygame.sprite.Sprite):
	def __init__(self, pos, width, height):
		pygame.sprite.Sprite.__init__(self)
		#self.pos = pos
		#self.rect = pygame.Rect(pos[0], pos[1], width, height)
		self.image = pygame.Surface((width, height))
		self.image.fill((0,0,0))
		self.rect = self.image.get_rect()
		self._set_pos(pos)
		self.font_height = 16
		self.font = pygame.font.Font(None, self.font_height)

	def update(self, text):
		print "update function"
		rect = self.rect
		y = rect.top
		while text:
			i = 1
			if y + self.font_height > rect.bottom:
				break
			while self.font.size(text[:i][0]) <  rect.width and i < len(text):
				i += 1
			if i < len(text):
				i = text.rfind(" ", 0, i) + 1
			im = self.font.render(text[:i], 1, (255, 255, 255))
			self.image.blit(im, (rect.left, y))
			y += self.font_height - 2 #line spacing
			text = text[i:]
		#pygame.display.flip()

	def clear(self):
		self.image.fill((0,0,0))

	def _get_pos(self):
		return (self.rect.midbottom[0]), (self.rect.midbottom[1])

	def _set_pos(self, pos):
		self.rect.topleft = pos[0], pos[1]
		#self.depth = self.rect.midbottom[1]

	pos = property(_get_pos, _set_pos)

	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)

#class Menu(pygame.Rect):
#	def __init(self, pos, size):
#		pygame.Rect.__init__(self, pos, size)
		#self.
		

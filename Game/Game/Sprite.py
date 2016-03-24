import pygame
from pygame import *

class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, frames=None):
		super(Sprite, self).__init__()
		self.frames = frames
		self.animation = self.stand_animation()
		self.image = frames[0][0]
		self.rect = self.image.get_rect()
		self.pos = pos
	
	def stand_animation(self):
		while True:
			for frame in self.frames[0]:
			self.image = frame
			yield None
			yield None

	def update(self, *args):
		self.animation.next()

	def _get_pos(self):
		return (self.rect.midbottom[0]), (self.rect.midbottom[1])

	def _set_pos(self, pos):
		self.rect.midbottom = pos[0]+16, pos[1]+32
		self.depth = self.rect.midbottom[1]

	pos = property(_get_pos, _set_pos)

	def move(self, dx, dy):
		self.rect.move_ip(dx, dy)
		self.depth = self.rect.midbottom[1]
		#print "called sprite move function"

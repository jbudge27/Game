import pygame
import Level


if __name__ == "__main__":
	pygame.init()
	screen = pygame.display.set_mode((320, 320))

	MAP_TILE_WIDTH = 32
	MAP_TILE_HEIGHT = 32
	game_over = False
	level = Level()
	level.load_file('levels/test.map')
	clock = pygame.time.Clock()
	background = level.render()
	screen.blit(background, (0, 0))
	pygame.display.flip()
	while not game_over:
		pygame.display.flip()
		clock.tick(15)
		for event in pygame.event.get():
			if event.type == pygame.locals.QUIT:
				game_over = True
			elif event.type == pygame.locals.KEYDOWN:
				pressed_key = event.key


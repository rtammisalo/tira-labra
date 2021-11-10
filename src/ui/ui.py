import sys
import pygame
import pygame.locals as pgl
import ui.grid

class UI():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BACKGROUND_COLOR = (100, 100, 100)

    def __init__(self, grid):
        pygame.init()
        self._screen_size = (UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)
        self._screen = pygame.display.set_mode(self._screen_size)
        self._screen.fill(UI.BACKGROUND_COLOR)
        self._clock = pygame.time.Clock()
        self._grid = ui.grid.Grid(grid)
        self._grid.draw(self._screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self._clock.tick(60)
            pygame.display.flip()

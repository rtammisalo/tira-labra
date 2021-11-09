import sys
import pygame
import pygame.locals as pgl


class Cell(pygame.sprite.DirtySprite):
    WIDTH = 10
    HEIGHT = 10
    EMPTY_COLOR = (0, 0, 0)
    WALL_COLOR = (255, 255, 255)

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface([Cell.WIDTH, Cell.HEIGHT])
        self.image.fill(Cell.EMPTY_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos


class Grid():
    def __init__(self, size):
        self.group = pygame.sprite.RenderUpdates()
        x_size = int(size[0] / Cell.WIDTH)
        x_size = x_size - int(x_size / Cell.WIDTH)
        y_size = int(size[1] / Cell.HEIGHT)
        y_size = y_size - int(y_size / Cell.HEIGHT)
        self.grid = []

        for y in range(y_size):
            self.grid.append([])
            for x in range(x_size):
                cell = Cell((x * (Cell.WIDTH + 1) + 4,
                            y * (Cell.HEIGHT + 1) + 4))
                self.grid[y].append(cell)
                self.group.add(cell)

    def draw(self, surface):
        self.group.draw(surface)


class UI():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BACKGROUND_COLOR = (100, 100, 100)

    def __init__(self):
        pygame.init()
        self._screen_size = (UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)
        self._screen = pygame.display.set_mode(self._screen_size)
        self._screen.fill(UI.BACKGROUND_COLOR)
        self._clock = pygame.time.Clock()
        self._grid = Grid(self._screen_size)
        self._grid.draw(self._screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self._clock.tick(60)
            pygame.display.flip()

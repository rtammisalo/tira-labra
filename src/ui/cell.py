import pygame

class Cell(pygame.sprite.DirtySprite):
    WIDTH = 10
    HEIGHT = 10
    EMPTY_COLOR = (0, 0, 0)
    WALL_COLOR = (255, 255, 255)
    START_COLOR = (0, 0, 200)
    GOAL_COLOR = (200, 0, 0)
    CELL_COLOR = {'.': EMPTY_COLOR, '#': WALL_COLOR,
                  'S': START_COLOR, 'G': GOAL_COLOR}

    def __init__(self, pos, cell):
        super().__init__()
        self.image = pygame.Surface([Cell.WIDTH, Cell.HEIGHT])
        self.update_color(cell)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update_color(self, cell):
        cell_color = self.CELL_COLOR[str(cell)]
        self.image.fill(cell_color)
        self.dirty = 1

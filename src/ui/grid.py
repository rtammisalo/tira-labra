import pygame
from ui.cell import Cell


class Grid():
    def __init__(self, grid):
        self.group = pygame.sprite.RenderUpdates()
        self.grid = []

        for y in range(grid.y_size):
            self.grid.append([])
            for x in range(grid.x_size):
                cell = Cell((x * (Cell.WIDTH + 1) + 4,
                             y * (Cell.HEIGHT + 1) + 4), grid[y][x])
                self.grid[y].append(cell)
                self.group.add(cell)

    def draw(self, surface):
        self.group.draw(surface)

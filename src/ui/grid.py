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

    def set_graph_visited(self, visited_pos):
        self.grid[visited_pos[1]][visited_pos[0]].set_graph_visited()

    def set_graph_visible(self, visible_pos):
        self.grid[visible_pos[1]][visible_pos[0]].set_graph_visible()

    def set_graph_visible_nodes(self, visible_nodes):
        for visible_node in visible_nodes:
            self.set_graph_visible(visible_node.pos)

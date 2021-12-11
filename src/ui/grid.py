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

    def set_graph_look_ahead(self, look_ahead_pos, direction):
        self.grid[look_ahead_pos[1]][look_ahead_pos[0]
                                     ].set_graph_look_ahead(direction)

    def set_graph_visible_nodes(self, visible_nodes):
        for visible_node in visible_nodes:
            self.set_graph_visible(visible_node.pos)

    def set_graph_look_ahead_nodes(self, look_ahead_nodes):
        for node, direction in look_ahead_nodes:
            self.set_graph_look_ahead(node.pos, direction)

    def set_path_to_goal(self, path_to_goal):
        for pos in path_to_goal:
            self.grid[pos[1]][pos[0]].set_path_to_goal()

    def get_cell_pos_at_screen_position(self, pos):
        pos = pos[0] - 4, pos[1] - 4
        if pos[0] < 0 or pos[1] < 0:
            return None
        cell_pos = pos[0] // (Cell.WIDTH + 1), pos[1] // (Cell.HEIGHT + 1)
        if cell_pos[0] < len(self.grid[0]):
            if cell_pos[1] < len(self.grid):
                return cell_pos
        return None

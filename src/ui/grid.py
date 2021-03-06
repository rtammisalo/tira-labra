import pygame
from ui.cell import Cell


class Grid():
    """ A UI-related grid container for holding a group of UI-related Cell-objects. """
    BORDER = 1
    LEFT_PAD = 4
    TOP_PAD = 4

    def __init__(self, grid_pos, grid):
        self.group = pygame.sprite.RenderUpdates()
        self.grid = []
        self._pos = grid_pos

        for y in range(grid.y_size):
            self.grid.append([])
            for x in range(grid.x_size):
                cell = Cell((grid_pos[0] + x * (Cell.WIDTH + Grid.BORDER) + Grid.LEFT_PAD,
                             grid_pos[1] + y * (Cell.HEIGHT + Grid.BORDER) + Grid.TOP_PAD), grid[y][x])
                self.grid[y].append(cell)
                self.group.add(cell)

    def draw(self, surface):
        """ Draws the changed cells to the screen. """
        self.group.draw(surface)

    def move(self, delta_pos):
        """ Moves the UI Grid by delta_pos. Call draw afterwards. """
        self._pos = (self._pos[0] + delta_pos[0], self._pos[1] + delta_pos[1])
        for row in self.grid:
            for cell in row:
                cell.move(delta_pos)

    def set_graph_visited(self, visited_pos):
        """ Sets the cell at visited_pos to show as visited (bright yellow dot). Visited
        on the underlying graph means that the node has been taken out from the heap and
        marked as visited. """
        self.grid[visited_pos[1]][visited_pos[0]].set_graph_visited()

    def set_graph_visible(self, visible_pos):
        """ Sets the cell at visible_pos to show as visible (yellow). Visible on the
        underlying graph means that the node has been added to the heap. """
        self.grid[visible_pos[1]][visible_pos[0]].set_graph_visible()

    def set_graph_look_ahead(self, look_ahead_pos, direction):
        """ JPS related graphical operation. Sets the cell at look_ahead_pos to show
        an arrow for the direction the jumping proceeded in. """
        self.grid[look_ahead_pos[1]][look_ahead_pos[0]
                                     ].set_graph_look_ahead(direction)

    def set_graph_visible_nodes(self, visible_nodes):
        """ Sets the cells related to the nodes in visible_nodes as visible.
        """
        for visible_node in visible_nodes:
            self.set_graph_visible(visible_node.pos)

    def set_graph_look_ahead_nodes(self, look_ahead_nodes):
        """ Makes the cells related to the nodes in look_ahead_nodes show
        jump direction arrows. """
        for node, direction in look_ahead_nodes:
            self.set_graph_look_ahead(node.pos, direction)

    def set_path_to_goal(self, path_to_goal):
        """ Draws the path to the goal on the cells on the path. """
        for pos in path_to_goal:
            self.grid[pos[1]][pos[0]].set_path_to_goal()

    def get_cell_pos_at_screen_position(self, screen_pos):
        """ Returns the cell position underneath the actual screen position. """
        world_pos = (screen_pos[0] - Grid.LEFT_PAD - self._pos[0],
                     screen_pos[1] - Grid.TOP_PAD - self._pos[1])
        if world_pos[0] < 0 or world_pos[1] < 0:
            return None
        cell_pos = (world_pos[0] // (Cell.WIDTH + Grid.BORDER),
                    world_pos[1] // (Cell.HEIGHT + Grid.BORDER))
        if cell_pos[0] < len(self.grid[0]):
            if cell_pos[1] < len(self.grid):
                return cell_pos
        return None

    def show_idastar_path(self, path):
        for index, pos in enumerate(path):
            self.grid[pos[1]][pos[0]].show_idastar_path(index)

    def hide_idastar_path(self, path):
        for pos in path:
            self.grid[pos[1]][pos[0]].hide_idastar_path()

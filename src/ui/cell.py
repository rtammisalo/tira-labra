import pygame
from entities.grid import Grid
from entities.cell import Cell


class Cell(pygame.sprite.DirtySprite):
    """ A class to provide graphical representation for graph nodes/cells. """
    WIDTH = 10
    HEIGHT = 10
    EMPTY_COLOR = (0, 0, 0)
    WALL_COLOR = (255, 255, 255)
    START_COLOR = (0, 0, 200)
    GOAL_COLOR = (200, 0, 0)
    CELL_COLOR = {Cell.EMPTY: EMPTY_COLOR, Cell.WALL: WALL_COLOR,
                  Cell.START: START_COLOR, Cell.GOAL: GOAL_COLOR}
    VISITED_COLOR = (255, 255, 100)
    VISIBLE_COLOR = (120, 120, 10, 10)
    PATH_MARKER_COLOR = (250, 0, 250)
    IDASTAR_PATH_MARKER_COLOR = (150, 200, 150)
    DIRECTION_MARKER_COLOR = (50, 50, 200)
    DIRECTION_MARKER_VERTICES = {
        Grid.DOWN: [(WIDTH//2, HEIGHT - 1), (WIDTH//2 - 3, HEIGHT - 4), (WIDTH//2 + 3, HEIGHT - 4)],
        Grid.UP: [(WIDTH//2, 0), (WIDTH//2 - 3, 3), (WIDTH//2 + 3, 3)],
        Grid.RIGHT: [(WIDTH - 1, HEIGHT//2), (WIDTH - 4, HEIGHT//2 - 3), (WIDTH - 4, HEIGHT//2 + 3)],
        Grid.LEFT: [(0, HEIGHT//2), (3, HEIGHT//2 - 3), (3, HEIGHT//2 + 3)],
        Grid.NE: [(WIDTH - 1, 0), (WIDTH - 4, 0), (WIDTH - 1, 3)],
        Grid.SE: [(WIDTH - 1, HEIGHT - 1), (WIDTH - 4, HEIGHT - 1), (WIDTH - 1, HEIGHT - 4)],
        Grid.SW: [(0, HEIGHT - 1), (3, HEIGHT - 1), (0, HEIGHT - 4)],
        Grid.NW: [(0, 0), (0, 3), (3, 0)],
    }

    def __init__(self, pos, cell):
        """ Takes as args the cell position on the UI grid and the actual grid cell,
        which contains wall data, etc. """
        super().__init__()
        self.image = self._get_new_surface()
        self._set_color(cell)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self._graph_visible = False

    def move(self, delta_pos):
        """Moves the cell by delta_pos."""
        self.rect.x += delta_pos[0]
        self.rect.y += delta_pos[1]
        self.dirty = 1

    def _set_color(self, cell):
        """ Set the color of the cell to match the color of the cell. """
        cell_color = self.CELL_COLOR[str(cell)]
        self.image.fill(cell_color)
        self.dirty = 1

    def _get_cell_center(self):
        return (Cell.WIDTH // 2, Cell.HEIGHT // 2)

    def set_graph_visited(self):
        """ Draw the UI cell as visited. Paints a small yellow dot on the cell. """
        pygame.draw.circle(self.image, Cell.VISITED_COLOR,
                           self._get_cell_center(), 2)
        self.dirty = 1

    def set_graph_visible(self):
        """ Draw the UI cell as visible to the algorithm. Paints
        the cell yellow. """
        if not self._graph_visible:
            self.image.fill(Cell.VISIBLE_COLOR,
                            special_flags=pygame.BLEND_RGBA_ADD)
            self.dirty = 1
            self._graph_visible = True

    def set_graph_look_ahead(self, direction):
        """ Draws a small blue-ish arrow on the edge of the cell to mark
        the cell as a jumped over. The arrow points to the jump direction. """
        vertices = self.DIRECTION_MARKER_VERTICES[direction]
        pygame.draw.polygon(self.image, Cell.DIRECTION_MARKER_COLOR, vertices)
        self.dirty = 1

    def _get_new_surface(self):
        return pygame.Surface([Cell.WIDTH, Cell.HEIGHT]).convert_alpha()

    def set_path_to_goal(self):
        """ Draws a cross on the cell to mark it as one of the path cells. """
        pygame.draw.aaline(self.image, Cell.PATH_MARKER_COLOR,
                           (0, 0), (Cell.WIDTH, Cell.HEIGHT))
        pygame.draw.aaline(self.image, Cell.PATH_MARKER_COLOR,
                           (Cell.WIDTH, 0), (0, Cell.HEIGHT))
        self.dirty = 1

    def show_idastar_path(self, nodes_from_start):
        self._old_image = self.image.copy()
        if nodes_from_start > 10:
            nodes_from_start = 10
        color = (self.IDASTAR_PATH_MARKER_COLOR[0] - nodes_from_start * 5,
                 self.IDASTAR_PATH_MARKER_COLOR[1] - nodes_from_start * 5,
                 self.IDASTAR_PATH_MARKER_COLOR[2] - nodes_from_start * 5)
        self.image.fill(color)
        self.set_graph_visited()
        self.dirty = 1

    def hide_idastar_path(self):
        self.image = self._old_image
        self.dirty = 1

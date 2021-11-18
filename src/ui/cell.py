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
    VISITED_COLOR = (255, 255, 100)
    VISIBLE_COLOR = (150, 150, 20, 50)

    def __init__(self, pos, cell):
        super().__init__()
        self.image = self._get_new_surface()
        self.set_color(cell)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self._graph_visible = False

    def set_color(self, cell):
        cell_color = self.CELL_COLOR[str(cell)]
        self.image.fill(cell_color)
        self.dirty = 1

    def set_graph_visited(self):
        pygame.draw.polygon(self.image, Cell.VISITED_COLOR,
                            [(0, 0), (Cell.WIDTH, 0), (0, Cell.HEIGHT)])
        self.dirty = 1

    def set_graph_visible(self):
        if not self._graph_visible:
            self.image.fill(Cell.VISIBLE_COLOR,
                            special_flags=pygame.BLEND_RGBA_ADD)
            self.dirty = 1
            self._graph_visible = True

    def _get_new_surface(self):
        return pygame.Surface([Cell.WIDTH, Cell.HEIGHT]).convert_alpha()

import sys
import pygame
import pygame.locals as pgl
import ui.grid


class UI():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BACKGROUND_COLOR = (100, 100, 100)

    def __init__(self, grid, path_to_goal, history):
        pygame.init()
        self._screen_size = (UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)
        self._screen = pygame.display.set_mode(self._screen_size)
        self._screen.fill(UI.BACKGROUND_COLOR)
        self._clock = pygame.time.Clock()
        self._grid = ui.grid.Grid(grid)
        self._grid.draw(self._screen)
        self._path_to_goal = path_to_goal
        self._history = history

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        step = self._history.advance_step()
                        if not step:
                            continue
                        visited_node, visible_nodes = step
                        self._grid.set_graph_visited(visited_node.pos)
                        self._grid.set_graph_visible_nodes(visible_nodes)
                        self._grid.draw(self._screen)
            self._clock.tick(30)
            pygame.display.flip()

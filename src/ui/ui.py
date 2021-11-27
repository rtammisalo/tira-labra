import sys
import pygame
import ui.grid
from services.dijkstra import Dijkstra


class UI():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BACKGROUND_COLOR = (100, 100, 100)

    def __init__(self, grid, algorithm):
        pygame.init()
        self._screen_size = (UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)
        self._screen = pygame.display.set_mode(self._screen_size)
        self._screen.fill(UI.BACKGROUND_COLOR)
        self._clock = pygame.time.Clock()
        self._grid = ui.grid.Grid(grid)
        self._grid.draw(self._screen)
        self._algorithm = algorithm
        self._step_algorithm = algorithm.next_step()
        self._keyboard_timer = 0
        self._keys_pressed = set()

    def run(self):
        while True:
            self._process_input()
            self._clock.tick(30)
            pygame.display.flip()

    def _process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            self._keys_pressed.add(pygame.K_SPACE)

        if self._keyboard_timer != 0:
            self._keyboard_timer -= 1
            return

        if pygame.K_SPACE in self._keys_pressed:
            self._process_next_step()

        self._keyboard_timer = 2
        self._keys_pressed = set()

    def _process_next_step(self):
        if isinstance(self._algorithm, Dijkstra):
            try:
                visited_node, visible_nodes = self._step_algorithm.__next__()
                self._grid.set_graph_visited(visited_node.pos)
                self._grid.set_graph_visible_nodes(visible_nodes)
            except StopIteration as stop:
                path_to_goal = stop.value
                if path_to_goal:
                    self._grid.set_path_to_goal(path_to_goal)

        self._grid.draw(self._screen)

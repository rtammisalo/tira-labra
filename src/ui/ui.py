import sys
import pygame
import ui.grid
from services.dijkstra import Dijkstra
from services.jps import JPS


class UI():
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 830
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
        self._run_to_end = False

    def run(self):
        while True:
            self._process_input()
            self._clock.tick(60)
            pygame.display.flip()

    def _process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if self._run_to_end:
            for i in range(20):
                self._process_next_step()
            self._grid.draw(self._screen)

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_SPACE]:
            self._keys_pressed.add(pygame.K_SPACE)
        if key_pressed[pygame.K_e]:
            self._run_to_end = True
        if key_pressed[pygame.K_ESCAPE]:
            sys.exit()

        if self._keyboard_timer != 0:
            self._keyboard_timer -= 1
            return

        if pygame.K_SPACE in self._keys_pressed:
            self._process_next_step()
            self._grid.draw(self._screen)

        self._keyboard_timer = 40
        self._keys_pressed = set()

    def _process_next_step(self):
        path_to_goal = None

        if isinstance(self._algorithm, Dijkstra):
            try:
                visited_node, visible_nodes = self._step_algorithm.__next__()
                self._update_grid(visited_node, visible_nodes)
            except StopIteration as stop:
                path_to_goal = stop.value
        elif isinstance(self._algorithm, JPS):
            try:
                visited_node, visible_nodes, look_ahead_nodes = self._step_algorithm.__next__()
                self._update_grid(
                    visited_node, visible_nodes, look_ahead_nodes)
            except StopIteration as stop:
                path_to_goal = stop.value

        if path_to_goal:
            self._grid.set_path_to_goal(path_to_goal)

    def _update_grid(self, visited_node, visible_nodes, look_ahead_nodes=None):
        self._grid.set_graph_visited(visited_node.pos)
        self._grid.set_graph_visible_nodes(visible_nodes)
        if look_ahead_nodes:
            self._grid.set_graph_look_ahead_nodes(look_ahead_nodes)

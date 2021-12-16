import sys
import pygame
from services.ida_star import IDAStar
import ui.grid
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.jps import JPS
from services.ida_star import IDAStar


class UI():
    """ The main UI class, call run-method after initializing. """
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 1200
    BACKGROUND_COLOR = (100, 100, 100)
    STEPS_PER_UPDATE = 100

    def __init__(self, grid_string):
        """ Takes as argument the string description of the grid. """
        pygame.display.init()
        self._print_help()
        self._grid_string = grid_string
        self._create_grid_from_string()
        self._screen_pos = (0, 0)
        self._screen_size = (UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)
        self._screen = pygame.display.set_mode(self._screen_size)
        self._clock = pygame.time.Clock()
        self._algorithm_class = Dijkstra
        self._reset_run()

    def _print_help(self):
        print("\nKäyttöohjeet:")
        print("mouse 1 - siirrä lähtöruutu")
        print("mouse 2 - siirrä maaliruutu")
        print("mouse 3 - muuta seinä tyhjäksi tai toisinpäin")
        print("lshift + mouse 1 - vaihtaa ruudun keskipistettä")
        print("d - vaihda käyttöön Dijkstran algoritmi")
        print("j - vaihda käyttöön JPS algoritmi")
        print("r - aja algoritmi nopeasti loppuun")
        print("space - aja algoritmin seuraava askel (ottaa yhden ruudun pois keosta)")
        print("c - tyhjentää kartan seinistä")
        print("n - palauttaa alkuperäisen kartan konfiguraation")
        print("ESC - lopettaa ohjelman\n")

    def _set_algorithm(self, algorithm=None):
        if not algorithm:
            algorithm = self._algorithm_class
        self._algorithm_class = algorithm
        self._algorithm = algorithm(self._grid)
        self._step_algorithm = self._algorithm.next_step()

    def _reset_ui_grid(self):
        self._screen.fill(UI.BACKGROUND_COLOR)
        ui_grid_pos = (0 - self._screen_pos[0], 0 - self._screen_pos[1])
        self._ui_grid = ui.grid.Grid(ui_grid_pos, self._grid)
        self._ui_grid.draw(self._screen)

    def _create_grid_from_string(self):
        self._grid = Grid(self._grid_string)

    def _reset_run(self, algorithm=None):
        self._keys_pressed = set()
        self._keyboard_timer = 0
        self._run_to_end = False
        self._set_algorithm(algorithm)
        self._reset_ui_grid()

    def _set_new_start_position(self, cell_pos):
        old_start = self._algorithm.graph.get_start_node().pos
        self._grid.set_new_start(old_start, cell_pos)

    def _set_new_goal_position(self, cell_pos):
        old_goal = self._algorithm.graph.get_goal_node().pos
        self._grid.set_new_goal(old_goal, cell_pos)

    def run(self):
        """ Starts the UI. """
        while True:
            self._process_input()
            self._clock.tick(60)
            pygame.display.flip()

    def _handle_move_screen(self, new_pos):
        """ Considers the new screen mid-point to be new_pos. """
        new_screen_pos = (self._screen_size[0] // 2 - new_pos[0],
                          self._screen_size[1] // 2 - new_pos[1])
        self._ui_grid.move(new_screen_pos)
        new_screen_pos = (self._screen_pos[0] - new_screen_pos[0],
                          self._screen_pos[1] - new_screen_pos[1])
        self._screen_pos = new_screen_pos
        self._screen.fill(UI.BACKGROUND_COLOR)
        self._ui_grid.draw(self._screen)

    def _process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    self._handle_move_screen(event.pos)
                    return
                cell_pos = self._ui_grid.get_cell_pos_at_screen_position(
                    event.pos)
                if cell_pos:
                    if event.button == 1:
                        self._set_new_start_position(cell_pos)
                    elif event.button == 2:
                        self._set_new_goal_position(cell_pos)
                    elif event.button == 3:
                        self._grid.flip_cell_status(cell_pos)

                    self._reset_run()
                    return

        if self._run_to_end:
            for i in range(self.STEPS_PER_UPDATE):
                self._process_next_step()
            self._ui_grid.draw(self._screen)

        self._process_keyboard_input()

    def _process_keyboard_input(self):
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_SPACE]:
            self._keys_pressed.add(pygame.K_SPACE)
        if key_pressed[pygame.K_r]:
            self._run_to_end = True
        if key_pressed[pygame.K_d]:
            self._reset_run(Dijkstra)
        if key_pressed[pygame.K_j]:
            self._reset_run(JPS)
        if key_pressed[pygame.K_i]:
            self._reset_run(IDAStar)
        if key_pressed[pygame.K_c]:
            self._grid.clear_walls()
            self._reset_run()
        if key_pressed[pygame.K_n]:
            self._screen_pos = (0, 0)
            self._create_grid_from_string()
            self._reset_run()
        if key_pressed[pygame.K_ESCAPE]:
            sys.exit()

        if self._keyboard_timer != 0:
            self._keyboard_timer -= 1
            return

        if pygame.K_SPACE in self._keys_pressed:
            self._process_next_step()
            self._ui_grid.draw(self._screen)

        self._keyboard_timer = 3
        self._keys_pressed = set()

    def _process_next_step(self):
        path_to_goal = None

        if isinstance(self._algorithm, Dijkstra):
            try:
                visited_node, visible_nodes = self._step_algorithm.__next__()
                self._update_grid([visited_node], visible_nodes)
            except StopIteration as stop:
                path_to_goal = stop.value
        elif isinstance(self._algorithm, JPS):
            try:
                visited_node, visible_nodes, look_ahead_nodes = self._step_algorithm.__next__()
                self._update_grid(
                    [visited_node], visible_nodes, look_ahead_nodes)
            except StopIteration as stop:
                path_to_goal = stop.value
        elif isinstance(self._algorithm, IDAStar):
            try:
                visited_nodes = self._step_algorithm.__next__()
                self._update_grid(visited_nodes, visited_nodes)
            except StopIteration as stop:
                path_to_goal = stop.value

        if path_to_goal:
            self._ui_grid.set_path_to_goal(path_to_goal)

    def _update_grid(self, visited_nodes, visible_nodes, look_ahead_nodes=None):
        for visited_node in visited_nodes:
            self._ui_grid.set_graph_visited(visited_node.pos)
        self._ui_grid.set_graph_visible_nodes(visible_nodes)
        if look_ahead_nodes:
            self._ui_grid.set_graph_look_ahead_nodes(look_ahead_nodes)

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
    SCREEN_HEIGHT = 800
    BACKGROUND_COLOR = (100, 100, 100)
    STEPS_PER_UPDATE = 100

    def __init__(self, grid_string):
        """ Takes as argument the string description of the grid. """
        pygame.display.init()
        pygame.display.set_caption("MazeFinder")
        self._print_help()
        self._grid_string = grid_string
        self._create_grid_from_string()
        self._screen_pos = (0, 0)
        self._screen_size = (UI.SCREEN_WIDTH, UI.SCREEN_HEIGHT)
        self._screen = pygame.display.set_mode(self._screen_size)
        self._clock = pygame.time.Clock()
        # Use Dijkstra's algorithm by default.
        self._algorithm_class = Dijkstra
        self._reset_run()

    def _print_help(self):
        print("\nKäyttöohjeet:")
        print("mouse 1 - siirrä lähtöruutu")
        print("lshift + mouse 1 - siirrä maaliruutu")
        print("mouse 2 - vaihtaa ruudun keskipistettä")
        print("mouse 3 - muuta seinä tyhjäksi tai toisinpäin")
        print("d - vaihda käyttöön Dijkstran algoritmi")
        print("j - vaihda käyttöön JPS algoritmi")
        print("i - vaihda käyttöön IDA* algoritmi")
        print("r - aja algoritmi nopeasti loppuun")
        print("space - aja algoritmin seuraava 'askel'")
        print("c - tyhjentää kartan seinistä")
        print("n - palauttaa alkuperäisen kartan konfiguraation")
        print("s - lopettaa algoritmin ajon (r-komento) kesken / IDA* polkujen näytön")
        print("h - tulostaa käyttöohjeet uudestaan")
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

    def _process_mouse_events(self, event):
        if event.button == 2:
            self._handle_move_screen(event.pos)
            return False

        cell_pos = self._ui_grid.get_cell_pos_at_screen_position(
            event.pos)
        if cell_pos:
            if event.button == 1:
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    self._set_new_goal_position(cell_pos)
                else:
                    self._set_new_start_position(cell_pos)
            elif event.button == 3:
                self._grid.flip_cell_status(cell_pos)

            self._reset_run()
            return False
        return True

    def _process_keydown_events(self, event):
        if event.key == pygame.K_r:
            if not self._run_to_end:
                print("Ajetaan algoritmi nopeasti loppuun..")
                self._run_to_end = True
                return True
        elif event.key == pygame.K_SPACE:
            self._keys_pressed.add(pygame.K_SPACE)
            return True
        elif event.key == pygame.K_h:
            self._print_help()
            return True
        elif event.key == pygame.K_d:
            print("Vaihdetaan Dijkstran algoritmiin.")
            self._reset_run(Dijkstra)
        elif event.key == pygame.K_j:
            print("Vaihdetaan JPS algoritmiin.")
            self._reset_run(JPS)
        elif event.key == pygame.K_i:
            print("Vaihdetaan IDA* algoritmiin.")
            self._reset_run(IDAStar)
        elif event.key == pygame.K_c:
            self._grid.clear_walls()
            self._reset_run()
        elif event.key == pygame.K_n:
            self._screen_pos = (0, 0)
            self._create_grid_from_string()
            self._reset_run()
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        return False

    def _process_keyup_events(self, event):
        if event.key == pygame.K_SPACE:
            if pygame.K_SPACE in self._keys_pressed:
                self._keys_pressed.remove(pygame.K_SPACE)
        return True

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self._process_mouse_events(event):
                    return False
            elif event.type == pygame.KEYDOWN:
                if not self._process_keydown_events(event):
                    return False
            elif event.type == pygame.KEYUP:
                if not self._process_keyup_events(event):
                    return False
        return True

    def _process_input(self):
        if not self._process_events():
            return

        if self._run_to_end:
            # Have some way to stop auto-running to the end.
            # This is mostly because of IDA*.
            for i in range(self.STEPS_PER_UPDATE):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                            print("Laskenta lopetettu.")
                            self._run_to_end = False
                            return
                self._process_next_step()
            self._ui_grid.draw(self._screen)

        self._process_space_input()

    def _process_space_input(self):
        if self._keyboard_timer != 0:
            self._keyboard_timer -= 1
            return

        if pygame.K_SPACE in self._keys_pressed:
            self._process_next_step()
            self._ui_grid.draw(self._screen)

        self._keyboard_timer = 3

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
                visited_nodes, found_paths = self._step_algorithm.__next__()
                self._update_grid(visited_nodes, visited_nodes)
                self._show_idastar_found_paths(found_paths)
            except StopIteration as stop:
                path_to_goal = stop.value

        if path_to_goal:
            print("Polun pituus:", self._get_path_cost(path_to_goal))
            self._ui_grid.set_path_to_goal(path_to_goal)

    def _get_path_cost(self, path):
        import math
        total_cost = 0
        previous_pos = path[0]
        for next_pos in path[1:]:
            total_cost += math.sqrt((next_pos[0]-previous_pos[0])**2
                                    + (next_pos[1]-previous_pos[1])**2)
            previous_pos = next_pos
        return total_cost

    def _update_grid(self, visited_nodes, visible_nodes, look_ahead_nodes=None):
        for visited_node in visited_nodes:
            self._ui_grid.set_graph_visited(visited_node.pos)
        self._ui_grid.set_graph_visible_nodes(visible_nodes)
        if look_ahead_nodes:
            self._ui_grid.set_graph_look_ahead_nodes(look_ahead_nodes)

    def _show_idastar_found_paths(self, found_paths):
        if self._run_to_end or len(found_paths) == 0:
            return

        self._ui_grid.draw(self._screen)
        pygame.display.flip()
        time_per_path = 10
        skip_show_path = False

        for path in found_paths:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        skip_show_path = True
                if event.type == pygame.KEYUP:
                    self._process_keyup_events(event)
            if skip_show_path:
                break
            self._ui_grid.show_idastar_path(path)
            self._ui_grid.draw(self._screen)
            pygame.display.flip()
            pygame.time.wait(time_per_path)
            self._ui_grid.hide_idastar_path(path)

        self._ui_grid.draw(self._screen)
        pygame.display.flip()

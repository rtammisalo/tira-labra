import math
import unittest
from entities.grid import Grid
from services.dijkstra import Dijkstra


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        simple_test_grid = Grid("""
        ####
        S..G
        ##.#
        """)
        self.dijkstra = Dijkstra(simple_test_grid)

    def test_simple_test_path_to_goal_is_correct(self):
        path = self.dijkstra.run()
        self.assertEqual(path, [(0, 1), (1, 1), (2, 1), (3, 1)])

    def test_simple_test_next_steps_return_correct_visited_and_visible_nodes(self):
        next_step_gen = self.dijkstra.next_step()
        visited_node, visible_nodes = next_step_gen.__next__()
        self.assertEqual(visited_node.pos, (0, 1))
        self.assertEqual(list_positions(visible_nodes), [(1, 1)])

        visited_node, visible_nodes = next_step_gen.__next__()
        self.assertEqual(visited_node.pos, (1, 1))
        self.assertCountEqual(list_positions(visible_nodes), [(2, 1), (2, 2)])

        visited_node, visible_nodes = next_step_gen.__next__()
        self.assertEqual(visited_node.pos, (2, 1))
        self.assertCountEqual(list_positions(visible_nodes), [(2, 2), (3, 1)])

    def test_dijkstra_on_a_grid_with_no_path_to_goal_returns_empty_list_as_path(self):
        dijkstra = Dijkstra(Grid("S#G"))
        path = dijkstra.run()
        self.assertEqual(len(path), 0)

    def test_dijkstra_complex_path_length_is_correct(self):
        grid = """
        S........#
        .#######.#
        .#.......#
        .#.#######
        .#.......#
        .########.
        .####.#...
        #.##...#.G
        ##.#.#.#.#
        ###.#.#.##
        """
        correct_length = 8 + 7 * math.sqrt(2)
        dijkstra = Dijkstra(Grid(grid))
        path = dijkstra.run()
        path_length = calculate_path_length(path)
        self.assertAlmostEqual(path_length, correct_length, places=5)


def list_positions(nodes):
    return [node.pos for node in nodes]


def calculate_path_length(path):
    length = 0
    pos = path[0]

    for next_pos in path[1:]:
        length += math.sqrt(sum([(coords[0] - coords[1]) ** 2
                                 for coords in zip(pos, next_pos)]))
        pos = next_pos

    return length

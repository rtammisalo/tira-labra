import math
import unittest
from entities.grid import Grid
import services.dijkstra as dijkstra


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        simple_test_grid = Grid("""
        ####
        S..G
        ##.#
        """)
        goal, history = dijkstra.dijkstra(simple_test_grid)
        self.simple_test_goal = goal
        self.simple_test_history = history

    def test_simple_test_path_to_goal_is_correct(self):
        path = self.simple_test_goal.path_from_start()
        self.assertEqual(path, [(0, 1), (1, 1), (2, 1), (3, 1)])

    def test_simple_test_history_contains_correct_visited_and_visible_nodes(self):
        visited_node, visible_nodes = self.simple_test_history.advance_step()
        self.assertEqual(visited_node.pos, (0, 1))
        self.assertEqual(list_positions(visible_nodes), [(1, 1)])

        visited_node, visible_nodes = self.simple_test_history.advance_step()
        self.assertEqual(visited_node.pos, (1, 1))
        self.assertCountEqual(list_positions(visible_nodes), [(2, 1), (2, 2)])

        visited_node, visible_nodes = self.simple_test_history.advance_step()
        self.assertEqual(visited_node.pos, (2, 1))
        self.assertCountEqual(list_positions(visible_nodes), [(2, 2), (3, 1)])

    def test_dijkstra_returns_empty_history_when_not_logging(self):
        _, history = dijkstra.dijkstra(Grid("SG"), logging=False)
        self.assertIsNone(history.advance_step())

    def test_dijkstra_on_a_grid_with_no_path_to_goal_returns_None_as_goal_node(self):
        goal, _ = dijkstra.dijkstra(Grid("S#G"))
        self.assertIsNone(goal)

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
        goal, history = dijkstra.dijkstra(Grid(grid))
        path_length = calculate_path_length(goal.path_from_start())
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

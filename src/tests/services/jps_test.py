import math
import unittest
from entities.grid import Grid
from services.jps import JPS


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        simple_test_grid = Grid("""
        ####
        S..G
        ##.#
        """)
        self.jps = JPS(simple_test_grid)

    def test_simple_test_path_to_goal_is_correct(self):
        path = self.jps.run()
        self.assertEqual(path, [(0, 1), (1, 1), (2, 1), (3, 1)])

    def test_next_step_gen_yields_none_when_not_using_step_info(self):
        self.jps._generate_step_info = False
        next_step_gen = self.jps.next_step()
        self.assertIsNone(next_step_gen.__next__())

    def test_jps_on_a_grid_with_no_path_to_goal_returns_empty_list_as_path(self):
        jps = JPS(Grid("S#G"))
        path = jps.run()
        self.assertEqual(len(path), 0)

    def test_jps_complex_path_length_is_correct(self):
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
        jps = JPS(Grid(grid))
        path = jps.run()
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

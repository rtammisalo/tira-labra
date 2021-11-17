import unittest
from entities.grid import Grid
from entities.graph import Graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.grid = Grid("""
        #..#
        S##G
        .#.#
        #.##
        """)
        self.graph = Graph(self.grid)

    def test_get_start_node_returns_the_starting_node(self):
        start_node = self.graph.get_start_node()
        self.assertEqual(start_node.pos, (0, 1))

    def test_get_goal_node_returns_the_goal_node(self):
        goal_node = self.graph.get_goal_node()
        self.assertEqual(goal_node.pos, (3, 1))

    def test_get_node_returns_the_node_representing_non_wall_grid_position(self):
        node = self.graph.get_node((1, 0))
        self.assertEqual(node.pos, (1, 0))

    def test_get_node_returns_none_on_wall_grid_positions(self):
        node = self.graph.get_node((0, 0))
        self.assertIsNone(node)

    def test_get_node_returns_none_on_out_of_grid_positions(self):
        node = self.graph.get_node((-1, 0))
        self.assertIsNone(node)

    def test_get_nodes_returns_all_nodes_representing_non_wall_grid_positions(self):
        nodes = self.graph.get_nodes()
        self.assertEqual(len(nodes), 7)
        grid_positions = []
        for node in nodes:
            grid_positions.append(node.pos)
        self.assertCountEqual(
            grid_positions, [(1, 0), (2, 0), (0, 1), (3, 1), (0, 2), (2, 2), (1, 3)])

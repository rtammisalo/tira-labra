import unittest
from entities.jps_node import JPSNode
from entities.grid import Grid


class StubGraph:
    def __init__(self, grid_list):
        self.grid = grid_list

    def get_node(self, pos):
        return self.grid[pos[1]][pos[0]]


class TestJPSNode(unittest.TestCase):
    def setUp(self):
        self.graph = StubGraph([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.pos = (1, 1)
        self.node = JPSNode(self.pos, self.graph)

    def test_get_node_in_up_direction_returns_upper_node(self):
        number = self.node.get_node_in_direction(Grid.UP)
        self.assertEqual(number, 2)

    def test_get_node_in_left_direction_returns_left_node(self):
        number = self.node.get_node_in_direction(Grid.LEFT)
        self.assertEqual(number, 4)

    def test_get_node_in_NE_direction_returns_NE_node(self):
        number = self.node.get_node_in_direction(Grid.NE)
        self.assertEqual(number, 3)

    def test_get_node_in_SW_direction_returns_SW_node(self):
        number = self.node.get_node_in_direction(Grid.SW)
        self.assertEqual(number, 7)

    def test_get_cardinal_expansion_directions_returns_correct_cardinal_directions(self):
        directions = self.node.get_cardinal_expansion_directions(Grid.NE)
        self.assertCountEqual(directions, [Grid.UP, Grid.RIGHT])

    def test_get_cardinal_expansion_directions_returns_an_empty_list_for_cardinal_expansion(self):
        directions = self.node.get_cardinal_expansion_directions(Grid.RIGHT)
        self.assertCountEqual(directions, [])

    def test_diagonal_pruned_neighbor_directions_returns_correct_neighbors_when_none_forced(self):
        directions = list(self.node.iter_pruned_neighbor_directions(Grid.NE))
        self.assertCountEqual(directions, [Grid.UP, Grid.NE, Grid.RIGHT])
        directions = list(self.node.iter_pruned_neighbor_directions(Grid.SE))
        self.assertCountEqual(directions, [Grid.DOWN, Grid.SE, Grid.RIGHT])
        directions = list(self.node.iter_pruned_neighbor_directions(Grid.SW))
        self.assertCountEqual(directions, [Grid.DOWN, Grid.SW, Grid.LEFT])
        directions = list(self.node.iter_pruned_neighbor_directions(Grid.NW))
        self.assertCountEqual(directions, [Grid.UP, Grid.NW, Grid.LEFT])

    def test_cardinal_pruned_neighbor_directions_returns_correct_neighbors_when_none_forced(self):
        directions = list(self.node.iter_pruned_neighbor_directions(Grid.UP))
        self.assertCountEqual(directions, [Grid.UP])
        directions = list(
            self.node.iter_pruned_neighbor_directions(Grid.RIGHT))
        self.assertCountEqual(directions, [Grid.RIGHT])
        directions = list(self.node.iter_pruned_neighbor_directions(Grid.DOWN))
        self.assertCountEqual(directions, [Grid.DOWN])
        directions = list(self.node.iter_pruned_neighbor_directions(Grid.LEFT))
        self.assertCountEqual(directions, [Grid.LEFT])

    def test_diagonal_pruned_neighbor_directions_returns_correct_neighbors_with_forced(self):
        graph = StubGraph([[1, 2, 3], [None, 5, 6], [7, 8, 9]])
        node = JPSNode(self.pos, graph)
        directions = list(node.iter_pruned_neighbor_directions(Grid.NE))
        self.assertCountEqual(
            directions, [Grid.NW, Grid.UP, Grid.NE, Grid.RIGHT])

        graph = StubGraph([[1, 2, 3], [4, 5, 6], [7, None, 9]])
        node = JPSNode(self.pos, graph)
        directions = list(node.iter_pruned_neighbor_directions(Grid.NE))
        self.assertCountEqual(
            directions, [Grid.SE, Grid.UP, Grid.NE, Grid.RIGHT])

        graph = StubGraph([[1, 2, 3], [None, 5, 6], [7, None, 9]])
        node = JPSNode(self.pos, graph)
        directions = list(node.iter_pruned_neighbor_directions(Grid.NE))
        self.assertCountEqual(
            directions, [Grid.NW, Grid.UP, Grid.NE, Grid.RIGHT, Grid.SE])

    def test_cardinal_pruned_neighbor_directions_returns_correct_neighbors_with_forced(self):
        graph = StubGraph([[1, None, 3], [4, 5, 6], [7, 8, 9]])
        node = JPSNode(self.pos, graph)
        directions = list(node.iter_pruned_neighbor_directions(Grid.RIGHT))
        self.assertCountEqual(
            directions, [Grid.NE, Grid.RIGHT])

        graph = StubGraph([[1, 2, 3], [4, 5, 6], [7, None, 9]])
        node = JPSNode(self.pos, graph)
        directions = list(node.iter_pruned_neighbor_directions(Grid.RIGHT))
        self.assertCountEqual(
            directions, [Grid.SE, Grid.RIGHT])

        graph = StubGraph([[1, None, 3], [4, 5, 6], [7, None, 9]])
        node = JPSNode(self.pos, graph)
        directions = list(node.iter_pruned_neighbor_directions(Grid.RIGHT))
        self.assertCountEqual(
            directions, [Grid.NE, Grid.RIGHT, Grid.SE])

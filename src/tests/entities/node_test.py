import unittest
from entities.node import Node


class StubGraph():
    def __init__(self):
        self.nodes = {}

    def get_node(self, pos):
        if pos in self.nodes:
            return self.nodes[pos]
        return None

    def create_node(self, pos):
        self.nodes[pos] = Node(pos, self)
        return self.nodes[pos]


class TestNode(unittest.TestCase):
    def setUp(self):
        self.graph = StubGraph()
        self.node_a = self.graph.create_node((0, 0))
        self.node_b = self.graph.create_node((1, 0))
        self.node_c = self.graph.create_node((0, 1))
        self.node_start = self.graph.create_node((0, 2))
        self.node_goal = self.graph.create_node((2, 0))
        self.node_alone = self.graph.create_node((10, 10))
        self.node_goal.previous = self.node_b
        self.node_b.previous = self.node_c
        self.node_c.previous = self.node_start

    def test_get_neighbors_returns_list_of_neighbors(self):
        neighbors = self.node_a.get_neighbors()
        self.assertEqual(len(neighbors), 2)
        self.assertTrue(self.node_b in [node for node, weight in neighbors])
        self.assertTrue(self.node_c in [node for node, weight in neighbors])

    def test_get_neighbors_returns_empty_list_when_node_has_no_neighbors(self):
        self.assertEqual(len(self.node_alone.get_neighbors()), 0)

    def test_path_from_start_to_goal_is_correct(self):
        correct_path = [(0, 2), (0, 1), (1, 0), (2, 0)]
        self.assertEqual(self.node_goal.path_from_start(), correct_path)

    def test_unvisited_nodes_return_empty_list_as_path_from_start(self):
        correct_path = []
        self.assertEqual(self.node_alone.path_from_start(), correct_path)

    def test_nodes_with_a_number_as_distance_are_lesser_than_default_distance_nodes(self):
        test_node = Node((11,11), self.graph)
        test_node.distance = 1
        self.assertTrue(test_node < self.node_a)

    def test_nodes_are_considered_equal_if_the_position_coordinates_match(self):
        test_node_a = Node((0,0), self.graph)
        self.assertTrue(test_node_a == self.node_a)
    
    def test_nodes_are_considered_not_same_if_the_position_coordinates_mismatch(self):
        self.assertTrue(self.node_a != self.node_b)

    def test_node_equality_compared_to_non_nodes_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.assertTrue(self.node_a != 'a')
    
    def test_nodes_return_string_representation_of_correct_default_values(self):
        correct_str = "Node at (0, 0), distance of inf, previous node set to None"
        self.assertEqual(str(self.node_a), correct_str)
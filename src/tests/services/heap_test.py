import unittest
from services.heap import Heap
from entities.node import Node


class TestHeap(unittest.TestCase):
    def setUp(self):
        self.node_a = Node((0, 0), None)
        self.node_b = Node((1, 1), None)
        self.node_c = Node((2, 2), None)
        self.node_d = Node((3, 3), None)
        self.node_a.distance = 1
        self.node_b.distance = 2
        self.node_c.distance = 3
        self.heap = Heap([self.node_a, self.node_b, self.node_c, self.node_d])

    def test_pop_node_returns_smallest_distance_node(self):
        node = self.heap.pop_node()
        self.assertEqual(node.distance, 1)

    def test_pop_node_removes_node_from_heap(self):
        self.heap.pop_node()
        self.assertEqual(len(self.heap._heap), 3)

    def test_pop_node_on_empty_heap_returns_None(self):
        empty_heap = Heap([])
        self.assertEqual(empty_heap.pop_node(), None)

    def test_pop_node_returns_new_smallest_distance_node_pushed(self):
        new_node = Node((10, 10), None)
        new_node.distance = 0.5
        self.heap.push_node(new_node)
        self.assertAlmostEqual(self.heap.pop_node().distance, 0.5)

    def test_pop_node_returns_smallest_distance_node_after_pushing_large_dist_node(self):
        new_large_node = Node((10, 10), None)
        new_large_node.distance = 10
        self.heap.push_node(new_large_node)
        self.assertEqual(self.heap.pop_node().distance, 1)

    def test_updating_node_distance_changes_heap(self):
        self.heap.update_node(self.node_a, 4)
        self.assertEqual(self.heap.pop_node().distance, 2)
        self.assertEqual(self.heap.pop_node().distance, 3)
        self.assertEqual(self.heap.pop_node().distance, 4)

    def test_is_empty_returns_true_on_empty_heaps(self):
        empty = Heap([])
        self.assertTrue(empty.is_empty())

    def test_is_empty_returns_false_on_heaps_with_nodes(self):
        self.assertFalse(self.heap.is_empty())

    def test_is_empty_returns_true_on_heaps_emptied_with_pop_node(self):
        self.heap.pop_node()
        self.heap.pop_node()
        self.heap.pop_node()
        self.heap.pop_node()
        self.assertTrue(self.heap.is_empty())

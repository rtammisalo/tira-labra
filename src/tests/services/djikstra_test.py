import math
import unittest
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.heap import Heap
from services.math_utils import calculate_path_cost, octile_distance
import tests.services.test_maps as maps


def get_path_cost(map_string):
    grid = Grid(map_string)
    path = Dijkstra(grid).run()
    return calculate_path_cost(path), path


def set_up_dijkstra(map_string):
    grid = Grid(map_string)
    heap = Heap()
    dijkstra = Dijkstra(grid, heap)
    dijkstra_gen = dijkstra.next_step()
    return grid, heap, dijkstra, dijkstra_gen


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        grid, heap, dijkstra, dijkstra_gen = set_up_dijkstra(maps.SPARSE_MAP)
        self.grid = grid
        self.heap = heap
        self.dijkstra = dijkstra
        self.dijkstra_gen = dijkstra_gen

    def test_simple_grid_path_cost_matches_actual_distance(self):
        dijkstra_cost, path = get_path_cost(maps.SIMPLE_MAP)
        self.assertAlmostEqual(dijkstra_cost, maps.SIMPLE_MAP_DISTANCE)

    def test_dijkstra_finds_no_path_on_no_path_map(self):
        grid = Grid(maps.NO_PATH_MAP)
        path = Dijkstra(grid).run()
        self.assertEqual(len(path), 0)

    def test_dijkstra_finds_no_path_on_no_start_neighbors_map(self):
        grid = Grid(maps.NO_START_NEIGHBORS_MAP)
        path = Dijkstra(grid).run()
        self.assertEqual(len(path), 0)

    def test_two_way_box_map_path_cost_matches_actual_distance(self):
        dijkstra_cost, path = get_path_cost(maps.TWO_WAY_BOX_MAP)
        self.assertAlmostEqual(dijkstra_cost, maps.TWO_WAY_BOX_MAP_DISTANCE)

    def test_complex_map_path_cost_matches_actual_distance(self):
        dijkstra_cost, path = get_path_cost(maps.COMPLEX_MAP)
        self.assertAlmostEqual(dijkstra_cost, maps.COMPLEX_MAP_DISTANCE)

    def test_big_l_map_path_cost_matches_actual_distance(self):
        dijkstra_cost, path = get_path_cost(maps.BIG_L_MAP)
        self.assertAlmostEqual(dijkstra_cost, maps.BIG_L_MAP_DISTANCE)

    def test_sparse_map_path_cost_matches_actual_distance(self):
        dijkstra_cost, path = get_path_cost(maps.SPARSE_MAP)
        self.assertAlmostEqual(dijkstra_cost, maps.SPARSE_MAP_DISTANCE)

    def test_heap_should_not_contain_visited_nodes_with_less_distance_than_actual(self):
        for i in range(100):
            self.dijkstra_gen.__next__()
        start = self.dijkstra.graph.get_start_node()
        heap_contents = self.heap.get_heap_contents()
        for distance, heap_node in heap_contents:
            if heap_node.visited:
                actual_distance = octile_distance(heap_node, start)
                self.assertLessEqual(actual_distance, distance)

    def test_closest_nodes_after_25_gen_calls_should_be_the_nodes_straight_from_start(self):
        for i in range(25):
            self.dijkstra_gen.__next__()
        # Start node at (45,3)
        next_node = self.heap.pop_node()
        self.assertIn(next_node.pos, [(42, 3), (48, 3), (45, 6), (45, 0)])
        next_node = self.heap.pop_node()
        self.assertIn(next_node.pos, [(42, 3), (48, 3), (45, 6), (45, 0)])
        next_node = self.heap.pop_node()
        self.assertIn(next_node.pos, [(42, 3), (48, 3), (45, 6), (45, 0)])
        next_node = self.heap.pop_node()
        self.assertIn(next_node.pos, [(42, 3), (48, 3), (45, 6), (45, 0)])

    def test_next_generator_call_stops_iteration_when_goal_is_the_lowest_node_in_the_heap(self):
        heap_node = None
        goal_node = self.dijkstra.graph.get_goal_node()
        for visited, visible in self.dijkstra_gen:
            if visited != goal_node:
                heap_node = self.heap.peek_node()
        self.assertEqual(heap_node, goal_node)

    def test_all_nodes_should_be_in_the_heap_at_start_with_inf_distance(self):
        start = self.dijkstra.graph.get_start_node()
        for distance, node in self.heap.get_heap_contents():
            if node == start:
                # Should be twice in the heap at start.
                self.assertIn(distance, [0, float('inf')])
                self.assertIn(node.distance, [0, float('inf')])
            else:
                self.assertEqual(distance, float('inf'))
                self.assertEqual(node.distance, float('inf'))

    def test_simple_test_next_steps_return_correct_visited_and_visible_nodes(self):
        grid, heap, dijkstra, dijkstra_gen = set_up_dijkstra(maps.SIMPLE_MAP)

        visited_node, visible_nodes = dijkstra_gen.__next__()
        self.assertEqual(visited_node.pos, (0, 1))
        self.assertEqual(list_positions(visible_nodes), [(1, 1)])

        visited_node, visible_nodes = dijkstra_gen.__next__()
        self.assertEqual(visited_node.pos, (1, 1))
        self.assertCountEqual(list_positions(visible_nodes), [(2, 1), (2, 2)])

        visited_node, visible_nodes = dijkstra_gen.__next__()
        self.assertEqual(visited_node.pos, (2, 1))
        self.assertCountEqual(list_positions(visible_nodes), [(2, 2), (3, 1)])

    def test_on_sparse_map_dijkstra_should_visit_more_than_90_percent_of_nodes(self):
        self.dijkstra.run()
        all_nodes = self.dijkstra.graph.get_nodes()
        visited_nodes_sum = sum([node.visited for node in all_nodes])
        self.assertGreater(visited_nodes_sum, 0.90 * len(all_nodes))

    def test_dijkstra_should_return_as_visited_all_nodes_marked_as_visited(self):
        visited_nodes = []
        for visited, visible_nodes in self.dijkstra_gen:
            visited_nodes.append(visited)
        for node in self.dijkstra.graph.get_nodes():
            if node.visited:
                self.assertIn(node, visited_nodes)


def list_positions(nodes):
    return [node.pos for node in nodes]

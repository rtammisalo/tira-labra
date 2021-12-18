import math
import unittest
from entities.grid import Grid
from services.ida_star import IDAStar
from services.math_utils import calculate_path_cost, octile_distance, octile_distance_pos
import tests.services.test_maps as maps


def get_path_cost(map_string):
    grid = Grid(map_string)
    path = IDAStar(grid).run()
    return calculate_path_cost(path), path


def set_up_IDAStar(map_string):
    grid = Grid(map_string)
    ida = IDAStar(grid)
    ida_gen = ida.next_step()
    return grid, ida, ida_gen


class TestIDAStar(unittest.TestCase):
    def test_simple_grid_path_cost_matches_actual_distance(self):
        ida_cost, path = get_path_cost(maps.SIMPLE_MAP)
        self.assertAlmostEqual(ida_cost, maps.SIMPLE_MAP_DISTANCE)

    def test_IDAStar_finds_no_path_on_no_path_map(self):
        grid = Grid(maps.NO_PATH_MAP)
        path = IDAStar(grid).run()
        self.assertEqual(len(path), 0)

    def test_IDAStar_finds_no_path_on_no_start_neighbors_map(self):
        grid = Grid(maps.NO_START_NEIGHBORS_MAP)
        path = IDAStar(grid).run()
        self.assertEqual(len(path), 0)

    def test_two_way_box_map_path_cost_matches_actual_distance(self):
        ida_cost, path = get_path_cost(maps.TWO_WAY_BOX_MAP)
        self.assertAlmostEqual(ida_cost, maps.TWO_WAY_BOX_MAP_DISTANCE)

    def test_complex_map_path_cost_matches_actual_distance(self):
        ida_cost, path = get_path_cost(maps.COMPLEX_MAP)
        self.assertAlmostEqual(ida_cost, maps.COMPLEX_MAP_DISTANCE)

    def test_big_l_map_path_cost_matches_actual_distance(self):
        ida_cost, path = get_path_cost(maps.BIG_L_MAP)
        self.assertAlmostEqual(ida_cost, maps.BIG_L_MAP_DISTANCE)

    def test_sparse_map_path_cost_matches_actual_distance(self):
        ida_cost, path = get_path_cost(maps.SPARSE_MAP)
        self.assertAlmostEqual(ida_cost, maps.SPARSE_MAP_DISTANCE)

    def test_no_iterative_path_can_cross_over_itself(self):
        grid, ida, ida_gen = set_up_IDAStar(maps.TWO_WAY_BOX_MAP)
        for visited_nodes, iterative_paths in ida_gen:
            for path in iterative_paths:
                positions = set()
                for pos in path:
                    self.assertNotIn(pos, positions)
                    positions.add(pos)

    def test_no_iterative_path_goes_outside_visited_nodes(self):
        grid, ida, ida_gen = set_up_IDAStar(maps.TWO_WAY_BOX_MAP)
        visited_positions = set()
        for visited_nodes, iterative_paths in ida_gen:
            visited_positions = visited_positions.union(
                [node.pos for node in visited_nodes])
            for path in iterative_paths:
                for pos in path:
                    self.assertIn(pos, visited_positions)

    def test_no_iterative_path_costs_more_than_the_bound(self):
        grid, ida, ida_gen = set_up_IDAStar(maps.TWO_WAY_BOX_MAP)
        for visited_nodes, iterative_paths in ida_gen:
            bound = ida._bound

            for path in iterative_paths:
                path_cost = calculate_path_cost(path[:-1])
                if not math.isclose(path_cost, bound):
                    self.assertLessEqual(path_cost, bound)

    def test_no_visited_node_is_farther_away_than_the_bound(self):
        grid, ida, ida_gen = set_up_IDAStar(maps.TWO_WAY_BOX_MAP)
        start_node = ida.graph.get_start_node()

        for visited_nodes, iterative_paths in ida_gen:
            bound = ida._bound
            for node in visited_nodes:
                min_cost = octile_distance(node, start_node)
                self.assertLessEqual(min_cost, bound)

    def test_all_visited_nodes_neighbor_other_visited_nodes(self):
        grid, ida, ida_gen = set_up_IDAStar(maps.TWO_WAY_BOX_MAP)
        start_node = ida.graph.get_start_node()

        for visited_nodes, iterative_paths in ida_gen:
            for node in visited_nodes:
                if node == start_node:
                    continue
                neighbors_in_visited = False
                for neighbor, _ in node.get_neighbors():
                    if neighbor in visited_nodes:
                        neighbors_in_visited = True
                        break
                self.assertTrue(neighbors_in_visited)

    def test_bound_increases_by_minimum_cost(self):
        grid_str = \
            """
            ##..
            S..#
            ####
            G###
            """
        grid, ida, ida_gen = set_up_IDAStar(grid_str)

        for i in range(3):
            ida_gen.__next__()

        self.assertEqual(ida._bound, 2 + octile_distance_pos((2, 1), (0, 3)))
        ida_gen.__next__()
        self.assertEqual(ida._bound, 1 + math.sqrt(2) +
                         octile_distance_pos((2, 0), (0, 3)))

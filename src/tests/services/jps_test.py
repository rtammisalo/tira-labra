import unittest
from entities.grid import Grid
from services.jps import JPS
from services.heap import Heap
from services.math_utils import octile_distance, calculate_path_cost
import tests.services.test_maps as maps


def get_path_cost(map_string):
    grid = Grid(map_string)
    path = JPS(grid).run()
    return calculate_path_cost(path), path


def set_up_JPS(map_string):
    grid = Grid(map_string)
    heap = Heap()
    jps = JPS(grid, heap)
    jps_gen = jps.next_step()
    return grid, heap, jps, jps_gen


class TestJPS(unittest.TestCase):
    def setUp(self):
        grid, heap, jps, jps_gen = set_up_JPS(maps.SPARSE_MAP)
        self.grid = grid
        self.heap = heap
        self.jps = jps
        self.jps_gen = jps_gen

    def test_simple_grid_path_cost_matches_actual_distance(self):
        cost, path = get_path_cost(maps.SIMPLE_MAP)
        self.assertAlmostEqual(cost, maps.SIMPLE_MAP_DISTANCE)

    def test_JPS_finds_no_path_on_no_path_map(self):
        grid = Grid(maps.NO_PATH_MAP)
        path = JPS(grid).run()
        self.assertEqual(len(path), 0)

    def test_JPS_finds_no_path_on_no_start_neighbors_map(self):
        grid = Grid(maps.NO_START_NEIGHBORS_MAP)
        path = JPS(grid).run()
        self.assertEqual(len(path), 0)

    def test_two_way_box_map_path_cost_matches_actual_distance(self):
        jps_cost, path = get_path_cost(maps.TWO_WAY_BOX_MAP)
        self.assertAlmostEqual(jps_cost, maps.TWO_WAY_BOX_MAP_DISTANCE)

    def test_complex_map_path_cost_matches_actual_distance(self):
        jps_cost, path = get_path_cost(maps.COMPLEX_MAP)
        self.assertAlmostEqual(jps_cost, maps.COMPLEX_MAP_DISTANCE)

    def test_big_l_map_path_cost_matches_actual_distance(self):
        jps_cost, path = get_path_cost(maps.BIG_L_MAP)
        self.assertAlmostEqual(jps_cost, maps.BIG_L_MAP_DISTANCE)

    def test_sparse_map_path_cost_matches_actual_distance(self):
        jps_cost, path = get_path_cost(maps.SPARSE_MAP)
        self.assertAlmostEqual(jps_cost, maps.SPARSE_MAP_DISTANCE)

    def test_heap_should_not_contain_visited_nodes_with_less_distance_than_actual(self):
        for i in range(10):
            self.jps_gen.__next__()
        start = self.jps.graph.get_start_node()
        heap_contents = self.heap.get_heap_contents()
        for distance, heap_node in heap_contents:
            if heap_node.visited:
                actual_distance = octile_distance(heap_node, start)
                self.assertLessEqual(actual_distance, distance)

    def _jump_identifies_new_jump_points_and_expands_correctly(self, grid_str, jump_points,
                                                               look_ahead_points):
        """
        A helper function to check for jump points and look ahead points.
        """
        grid, heap, jps, jps_gen = set_up_JPS(grid_str)
        start = jps.graph.get_start_node()
        jump_points.append(start.pos)
        look_aheads_seen = []
        jump_points_seen = []
        jump_points_visited = []

        for visited_node, jump_point_nodes, look_ahead_nodes in jps_gen:
            jump_points_visited.append(visited_node)
            jump_points_seen.extend(jump_point_nodes)
            look_aheads_seen.extend(look_ahead_nodes)

        # We should look for all the look ahead points described in the method argument
        # in the returned look ahead nodes.
        look_ahead_points_found = 0
        for look_ahead_point in look_ahead_points:
            for look_ahead_seen, _ in look_aheads_seen:
                if look_ahead_point == look_ahead_seen.pos:
                    look_ahead_points_found += 1
        self.assertEqual(look_ahead_points_found, len(look_ahead_points))

        # We should be able to find all nodes marked as visited in the jump_points arg.
        jump_points_found = 0
        for node in jps.graph.get_nodes():
            if node.visited:
                self.assertIn(node.pos, jump_points)
                jump_points_found += 1
        self.assertEqual(jump_points_found, len(jump_points))

        # Sanity check: see if the algorithm claims to have actually visited all
        # jump points as well.
        jump_points_seen.append(start)
        self.assertEqual(len(jump_points_visited), len(jump_points_seen))

    def test_jumping_left_correctly_identifies_upper_jump_point(self):
        grid_str = \
            """
            ####.##
            G#....S
            #######
            """
        jump_points = [(5, 1)]
        look_ahead_points = [(4, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_left_correctly_identifies_lower_jump_point(self):
        grid_str = \
            """
            #######
            G#....S
            ####.##
            """
        jump_points = [(5, 1)]
        look_ahead_points = [(4, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_left_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            ####.##
            G#....S
            ####.##
            """
        jump_points = [(5, 1)]
        look_ahead_points = [(4, 0), (4, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_right_correctly_identifies_upper_jump_point(self):
        grid_str = \
            """
            ##.###
            S...#G
            ######
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_right_correctly_identifies_lower_jump_point(self):
        grid_str = \
            """
            ##.###
            S...#G
            ######
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_right_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            ##.###
            S...#G
            ##.###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 0), (2, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_up_correctly_identifies_left_jump_point(self):
        grid_str = \
            """
            ..###
            #.##G
            #S###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_up_correctly_identifies_right_jump_point(self):
        grid_str = \
            """
            #..##
            #.##G
            #S###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_up_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            ...##
            #.##G
            #S###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 0), (2, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_down_correctly_identifies_left_jump_point(self):
        grid_str = \
            """
            #S###
            #.##G
            ..###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_down_correctly_identifies_right_jump_point(self):
        grid_str = \
            """
            #S###
            #.##G
            #..##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_down_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            #S###
            #.##G
            ...##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 2), (2, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_NE_correctly_identifies_NW_jump_point(self):
        grid_str = \
            """
            ..###
            #.##G
            S.###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_NE_correctly_identifies_SE_jump_point(self):
        grid_str = \
            """
            #.###
            #.##G
            S#.##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_NE_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            ..###
            #.##G
            S#.##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 2), (0, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_SE_correctly_identifies_SW_jump_point(self):
        grid_str = \
            """
            S.###
            #.##G
            ..###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_SE_correctly_identifies_NE_jump_point(self):
        grid_str = \
            """
            S#.##
            #.##G
            #.###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_SE_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            S#.##
            #.##G
            ..###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 0), (0, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_SW_correctly_identifies_NW_jump_point(self):
        grid_str = \
            """
            .#S##
            #.##G
            ..###
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_SW_correctly_identifies_SE_jump_point(self):
        grid_str = \
            """
            ##S##
            #.##G
            ...##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_SW_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            .#S##
            #.##G
            ...##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 0), (2, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_NW_correctly_identifies_NW_jump_point(self):
        grid_str = \
            """
            ..###
            #.##G
            .#S##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 2)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_NW_correctly_identifies_NE_jump_point(self):
        grid_str = \
            """
            ...##
            #.##G
            ##S##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(2, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_jumping_NW_correctly_identifies_both_jump_points(self):
        grid_str = \
            """
            ...##
            #.##G
            .#S##
            """
        jump_points = [(1, 1)]
        look_ahead_points = [(0, 2), (2, 0)]
        self._jump_identifies_new_jump_points_and_expands_correctly(
            grid_str, jump_points, look_ahead_points)

    def test_on_sparse_map_JPS_puts_less_than_10_percent_of_all_graph_nodes_in_heap(self):
        grid, heap, jps, jps_gen = set_up_JPS(maps.SPARSE_MAP)
        all_jump_points = set()
        for visited_node, visible_nodes, look_ahead_nodes in jps_gen:
            all_jump_points.add(visited_node.pos)
            for node in visible_nodes:
                all_jump_points.add(node.pos)
        self.assertLess(len(all_jump_points), 0.1 * len(jps.graph.get_nodes()))

    def test_JPS_puts_only_visible_nodes_in_heap(self):
        grid, heap, jps, jps_gen = set_up_JPS(maps.SPARSE_MAP)
        once_visibles = []
        for visited_node, visible_nodes, look_ahead_nodes in jps_gen:
            once_visibles.extend(visible_nodes)
            heap_nodes = [heap_node for dist,
                          heap_node in heap.get_heap_contents()]
            for visible_node in visible_nodes:
                self.assertIn(visible_node, heap_nodes)
            for heap_node in heap_nodes:
                if heap_node != jps.graph.get_start_node():
                    self.assertIn(heap_node, once_visibles)

    def test_on_sparse_map_JPS_jumps_over_more_than_80_percent_of_all_graph_nodes(self):
        grid, heap, jps, jps_gen = set_up_JPS(maps.SPARSE_MAP)
        all_look_aheads = set()
        for visited_node, visible_nodes, look_ahead_nodes in jps_gen:
            all_look_aheads = all_look_aheads.union(
                [node.pos for node, direction in look_ahead_nodes])
        self.assertGreater(len(all_look_aheads), 0.8 *
                           len(jps.graph.get_nodes()))

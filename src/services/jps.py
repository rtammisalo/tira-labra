import math
from entities.graph import Graph
from entities.grid import Grid
from services.heap import Heap


class JPS():
    # Running into these points while looking ahead can cause forced neighbors.
    # Dict key is the expanding direction, values are a list of (blocked, free) tuples
    # stored as relative directions to the inspected node position.
    BLOCKED_FREE_PAIRS = {Grid.UP: [(Grid.LEFT, Grid.NW), (Grid.RIGHT, Grid.NE)],
                          Grid.RIGHT: [(Grid.UP, Grid.NE), (Grid.DOWN, Grid.SE)],
                          Grid.DOWN: [(Grid.LEFT, Grid.SW), (Grid.RIGHT, Grid.SE)],
                          Grid.LEFT: [(Grid.UP, Grid.NW), (Grid.DOWN, Grid.SW)],
                          Grid.NE: [(Grid.LEFT, Grid.NW), (Grid.DOWN, Grid.SE)],
                          Grid.SE: [(Grid.LEFT, Grid.SW), (Grid.UP, Grid.NE)],
                          Grid.SW: [(Grid.UP, Grid.NW), (Grid.RIGHT, Grid.SE)],
                          Grid.NW: [(Grid.DOWN, Grid.SW), (Grid.RIGHT, Grid.NE)]}

    EXPANSION_DIRECTIONS = {Grid.UP: [Grid.UP],
                            Grid.RIGHT: [Grid.RIGHT],
                            Grid.DOWN: [Grid.DOWN],
                            Grid.LEFT: [Grid.LEFT],
                            Grid.NE: [Grid.UP, Grid.NE, Grid.RIGHT],
                            Grid.SE: [Grid.DOWN, Grid.SE, Grid.RIGHT],
                            Grid.SW: [Grid.DOWN, Grid.SW, Grid.LEFT],
                            Grid.NW: [Grid.UP, Grid.NW, Grid.LEFT]}

    def __init__(self, grid):
        self._grid = grid
        self._graph = Graph(grid)
        self._open_nodes_by_distance = Heap([])
        self._expanded_nodes = []
        self._visible_nodes = []
        self._generate_step_info = True

    def run(self):
        try:
            self._generate_step_info = False
            generator = self.next_step()
            while True:
                generator.__next__()
        except StopIteration as stop:
            return stop.value

    def next_step(self):
        start_node = self._init_start_node()
        self._expand_start_node(start_node)
        if self._generate_step_info:
            yield start_node, self._visible_nodes, self._expanded_nodes

        while not self._open_nodes_by_distance.is_empty():
            current_node = self._open_nodes_by_distance.pop_node()
            self._expanded_nodes = []
            self._visible_nodes = []

            additional_expanding_directions = self._find_forced_neighbor_node_directions(
                current_node, current_node.direction)
            for direction in additional_expanding_directions:
                self._expand_in_direction(
                    current_node, direction, current_node.travel_cost)

            for direction in self.EXPANSION_DIRECTIONS[current_node.direction]:
                self._expand_in_direction(
                    current_node, direction, current_node.travel_cost)

            if self._generate_step_info:
                yield current_node, self._visible_nodes, self._expanded_nodes
            else:
                yield None

            if self._graph.get_goal_node().visited:
                return self._create_path_to_goal()

        return []

    def _reverse_direction(self, direction):
        return tuple(map(lambda coord: -1 * coord, direction))

    def _create_path_to_goal(self):
        node = self._graph.get_goal_node()
        start_node = self._graph.get_start_node()
        path_to_goal = [node.pos]

        while node != start_node:
            from_direction = self._reverse_direction(node.direction)
            node = self._get_node_in_direction(node, from_direction)
            path_to_goal.append(node.pos)
            while not node.visited:
                node = self._get_node_in_direction(node, from_direction)
                path_to_goal.append(node.pos)

        path_to_goal.reverse()
        return path_to_goal

    def _handle_found_goal_node(self, direction, cost):
        goal_node = self._graph.get_goal_node()
        goal_node.total_cost = cost
        goal_node.distance = cost
        goal_node.direction = direction
        goal_node.visited = True

    def _handle_forced_neighbors(self, node, expanding_direction, cost):
        if node.visited:
            return

        if self._is_interest_node(node, expanding_direction):
            old_distance = node.distance
            new_distance = cost + self._heuristic(node)

            if new_distance < old_distance:
                node.distance = new_distance
                node.travel_cost = cost
                node.direction = expanding_direction
                if old_distance == float('inf'):
                    self._open_nodes_by_distance.push_node(node)
                else:
                    self._open_nodes_by_distance.decrease_distance(
                        node, new_distance)

                self._visible_nodes.append(node)

    def _is_interest_node(self, node, expanding_direction):
        if self._find_forced_neighbor_node_directions(node, expanding_direction):
            return True

        return False

    def _find_forced_neighbor_node_directions(self, node, expanding_direction):
        additional_expanding_directions = []

        for blocked_dir, free_dir in self.BLOCKED_FREE_PAIRS[expanding_direction]:
            blocked_node = self._get_node_in_direction(node, blocked_dir)
            free_node = self._get_node_in_direction(node, free_dir)
            if free_node and free_node.distance < float('inf'):
                free_node = None
            if not blocked_node and free_node:
                additional_expanding_directions.append(free_dir)

        return additional_expanding_directions

    def _expand_in_direction(self, original_node, direction, cost):
        if direction in Grid.CARDINAL_DIRECTIONS:
            self._expand_in_cardinal_direction(original_node, direction, cost)
        else:
            self._expand_in_diagonal_direction(original_node, direction, cost)

    def _expand_in_cardinal_direction(self, origin_node, direction, cost):
        old_cost = cost
        next_node = origin_node

        while True:
            cost += 1
            next_node = self._get_node_in_direction(next_node, direction)

            if not next_node:
                return False

            if self._generate_step_info:
                self._expanded_nodes.append((next_node, direction))

            if next_node == self._graph.get_goal_node():
                self._handle_found_goal_node(direction, cost)
                return True

            if self._is_interest_node(next_node, direction):
                self._handle_forced_neighbors(next_node, direction, cost)
                return True

    def _expand_in_diagonal_direction(self, origin_node, direction, cost):
        old_cost = cost
        next_node = origin_node

        while True:
            cost += math.sqrt(2)
            next_node = self._get_node_in_direction(next_node, direction)

            if not next_node:
                break

            if self._generate_step_info:
                self._expanded_nodes.append((next_node, direction))

            if next_node == self._graph.get_goal_node():
                self._handle_found_goal_node(direction, cost)
                break

            if self._is_interest_node(next_node, direction):
                self._handle_forced_neighbors(next_node, direction, cost)
                break

            extra_cardinal_directions = []
            found_cardinal_expansion_interest = False
            if direction[0] > 0:
                extra_cardinal_directions.append(Grid.RIGHT)
            else:
                extra_cardinal_directions.append(Grid.LEFT)

            if direction[1] > 0:
                extra_cardinal_directions.append(Grid.DOWN)
            else:
                extra_cardinal_directions.append(Grid.UP)

            for expand_direction in self.EXPANSION_DIRECTIONS[direction]:
                if expand_direction in Grid.DIAGONAL_DIRECTIONS:
                    continue
                if self._expand_in_cardinal_direction(next_node, expand_direction, cost):
                    found_cardinal_expansion_interest = True

            if found_cardinal_expansion_interest and next_node.distance == float('inf'):
                next_node.visited = True
                next_node.distance = cost + self._heuristic(next_node)
                next_node.travel_cost = cost
                next_node.direction = direction
                next_node.previous = origin_node
                self._visible_nodes.append(next_node)

    def _expand_start_node(self, start_node):
        all_directions = list(Grid.CARDINAL_DIRECTIONS) + \
            list(Grid.DIAGONAL_DIRECTIONS)
        for direction in all_directions:
            self._expand_in_direction(start_node, direction, 0)

    def _init_start_node(self):
        start_node = self._graph.get_start_node()
        start_node.distance = 0
        start_node.travel_cost = 0
        start_node.direction = None
        start_node.visited = True
        return start_node

    def _get_position_in_direction(self, pos, move_direction):
        return (pos[0] + move_direction[0], pos[1] + move_direction[1])

    def _get_node_in_direction(self, node, move_direction):
        pos = self._get_position_in_direction(node.pos, move_direction)
        return self._graph.get_node(pos)

    def _distance_between_nodes(self, node_a, node_b):
        x_delta = node_a.pos[0] - node_b.pos[0]
        y_delta = node_a.pos[1] - node_b.pos[1]
        return math.sqrt(x_delta**2 + y_delta**2)

    def _heuristic(self, node):
        return self._distance_between_nodes(node, self._graph.get_goal_node())

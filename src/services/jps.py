import math
from entities.graph import Graph
from entities.history import History
from services.heap import Heap


class JPS():
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    NE = (1, -1)
    SE = (1, 1)
    SW = (-1, 1)
    NW = (-1, -1)
    CARDINAL_DIRECTIONS = {UP, RIGHT, DOWN, LEFT}
    DIAGONAL_DIRECTIONS = {NE, SE, SW, NW}

    # Running into these points while looking ahead can cause forced neighbors.
    # Dict key is the expanding direction, values are a list of (blocked, free) tuples
    # stored as relative directions to the inspected node position.
    BLOCKED_FREE_PAIRS = {UP: [(LEFT, NW), (RIGHT, NE)],
                          RIGHT: [(UP, NE), (DOWN, SE)],
                          DOWN: [(LEFT, SW), (RIGHT, SE)],
                          LEFT: [(UP, NW), (DOWN, SW)],
                          NE: [(LEFT, NW), (DOWN, SE)],
                          SE: [(LEFT, SW), (UP, NE)],
                          SW: [(UP, NW), (RIGHT, SE)],
                          NW: [(DOWN, SW), (RIGHT, NE)]}

    EXPANSION_DIRECTIONS = {UP: [UP], RIGHT: [RIGHT], DOWN: [DOWN], LEFT: [LEFT],
                            NE: [UP, NE, RIGHT], SE: [DOWN, SE, RIGHT],
                            SW: [DOWN, SW, LEFT], NW: [UP, NW, LEFT]}

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
        if direction in self.CARDINAL_DIRECTIONS:
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
                extra_cardinal_directions.append(self.RIGHT)
            else:
                extra_cardinal_directions.append(self.LEFT)

            if direction[1] > 0:
                extra_cardinal_directions.append(self.DOWN)
            else:
                extra_cardinal_directions.append(self.UP)

            for expand_direction in self.EXPANSION_DIRECTIONS[direction]:
                if expand_direction in self.DIAGONAL_DIRECTIONS:
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
        all_directions = list(self.CARDINAL_DIRECTIONS) + \
            list(self.DIAGONAL_DIRECTIONS)
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

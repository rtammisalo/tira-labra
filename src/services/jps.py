import math
from entities.jps_graph import JPSGraph
from entities.grid import Grid
from services.heap import Heap


class JPS():
    """ Class for handling Jump Point Search algorithm.
    """

    def __init__(self, grid):
        """ Inits the algorithm, requires a fully formed Grid-object as the base map.
        """
        self._grid = grid
        self.graph = JPSGraph(grid)
        self._open_nodes_by_distance = Heap([])
        self._expanded_nodes = []
        self._visible_nodes = []
        self._generate_step_info = True

    def run(self):
        """ Runs the algorithm without generating step information or stopping every step.
        Returns the path to the goal, or an empty list if there was no path.
        """
        try:
            self._generate_step_info = False
            generator = self.next_step()
            while True:
                generator.__next__()
        except StopIteration as stop:
            return stop.value

    def next_step(self):
        """ Generates the next step of the algorithm. Expands the popped jump point and yields
        to the caller a tuple of jump point node (current node), list of new jump points
        (visited_nodes) and a list of node, direction pairs of nodes visited in look-ahead
        operations. Returns the path to the goal if it exists.
        """
        self._init_start_node()
        self._expand_from_start_node()
        if self._generate_step_info:
            yield self.graph.get_start_node(), self._visible_nodes, self._expanded_nodes

        while True:
            current_node = self._open_nodes_by_distance.pop_node()
            if not current_node:
                break

            if current_node == self.graph.get_goal_node():
                return self._create_path_to_goal()

            if self._generate_step_info:
                self._expanded_nodes = []
                self._visible_nodes = []

            self._expand_jump_point(current_node)

            if self._generate_step_info:
                yield current_node, self._visible_nodes, self._expanded_nodes
            else:
                yield None

        return []

    def _jump_in_direction(self, initial_node, direction):
        """ Performs a jump operation starting from initial node in the
        given direction.
        """
        next_node = initial_node
        while True:
            next_node = next_node.get_node_in_direction(direction)
            if not next_node:
                return None

            if self._generate_step_info:
                self._expanded_nodes.append((next_node, direction))

            if next_node == self.graph.get_goal_node():
                return next_node
            if next_node.has_forced_neighbor(direction):
                return next_node

            if direction in Grid.DIAGONAL_DIRECTIONS:
                for cardinal_direction in next_node.get_cardinal_expansion_directions(direction):
                    if self._jump_in_direction(next_node, cardinal_direction):
                        return next_node

    def _get_cost_for_jump(self, initial_node, jump_node):
        """ Calculates the cost of travelling from initial_node to
        the new jump node.
        """
        x_delta = initial_node.pos[0] - jump_node.pos[0]
        y_delta = initial_node.pos[1] - jump_node.pos[1]
        if x_delta == 0:
            return abs(y_delta)
        if y_delta == 0:
            return abs(x_delta)
        return math.sqrt(x_delta**2 + y_delta**2)

    def _add_jump_node_to_heap(self, initial_node, jump_node, direction):
        """ Adds the jump node to the heap, if the node exists is actually
        closer (in distance) than the previous iteration of it in the heap.
        """
        if not jump_node or jump_node.visited:
            return

        new_total_cost = initial_node.total_cost + \
            self._get_cost_for_jump(initial_node, jump_node)
        new_distance = new_total_cost + \
            self._heuristic_distance(jump_node)

        if new_distance < jump_node.distance:
            jump_node.distance = new_distance
            jump_node.total_cost = new_total_cost
            jump_node.previous = initial_node
            jump_node.direction = direction
            self._open_nodes_by_distance.push_node(jump_node)

            if self._generate_step_info:
                self._visible_nodes.append(jump_node)

    def _expand_jump_point(self, initial_node):
        """ Expands away from the jump point in the direction of pruned neighbors. This
        operation can create new jump points in the heap.
        """
        direction = initial_node.direction
        for jump_direction in initial_node.iter_pruned_neighbor_directions(direction):
            jump_node = self._jump_in_direction(initial_node, jump_direction)
            self._add_jump_node_to_heap(
                initial_node, jump_node, jump_direction)

    def _expand_from_start_node(self):
        """ A special case of finding new jump points.
        """
        start_node = self.graph.get_start_node()
        all_directions = list(Grid.CARDINAL_DIRECTIONS) + \
            list(Grid.DIAGONAL_DIRECTIONS)
        for direction in all_directions:
            jump_node = self._jump_in_direction(start_node, direction)
            self._add_jump_node_to_heap(start_node, jump_node, direction)

    def _init_start_node(self):
        start_node = self.graph.get_start_node()
        start_node.distance = 0
        start_node.total_cost = 0
        start_node.direction = None
        start_node.visited = True

    def _heuristic_distance(self, node):
        return self._get_cost_for_jump(node, self.graph.get_goal_node())

    def _get_nodes_between(self, node, previous_node):
        """ Returns a list of JPSNodes between node and previous node. """
        delta_pos = previous_node.pos[0] - \
            node.pos[0], previous_node.pos[1] - node.pos[1]
        moves = max(abs(delta_pos[0]), abs(delta_pos[1]))

        def get_move_coord(delta_coord):
            if delta_coord != 0:
                return delta_coord // abs(delta_coord)
            return 0

        move_direction = (
            get_move_coord(delta_pos[0]),
            get_move_coord(delta_pos[1]),
        )

        nodes = []
        while moves > 0:
            node = node.get_node_in_direction(move_direction)
            nodes.append(node)
            moves -= 1
        return nodes

    def _create_path_to_goal(self):
        """ Creates a list of node positions from start to goal node.
        """
        node = self.graph.get_goal_node()
        start_node = self.graph.get_start_node()
        path_to_goal = [node.pos]
        while node != start_node:
            previous_node = node.previous
            nodes_list = self._get_nodes_between(node, previous_node)
            for found_node in nodes_list:
                path_to_goal.append(found_node.pos)
            node = previous_node
        path_to_goal.reverse()
        return path_to_goal

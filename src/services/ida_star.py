from collections import deque
from entities.graph import Graph
from services.math_utils import octile_distance
from services.algorithm import Algorithm


class IDAStar(Algorithm):
    """ Implements IDA* pathfind algorithm. Supports Timer time limits.

    https://en.wikipedia.org/wiki/Iterative_deepening_A*
    """

    def __init__(self, grid):
        """ Constructor needs a Grid-object as an argument."""
        super().__init__(grid)
        self.graph = Graph(grid)
        self._visited_nodes = {}
        self._found_paths = []
        self._bound = 0
        self._path_found = False
        self._last_node_on_path = None

    def next_step(self):
        """ Take a 'step' of the algorithm. In IDA* this means one update of the
        bound. The algorithm is run until it finds the goal, or it ran into the current
        bound on all possible paths.

        Returns:
            list: Returns the path to the goal as a list of node positions.

        Yields:
            list: Yields the tuple (visited_nodes, found_paths) per step.

        Raises an exception if the time limit is reached.
        """
        self._bound = self._heuristic(self.graph.get_start_node())
        self._add_to_path(self.graph.get_start_node())

        if self._generate_step_info:
            yield self._get_step_info()

        while True:
            cheapest_path_cost = self._search(0)
            self._bound = cheapest_path_cost

            if self._generate_step_info:
                yield self._get_step_info()

            if self._path_found:
                return self._get_path()

            if cheapest_path_cost == float('inf'):
                return []

            if self._timer.in_use():
                self._timer.add_used_time()

    def _search(self, total_cost):
        """ IDA* search function. Called recursively to go through all possible
        paths inside the bound limits.

        Args:
            total_cost (float): The total cost of the path up to the last node
            on the 'stack' (self._last_node_on_path).

        Returns:
            float: The minimum path cost of all possible candidates around the
            node. In this case, this means the max. 8 directions the search
            can move from the node at the top of the 'stack'. If the estimated
            path cost is higher than the bound, the method returns the estimation.
        """
        if self._timer.in_use():
            self._timer.add_used_time()

        node = self._last_node_on_path
        estimated_cost = total_cost + self._heuristic(node)

        # Possible floating point errors.
        if estimated_cost - 1e-10 > self._bound:
            self._update_found_paths()
            return estimated_cost

        if self._is_goal_node(node):
            self._path_found = True
            self._update_found_paths()
            return estimated_cost

        min_cost = float('inf')

        for successor, move_cost, _ in self._successors(total_cost, node):
            if not self._node_is_on_path(successor):
                self._add_to_path(successor)

                cheapest_path_cost = self._search(total_cost + move_cost)

                if self._path_found:
                    return min_cost

                if cheapest_path_cost < min_cost:
                    min_cost = cheapest_path_cost

                self._remove_last_from_path()

        return min_cost

    def _node_is_on_path(self, node):
        if node.previous or node == self.graph.get_start_node():
            return True
        return False

    def _add_to_path(self, node):
        """Adds the node to the path. Instead of a direct stack, I
        used the previous links of the nodes to handle the path.

        Args:
            node (Node): Adds this node to the 'stack'.
        """
        node.previous = self._last_node_on_path
        self._last_node_on_path = node
        self._update_visited_nodes(node)

    def _remove_last_from_path(self):
        """Removes the last inserted node from the 'stack'. """
        removed_node = self._last_node_on_path
        self._last_node_on_path = removed_node.previous
        removed_node.previous = None

    def _successors(self, total_cost, node):
        """Generates a list of possible successor nodes for this node.
        Ordered by the estimated total cost (g + h(node)) of the successor
        node.

        Args:
            total_cost (float): The total cost of path up to node.
            node (Node): The node who's successors (neighbors) we are
            interested in.

        Returns:
            list: A sorted list of cheapest neighboring successors to the node.
            In ascending order.
        """
        neighbors = node.get_neighbors()
        ordered_neighbors = []
        for neighbor_node, move_cost in neighbors:
            estimated_cost = total_cost + move_cost + \
                self._heuristic(neighbor_node)
            ordered_neighbors.append(
                (neighbor_node, move_cost, estimated_cost))
        return sorted(ordered_neighbors, key=lambda node_data: node_data[2])

    def _get_step_info(self):
        visited_nodes = list(self._visited_nodes.values())
        found_paths = self._found_paths
        self._visited_nodes = {}
        self._found_paths = []
        return visited_nodes, found_paths

    def _update_found_paths(self):
        if self._generate_step_info:
            self._found_paths.append(self._get_path())

    def _update_visited_nodes(self, new_visited_node):
        if self._generate_step_info:
            self._visited_nodes[new_visited_node.pos] = new_visited_node

    def _heuristic(self, node):
        return octile_distance(node, self.graph.get_goal_node())

    def _is_goal_node(self, node):
        return node == self.graph.get_goal_node()

    def _get_path(self):
        """Returns a path from start to last node on path.

        Returns:
            list: A list of node position tuples (x,y).
        """
        node = self._last_node_on_path
        path = deque([node.pos])
        while node.previous:
            node = node.previous
            path.appendleft(node.pos)
        return list(path)

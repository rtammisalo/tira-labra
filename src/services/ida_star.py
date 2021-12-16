from collections import deque
from entities.graph import Graph
from services.distance import octile_distance
from services.algorithm import Algorithm


class IDAStar(Algorithm):
    """ Implements IDA* pathfind algorithm.

    https://en.wikipedia.org/wiki/Iterative_deepening_A*
    """

    def __init__(self, grid):
        """ Constructor needs a Grid-object as an argument. """
        super().__init__(grid)
        self.graph = Graph(grid)
        self._visited_nodes = {}
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
            list: Yields per step a list of visited nodes.
        """
        self._bound = self._heuristic(self.graph.get_start_node())
        self._add_to_path(self.graph.get_start_node())

        if self._generate_step_info:
            yield self._get_step_info()

        while True:
            cheapest_path_cost = self._search(0)

            if self._generate_step_info:
                yield self._get_step_info()
                self._visited_nodes = {}

            if self._path_found:
                return self._get_path()

            if cheapest_path_cost == float('inf'):
                return []

            self._bound = cheapest_path_cost

    def _search(self, total_cost):
        """ IDA* search function. Called recursively to go through all possible
        paths inside the bound limits.

        Args:
            total_cost (float): The total cost of the path up to the last node
            on the 'stack' (self._last_node_on_path).

        Returns:
            float: The minimum path cost of all possible candidates around the
            node. In this case, this means the max. 8 directions the search
            can move from the node at the top of the 'stack'.
        """
        node = self._last_node_on_path
        estimated_cheapest_cost = total_cost + self._heuristic(node)

        # substract 10^(-10) to deal with rounding errors.
        if estimated_cheapest_cost - 1e-10 > self._bound:
            return estimated_cheapest_cost

        if self._is_goal_node(node):
            self._path_found = True
            return estimated_cheapest_cost

        min_cost = float('inf')

        for successor, move_cost, _ in self._successors(total_cost, node):
            if not successor.previous and successor != self.graph.get_start_node():
                # The successor node is on the path if it has a previous node linked to it.
                self._add_to_path(successor)

                cheapest_path_cost = self._search(total_cost + move_cost)

                if self._path_found:
                    return min_cost

                if cheapest_path_cost < min_cost:
                    min_cost = cheapest_path_cost

                self._remove_last_from_path()

        return min_cost

    def _add_to_path(self, node):
        """Adds the node to the path. Instead of a direct stack, I
        used the previous links of the nodes to handle the stack.

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
        return list(self._visited_nodes.values())

    def _update_visited_nodes(self, new_visited_node):
        self._visited_nodes[new_visited_node.pos] = new_visited_node

    def _heuristic(self, node):
        return octile_distance(node, self.graph.get_goal_node())

    def _is_goal_node(self, node):
        return node == self.graph.get_goal_node()

    def _get_path(self):
        """Returns a path from start to goal.

        Returns:
            list: A list of node position tuples (x,y).
        """
        node = self._last_node_on_path
        path = deque([node.pos])
        while node.previous:
            node = node.previous
            path.appendleft(node.pos)
        return list(path)

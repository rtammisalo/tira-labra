from entities.graph import Graph
from services.heap import Heap
from services.algorithm import Algorithm


class Dijkstra(Algorithm):
    """Implementation of Dijkstra's algorithm. Finds the shortest path on a cell-based
    grid from the starting cell to the goal cell.

    https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
    """

    def __init__(self, grid):
        """Initializes the inner graph to resemble the given grid-object.

        Args:
            grid (Grid): Grid depiction of the map.
        """
        super().__init__(grid)
        self.graph = Graph(grid)
        self._open_nodes_by_distance = Heap(self.graph.get_nodes())
        self._open_nodes_by_distance.decrease_distance(
            self.graph.get_start_node(), 0)

    def next_step(self):
        """A step generator for Dijkstra's algorithm.

        Args:
            step_info (bool, optional): Set to true, if you want to generate visited node,
            visible nodes list pairs per step. Defaults to True.

        Returns:
            list of positions: a path to the goal

        Yields:
            visited node, visible nodes (list): Returns the node visited this step and the new
            visible nodes from this step.
        """
        while not self._open_nodes_by_distance.is_empty():
            node = self._open_nodes_by_distance.pop_node()

            if node.distance == float('inf'):
                # We ran out of neighbors (direct or indirect) to the starting cell,
                # which means that there is no path to goal.
                break

            if self._generate_step_info:
                visible_nodes = []

            if node == self.graph.get_goal_node():
                if self._generate_step_info:
                    yield node, visible_nodes
                return node.path_from_start()

            for neighbor_node, edge_weight in node.get_neighbors():
                if neighbor_node.visited:
                    continue

                if self._generate_step_info:
                    visible_nodes.append(neighbor_node)

                new_distance = node.distance + edge_weight

                if new_distance < neighbor_node.distance:
                    self._open_nodes_by_distance.decrease_distance(
                        neighbor_node, new_distance)
                    neighbor_node.previous = node

            if self._generate_step_info:
                yield node, visible_nodes

        return []

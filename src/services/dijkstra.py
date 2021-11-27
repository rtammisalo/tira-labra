from entities.graph import Graph
from services.heap import Heap


class Dijkstra():
    """Implementation of Dijkstra's algorithm. Finds the shortest path on a cell-based
    grid from the starting cell to the goal cell.
    """

    def __init__(self, grid):
        """Initializes the inner graph to resemble the given grid.

        Args:
            grid (Grid): Grid depiction of the map.
        """
        self._grid = grid
        self._graph = Graph(grid)
        self._open_nodes_by_distance = Heap(self._graph.get_nodes())
        self._open_nodes_by_distance.update_node(
            self._graph.get_start_node(), 0)

    def run(self):
        """Executes Dijkstra's algorithm on the graph. Returns a list of grid positions
        as the path to the goal, if possible. If no path was found the method returns an
        empty list.
        """
        try:
            generator = self.next_step(step_info=False)
            while True:
                generator.__next__()
        except StopIteration as stop:
            return stop.value

    def next_step(self, step_info=True):
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
            node.visited = True

            if step_info:
                visible_nodes = []

            for neighbor_node, edge_weight in node.get_neighbors():
                if neighbor_node.visited:
                    continue

                if step_info:
                    visible_nodes.append(neighbor_node)

                new_distance = node.distance + edge_weight

                if new_distance < neighbor_node.distance:
                    self._open_nodes_by_distance.update_node(
                        neighbor_node, new_distance)
                    neighbor_node.previous = node

                if neighbor_node == self._graph.get_goal_node():
                    if step_info:
                        yield node, visible_nodes
                    return neighbor_node.path_from_start()

            if step_info:
                yield node, visible_nodes
            else:
                yield None

        return []

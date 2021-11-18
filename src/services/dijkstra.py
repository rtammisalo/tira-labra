import heapq
from entities.graph import Graph
from entities.history import History


class Heap():
    """A small wrapper class for ease-of-use min-heap operations.
    """

    def __init__(self, nodes_list):
        """Inits the min-heap. Accepts a list of nodes as an argument.
        """
        self._heap = nodes_list
        heapq.heapify(self._heap)

    def push_node(self, node):
        """Push a node to the min-heap.
        """
        heapq.heappush(self._heap, node)

    def pop_node(self):
        """Pops the smallest node from the heap and returns it.
        """
        return heapq.heappop(self._heap)

    def update_node(self, node, new_distance):
        """Call this if you need to update the distance of a node.

        Args:
            node (Node): The node to be updated.
            new_distance (float): The new distance to the starting node for this node.
        """
        node.distance = new_distance
        heapq.heapify(self._heap)

    def is_empty(self):
        """Returns True if the heap is empty.
        """
        return len(self._heap) == 0


def init_distance_heap(graph):
    """Inits the min heap for storing nodes in order of distance from the starting node.

    Args:
        graph (Graph): A graph object made from the grid map.

    Returns:
        Heap: Returns the min heap.
    """
    distance = Heap(graph.get_nodes())
    distance.update_node(graph.get_start_node(), 0)
    return distance


def dijkstra(grid, logging=True):
    """Implementation of Dijkstra's algorithm. Finds the shortest path on a cell-based
    grid from the starting cell to the goal cell.

    Args:
        grid (Grid): Descibes the graph as an x by y grid with empty spaces, walls and
            starting and goal cells.

    Returns:
        Node, History: Returns a tuple containing the goal node and a history of
            visited/visible nodes. The goal node can be used to find the shortest path from
            the starting node. Returns a None if the goal was not reachable.

            History object can be used to trace the visited and visible nodes per each step of
            the algorithm.
    """
    graph = Graph(grid)
    distance = init_distance_heap(graph)
    history = History()

    while not distance.is_empty():
        node = distance.pop_node()
        node.visited = True

        if logging:
            history.add_step(node)

        for neighbor_node, edge_weight in node.get_neighbors():
            if neighbor_node.visited:
                continue

            new_distance = node.distance + edge_weight

            if new_distance < neighbor_node.distance:
                distance.update_node(neighbor_node, new_distance)
                neighbor_node.previous = node

            if logging:
                history.add_visible_node(neighbor_node)

            if neighbor_node == graph.get_goal_node():
                return neighbor_node, history

    return None, history

from entities.graph import Graph
from entities.history import History
from services.heap import Heap


def dijkstra(grid, logging=True):
    """Implementation of Dijkstra's algorithm. Finds the shortest path on a cell-based
    grid from the starting cell to the goal cell.

    Args:
        grid (Grid): Descibes the graph as an x by y grid with empty spaces, walls and
            starting and goal cells.

    Returns:
        Node, History: Returns a tuple containing the path to goal and a history of
            visited/visible nodes. Returns an empty list as path if the goal was not reachable.

            History object can be used to trace the visited and visible nodes per each step of
            the algorithm.
    """
    graph = Graph(grid)
    distance = Heap(graph.get_nodes())
    distance.update_node(graph.get_start_node(), 0)
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
                return neighbor_node.path_from_start(), history

    return [], history

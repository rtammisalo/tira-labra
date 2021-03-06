import math


class Node():
    """Node class used to represent nodes in a graph, with additional book keeping for distance to
    start node and a link to the discoverer node. Tied to a specific grid position (x,y).
    """
    relative_neighbor_positions = [
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, pos, graph):
        """Initializes the node. Sets distance to start node to infinity, previous node to
        None and marks the node unvisited.

        Args:
            pos (tuple int): The coordinates this node represents on the grid.
        """
        self.pos = pos
        self.graph = graph
        self.distance = float('inf')
        self.previous = None
        self.visited = False

    def get_neighbors(self):
        """Returns a list of tuples featuring neighboring nodes and their edge weights.
        """
        neighbors = []

        for relative_position in self.relative_neighbor_positions:
            neighbor_pos = (sum(elem)
                            for elem in zip(self.pos, relative_position))
            neighbor_node = self.graph.get_node(tuple(neighbor_pos))

            if neighbor_node:
                if relative_position[0] != 0 and relative_position[1] != 0:
                    edge_weight = math.sqrt(2)
                else:
                    edge_weight = 1

                neighbors.append((neighbor_node, edge_weight))

        return neighbors

    def path_from_start(self):
        """Returns a list with node coordinates starting from start node to this node.
        Returns an empty list, if the node was not reachable from the start node.
        """
        node = self
        path = []

        if not self.previous:
            return path

        while True:
            if not node:
                break
            path.append(node.pos)
            node = node.previous

        path.reverse()

        if len(path) > 0 and path[0] != self.graph.get_start_node().pos:
            return []

        return path

    def __lt__(self, other_node):
        return self.distance < other_node.distance

    def __eq__(self, other_node):
        if isinstance(other_node, Node):
            return self.pos == other_node.pos
        raise NotImplementedError()

    def __str__(self):
        prev_node_pos = None
        if self.previous:
            prev_node_pos = self.previous.pos
        return f'Node at {self.pos}, distance of {self.distance}, ' \
            f'previous node set to {prev_node_pos}'

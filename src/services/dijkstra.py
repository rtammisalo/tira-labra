import math
import heapq


class Node():
    """Node class used to represent nodes in a graph, with additional book keeping for distance to
    start node and a link to the discoverer node. Tied to a specific grid position (x,y).
    """
    relative_neighbor_positions = [
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, pos):
        """Initializes the node. Sets distance to start to infinity, and previous node to

        Args:
            pos (tuple int): The coordinates this node represents on the grid.
        """
        self.pos = pos
        self.distance = float('inf')
        self.previous = None

    def get_possible_neighbors(self):
        """Return a list of possible neighbor coordinates. Some of the tuples might be outside of
        the grid, or pointing towards wall-cells on the grid.

        Returns:
            list of tuples: a coordinate list for possible neighbor nodes on the grid.
        """
        neighbors = []
        for relative_position in self.relative_neighbor_positions:
            neighbor_pos = (sum(elem)
                            for elem in zip(self.pos, relative_position))
            edge_weight = math.sqrt(
                sum([coord**2 for coord in relative_position]))
            neighbors.append((tuple(neighbor_pos), edge_weight))
        return neighbors

    def path_from_start(self):
        """Returns a list with node coordinates starting from start node to this node.
        """
        node = self
        path = []

        while True:
            if not node:
                break
            path.append(node.pos)
            node = node.previous

        path.reverse()
        return path

    def __lt__(self, other_node):
        return self.distance < other_node.distance

    def __eq__(self, other_node):
        if isinstance(other_node, Node):
            return self.pos == other_node.pos
        raise NotImplementedError()

    def __hash__(self):
        return hash(self.pos)

    def __str__(self):
        return f'Node at {self.pos}, distance of {self.distance}, ' \
            f'previous node set to {self.previous}'


class Heap():
    """A small wrapper class for ease-of-use min-heap operations.
    """

    def __init__(self):
        """Inits the min-heap.
        """
        self._heap = []

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


def init_nodes(unvisited, distance, grid):
    """Initializes the cells in the grid as nodes in a graph for use by Dijkstra's algorithm.

    Args:
        unvisited (dict): An empty unvisited dict with grid coordinates as keys and the graph
            nodes as values.
        distance (Heap): Empty min-heap for storing the node distances to the starting node.
        grid (Grid): The abstract cell-based grid definition of the graph. Used to create
            the node-wrappers.

    Returns:
        Node: The goal node.
    """
    start_node = None
    goal_node = None

    for y_pos in range(grid.y_size):
        for x_pos in range(grid.x_size):
            cell = grid[y_pos][x_pos].cell
            if cell == '#':
                continue
            node = Node((x_pos, y_pos))
            if cell == 'S':
                start_node = node
            elif cell == 'G':
                goal_node = node
            distance.push_node(node)
            unvisited[node.pos] = node

    distance.update_node(start_node, 0)
    return goal_node


def dijkstra(grid):
    """Implementation of Dijkstra's algorithm. Finds the shortest path on a cell-based
    grid from the starting cell to the goal cell.

    Args:
        grid (Grid): Descibes the graph as an x by y grid with empty spaces, walls and
            starting and goal cells.

    Returns:
        Node: Returns the goal node, which can be used to find the shortest path to
            the goal node from the starting node. None if the goal was not reachable.
    """
    unvisited = {}
    distance = Heap()
    goal_node = init_nodes(unvisited, distance, grid)

    while len(unvisited) > 0:
        node = distance.pop_node()
        del unvisited[node.pos]

        for neighbor_pos, edge_weight in node.get_possible_neighbors():
            if neighbor_pos not in unvisited:
                continue
            neighbor_node = unvisited[neighbor_pos]
            new_distance = node.distance + edge_weight

            if new_distance < neighbor_node.distance:
                distance.update_node(neighbor_node, new_distance)
                neighbor_node.previous = node

            if neighbor_node == goal_node:
                return neighbor_node

    return None

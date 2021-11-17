from entities.node import Node


class Graph():
    """A graph with nodes and a 'concept' of edges between nodes made from a cell-based grid.
    """

    def __init__(self, grid):
        """Inits the graph's nodes based on the grid argument.

        Args:
            grid (Grid): The grid object the graph is made out of.
        """
        self._grid = grid
        self._graph = []
        self._start_node_pos = (-1, -1)
        self._goal_node_pos = (-1, -1)

        for y_pos in range(grid.y_size):
            self._graph.append([])
            for x_pos in range(grid.x_size):
                node = None
                cell = grid[y_pos][x_pos].cell

                if cell != '#':
                    node = Node((x_pos, y_pos), self)

                if cell == 'S':
                    self._start_node_pos = (x_pos, y_pos)
                elif cell == 'G':
                    self._goal_node_pos = (x_pos, y_pos)

                self._graph[y_pos].append(node)

    def get_start_node(self):
        """Returns the starting node of the graph.
        """
        return self.get_node(self._start_node_pos)

    def get_goal_node(self):
        """Returns the goal node of the graph.
        """
        return self.get_node(self._goal_node_pos)

    def get_node(self, pos):
        """Returns the node representing the cell at the given position on the grid.

        Args:
            pos (tuple of coordinates (x,y)): The position of the cell the node represents
                on the grid.

        Returns:
            Node: Returns the node or None if not found (out of bounds or the cell was a wall).
        """
        if not 0 <= pos[0] < self._grid.x_size or not 0 <= pos[1] < self._grid.y_size:
            return None
        return self._graph[pos[1]][pos[0]]

    def get_nodes(self):
        """Returns all the graph's nodes as a list.
        """
        nodes = []
        for y_pos in range(self._grid.y_size):
            for x_pos in range(self._grid.x_size):
                node = self._graph[y_pos][x_pos]
                if node:
                    nodes.append(node)
        return nodes

from entities.grid import Grid
from entities.node import Node


class JPSNode(Node):
    """A node used by Jump Point Search. Inherits Node.
    """
    # Running into these points while looking ahead can cause forced neighbors.
    # Dict key is the expanding direction, values are a list of (blocked, free) tuples
    # stored as relative directions to the inspected node position.
    BLOCKED_FREE_PAIRS = {Grid.UP: [(Grid.LEFT, Grid.NW), (Grid.RIGHT, Grid.NE)],
                          Grid.RIGHT: [(Grid.UP, Grid.NE), (Grid.DOWN, Grid.SE)],
                          Grid.DOWN: [(Grid.LEFT, Grid.SW), (Grid.RIGHT, Grid.SE)],
                          Grid.LEFT: [(Grid.UP, Grid.NW), (Grid.DOWN, Grid.SW)],
                          Grid.NE: [(Grid.LEFT, Grid.NW), (Grid.DOWN, Grid.SE)],
                          Grid.SE: [(Grid.LEFT, Grid.SW), (Grid.UP, Grid.NE)],
                          Grid.SW: [(Grid.UP, Grid.NW), (Grid.RIGHT, Grid.SE)],
                          Grid.NW: [(Grid.DOWN, Grid.SW), (Grid.RIGHT, Grid.NE)]}

    # A dict to hold possible natural neighbors of this node, when moving to the direction of
    # the key value, e.g., when moving NE from this node, consider nodes directly
    # UP, RIGHT and NE of this node as possible natural neighbors.
    EXPANSION_DIRECTIONS = {Grid.UP: [],
                            Grid.RIGHT: [],
                            Grid.DOWN: [],
                            Grid.LEFT: [],
                            Grid.NE: [Grid.UP, Grid.RIGHT],
                            Grid.SE: [Grid.DOWN, Grid.RIGHT],
                            Grid.SW: [Grid.DOWN, Grid.LEFT],
                            Grid.NW: [Grid.UP, Grid.LEFT]}

    def __init__(self, pos, graph):
        super().__init__(pos, graph)
        self.total_cost = 0

    def get_cardinal_expansion_directions(self, direction):
        """ Returns a list of straight directions of pruned neighbors for moving diagonally.
        """
        return self.EXPANSION_DIRECTIONS[direction]

    def iter_pruned_neighbor_directions(self, direction):
        """ Iterate through all pruned neighbors for this node going toward given direction.
        """
        if direction in Grid.DIAGONAL_DIRECTIONS:
            for neighbor_dir in self.get_cardinal_expansion_directions(direction):
                yield neighbor_dir
        yield direction
        for forced_dir in self.iter_forced_neighbor_directions(direction):
            yield forced_dir

    def iter_forced_neighbor_directions(self, direction):
        """ Iterate through forced neighbors of this node, when going toward given direction.
        """
        for blocked_direction, free_direction in self.BLOCKED_FREE_PAIRS[direction]:
            blocked_neighbor = self.get_node_in_direction(blocked_direction)
            free_neighbor = self.get_node_in_direction(free_direction)
            if not blocked_neighbor and free_neighbor:
                yield free_direction

    def has_forced_neighbor(self, direction):
        """ Returns true, if the node has a forced neighbor when jumping
        towards the given direction.
        """
        # pylint: disable=unused-variable
        for neighbor_direction in self.iter_forced_neighbor_directions(direction):
            return True
        return False

    def get_node_in_direction(self, direction):
        """ Returns the neighboring node in the given direction. """
        neighbor_pos = (self.pos[0] + direction[0], self.pos[1] + direction[1])
        return self.graph.get_node(neighbor_pos)

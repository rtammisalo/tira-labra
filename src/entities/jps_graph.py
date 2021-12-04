from entities.graph import Graph
from entities.jps_node import JPSNode


class JPSGraph(Graph):
    """ A small Graph-subclass for creating JPS-compatible graphs.
    """
    def _create_new_node(self, pos):
        return JPSNode(pos, self)

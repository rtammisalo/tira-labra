from entities.graph import Graph
from entities.jps_node import JPSNode


class JPSGraph(Graph):
    def _create_new_node(self, pos):
        return JPSNode(pos, self)

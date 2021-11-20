import heapq


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
        """Pops the smallest node from the heap and returns it. Returns None, if the heap is empty.
        """
        if len(self._heap) == 0:
            return None
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

import heapq


class Heap():
    """A small wrapper class for ease-of-use min-heap operations.
    """

    def __init__(self, nodes_list):
        """Inits the min-heap. Accepts a list of nodes as an argument.
        """
        self._heap = [(node.distance, node) for node in nodes_list]
        heapq.heapify(self._heap)

    def push_node(self, node):
        """Push a node to the min-heap.
        """
        heapq.heappush(self._heap, (node.distance, node))

    def pop_node(self):
        """Pops the smallest node from the heap and returns it. Sets popped node to visited.
        Returns None, if the heap is empty.
        """
        while len(self._heap) > 0:
            node = heapq.heappop(self._heap)[1]
            if not node.visited:
                node.visited = True
                return node

        return None

    def decrease_distance(self, node, new_distance):
        """Call this if you need to update the distance of a node. Works only when
        decreasing distance.

        Args:
            node (Node): The node to be updated.
            new_distance (float): The new distance to the starting node for this node.
        """
        node.distance = new_distance
        self.push_node(node)

    def is_empty(self):
        """Returns True if the heap is empty.
        """
        return len(self._heap) == 0

class History():
    """A storage class for algorithm step history. """

    def __init__(self):
        """Inits the history object.
        """
        self._step = -1
        self._log = []

    def add_step(self, visited_node):
        """Add a new step to the log. A single node in a graph being visited is considered
        a step.

        Args:
            visited_node (Node): The visited node.
        """
        self._log.append((visited_node, []))

    def add_visible_node(self, visible_node):
        """Adds the visible node to the list of visible nodes in the last added step.
        """
        self._log[len(self._log) - 1][1].append(visible_node)

    def advance_step(self):
        """Returns a tuple (visited, visible nodes) containing the node visited in the
        next step, and a list of visible nodes from the visited node.
        """
        if len(self._log) == 0:
            return None

        self._step += 1

        if len(self._log) - 1 < self._step:
            self._step = len(self._log) - 1

        return self._log[self._step]

from entities.node import Node


class History():
    def __init__(self):
        self._log = []

    def add_step(self, visited_node):
        self._log.append((visited_node, []))

    def add_visible_node(self, visible_node):
        self._log[len(self._log) - 1][1].append(visible_node)

    def get_step(self, step):
        if len(self._log) - 1 < step:
            step = len(self._log) - 1

        return self._log[step]

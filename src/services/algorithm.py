class Algorithm:
    """ A base class for all algorithm implementations. """

    def __init__(self, grid):
        """ Sets the step info generation to be on by default.
        """
        self._grid = grid
        self._generate_step_info = True

    def run(self):
        """ Runs the algorithm without generating step information or stopping every step.
        Returns the path to the goal, or an empty list if there was no path.
        """
        try:
            self._generate_step_info = False
            generator = self.next_step()
            while True:
                generator.__next__()
        except StopIteration as stop:
            return stop.value

    def next_step(self):
        """ Generates the next step of the algorithm. Does nothing here. """
        yield []

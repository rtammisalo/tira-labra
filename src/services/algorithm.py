from services.timer import Timer


class Algorithm:
    """ A base class for all algorithm implementations. """

    def __init__(self, grid):
        """ Sets the step info generation to be on by default.
        """
        self._grid = grid
        self._generate_step_info = True
        self._timer = Timer()

    def run(self, time_limit=0):
        """ Runs the algorithm without generating step information or stopping every step.
        Returns the path to the goal, or an empty list if there was no path.

        time_limit sets the time limit in seconds. 0 sets time limit off. Only used by IDA*.
        """
        self._timer = Timer(time_limit)
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

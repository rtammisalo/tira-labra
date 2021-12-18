import time


class TimeOut(Exception):
    """TimeOut exception when time runs out."""
    # pylint: disable=unnecessary-pass
    pass


class Timer:
    """A small timing related class for managing algorithm run time maximums. """

    def __init__(self, time_limit=0):
        """Sets time limit of the algorithm to time_limit (0, default, means no time limit). """
        self._time_limit = time_limit
        self._time_used = 0
        self._time_stamp = 0
        if self.in_use():
            self.start_timer()

    def start_timer(self):
        """Starts the timer, call only once in run-method."""
        self._time_stamp = time.perf_counter()

    def add_used_time(self):
        """Adds the used time between time stamps. Raises TimeOut exception if
        the time limit is over."""
        current_time_stamp = time.perf_counter()
        self._time_used += current_time_stamp - self._time_stamp
        self._time_stamp = current_time_stamp
        if self.is_over_time_limit():
            raise TimeOut

    def is_over_time_limit(self):
        """Returns True if the time limit has been crossed. """
        if self._time_limit == 0:
            return False
        return self._time_used > self._time_limit

    def in_use(self):
        """Returns True if the time limit is being used."""
        return self._time_limit != 0

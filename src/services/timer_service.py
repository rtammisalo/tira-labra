import time
import test_maps
from entities.grid import Grid
from services.dijkstra import Dijkstra


class TimerService():
    """Small timer service for performance measuring.
    """

    def __init__(self):
        self._grid = None
        self.map_description = ""
        self.dijkstra_delta = 0

    def time_performance(self, grid_str=test_maps.BIG_MAP,
                         map_description=test_maps.BIG_MAP_DESCRIPTION):
        """Call this method to start the test. Returns performance report as a string.

        Args:
            grid_str (str, optional): ASCII map. Defaults to test_maps.BIG_MAP.
            map_description (str, optional): Description of the map.
                Defaults to test_maps.BIG_MAP_DESCRIPTION.
        """
        self._grid = Grid(grid_str)
        self.map_description = map_description
        self.dijkstra_delta = self._time_dijkstra()
        return self.get_report()

    def get_report(self):
        """Returns a report string of the last performance measuring.
        """
        return f"Map description: {self.map_description}" + \
            f"Dijkstra time: {self.dijkstra_delta:0.5f}"

    def _time_dijkstra(self):
        dijkstra = Dijkstra(self._grid)
        start_time = time.perf_counter()
        dijkstra.run()
        end_time = time.perf_counter()

        return end_time - start_time

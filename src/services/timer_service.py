import time
import test_maps
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.jps import JPS


class TimerService():
    """Small timer service for performance measuring.
    """

    @staticmethod
    def time_performance(grid_str=test_maps.CITY_MAP,
                         map_description=test_maps.CITY_MAP_DESCRIPTION):
        """Call this method to start the test. Returns performance report as a string.

        Args:
            grid_str (str, optional): ASCII map. Defaults to test_maps.BIG_MAP.
            map_description (str, optional): Description of the map.
                Defaults to test_maps.BIG_MAP_DESCRIPTION.
        """
        grid = Grid(grid_str)
        dijkstra_delta = TimerService._time_dijkstra(grid)
        jps_delta = TimerService._time_jps(grid)
        return TimerService.get_report(map_description, dijkstra_delta, jps_delta)

    @staticmethod
    def get_report(map_description, dijkstra_delta, jps_delta):
        """Returns a report string of the last performance measuring.
        """
        return f"Map description: {map_description}\n" + \
            f"Dijkstra time: {dijkstra_delta:0.5f} s\n" + \
            f"JPS time: {jps_delta:0.05f} s"

    @staticmethod
    def _time_dijkstra(grid):
        dijkstra = Dijkstra(grid)
        start_time = time.perf_counter()
        path = dijkstra.run()
        end_time = time.perf_counter()
        print("Dijkstra path length:", len(path))
        return end_time - start_time

    @staticmethod
    def _time_jps(grid):
        jps = JPS(grid)
        start_time = time.perf_counter()
        path = jps.run()
        end_time = time.perf_counter()
        print("JPS path length:", len(path))
        return end_time - start_time

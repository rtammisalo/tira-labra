import time
import math
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.jps import JPS
from repositories.map_repository import MapRepository


class TimerService():
    """Small timer service for performance measuring.
    """
    RUNS = 5

    @staticmethod
    def time_performance():
        """Runs the algorithms 5 times on all the maps in the maps repository.
        Prints out a detailed report to the console. """
        map_repository = MapRepository()
        print(f"\nRunning each algorithm {TimerService.RUNS} times per map..")
        for map_desc, map_string in map_repository.iter_maps():
            grid = Grid(map_string)
            dijkstra_deltas = [0]*TimerService.RUNS
            jps_deltas = [0]*TimerService.RUNS

            for run in range(TimerService.RUNS):
                dijkstra_deltas[run], dijkstra_path = TimerService._time_algorithm(
                    Dijkstra, grid)
                jps_deltas[run], jps_path = TimerService._time_algorithm(
                    JPS, grid)
            TimerService._print_details((dijkstra_deltas, dijkstra_path),
                                        (jps_deltas, jps_path), map_desc)

    @staticmethod
    def _print_details(dijkstra_details, jps_details, map_description):
        """ Prints a timer details report for one map. Takes tuples of delta timings, path as
        the first 2 arguments. """
        print(f"\n{map_description}")
        dijkstra_delta_avg = TimerService.get_average(dijkstra_details[0])
        jps_delta_avg = TimerService.get_average(jps_details[0])
        print(f"Dijkstra average time taken: {dijkstra_delta_avg:0.5f} s")
        print(f"JPS average time taken: {jps_delta_avg:0.5f} s")
        dijkstra_cost = TimerService._calculate_cost(dijkstra_details[1])
        jps_cost = TimerService._calculate_cost(jps_details[1])
        if math.isclose(dijkstra_cost, jps_cost):
            print(
                f"Found path length of {len(dijkstra_details[1])}"
                f" with a total cost of {dijkstra_cost:0.5f}.")
        else:
            print("paths mismatch.")
            print(
                f"Found Dijkstra path length of {len(dijkstra_details[1])}"
                f" with a total cost of {dijkstra_cost:0.5f}.")
            print(
                f"Found JPS path length of {len(jps_details[1])}"
                f" with a total cost of {jps_cost:0.5f}.")

    @staticmethod
    def _calculate_cost(path):
        total_cost = 0
        previous_pos = path[0]
        for next_pos in path[1:]:
            total_cost += math.sqrt((next_pos[0]-previous_pos[0])**2
                                    + (next_pos[1]-previous_pos[1])**2)
            previous_pos = next_pos
        return total_cost

    @staticmethod
    def get_average(deltas):
        """ Returns the average time spent. """
        return sum(deltas) / len(deltas)

    @staticmethod
    def _time_algorithm(algorithm_class, grid):
        """ Times a run of algorithm on specified grid-object.
        Returns a tuple of delta time in ns, and the path.
        """
        algorithm = algorithm_class(grid)
        start_time = time.perf_counter()
        path = algorithm.run()
        end_time = time.perf_counter()
        return end_time - start_time, path

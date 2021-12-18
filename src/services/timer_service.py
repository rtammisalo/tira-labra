import time
import math
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.jps import JPS
from services.ida_star import IDAStar
from services.timer import TimeOut
from services.math_utils import calculate_path_cost
from repositories.map_repository import MapRepository


class TimerService():
    """Small timer service for performance measuring. Ugly and quick.
    """
    RUNS = 5
    IDA_TIME_LIMIT = 30

    @staticmethod
    def time_performance():
        """Runs the algorithms 5 times on all the maps in the maps repository.
        Prints out a detailed report to the console. """
        map_repository = MapRepository()
        print(f"\nRunning each algorithm {TimerService.RUNS} times per map.")
        for map_desc, map_string in map_repository.iter_maps():
            grid = Grid(map_string)
            dijkstra_deltas = [0]*TimerService.RUNS
            jps_deltas = [0]*TimerService.RUNS
            idas_deltas = [0]*TimerService.RUNS
            idas_time_limit_reached = False
            idas_path = []
            print("\n\nRunning...")

            for run in range(TimerService.RUNS):
                print("Run", run + 1)
                dijkstra_deltas[run], dijkstra_path = TimerService._time_algorithm(
                    Dijkstra, grid)
                jps_deltas[run], jps_path = TimerService._time_algorithm(
                    JPS, grid)

                if not idas_time_limit_reached:
                    try:
                        idas_deltas[run], idas_path = TimerService._time_algorithm(
                            IDAStar, grid, TimerService.IDA_TIME_LIMIT)
                    except TimeOut:
                        print("Timelimit of", TimerService.IDA_TIME_LIMIT,
                              "s reached for IDA*")
                        idas_time_limit_reached = True
                        idas_deltas = [-1] * TimerService.RUNS

            print()
            TimerService._print_details((dijkstra_deltas, dijkstra_path),
                                        (jps_deltas, jps_path), (idas_deltas, idas_path), map_desc)

    @staticmethod
    def _print_details(dijkstra_details, jps_details, idas_details, map_description):
        """ Prints a timer details report for one map. Takes tuples of delta timings, path as
        the first 2 arguments. """
        print(f"\n{map_description}")

        dijkstra_delta_avg = TimerService.get_average(dijkstra_details[0])
        jps_delta_avg = TimerService.get_average(jps_details[0])
        idas_delta_avg = TimerService.get_average(idas_details[0])
        print(f"Dijkstra average time taken: {dijkstra_delta_avg:0.5f} s")
        print(f"JPS average time taken: {jps_delta_avg:0.5f} s")
        if idas_delta_avg == -1:
            print("IDA* ran over time limit of", TimerService.IDA_TIME_LIMIT, "s")
        else:
            print(f"IDA* average time taken: {idas_delta_avg:0.5f} s")

        dijkstra_cost = calculate_path_cost(dijkstra_details[1])
        jps_cost = calculate_path_cost(jps_details[1])
        idas_cost = calculate_path_cost(idas_details[1])
        if idas_delta_avg != -1:
            if not math.isclose(idas_cost, jps_cost):
                print("Error: IDA* path cost did not match JPS.")
        if math.isclose(dijkstra_cost, jps_cost):
            print(
                f"Found path length of {len(dijkstra_details[1])}"
                f" with a total cost of {dijkstra_cost:0.5f}.")

    @staticmethod
    def get_average(deltas):
        """ Returns the average time spent. """
        return sum(deltas) / len(deltas)

    @staticmethod
    def _time_algorithm(algorithm_class, grid, time_limit=0):
        """ Times a run of algorithm on specified grid-object.
        Returns a tuple of delta time in ns, and the path.
        """
        algorithm = algorithm_class(grid)
        start_time = time.perf_counter()
        path = algorithm.run(time_limit)
        end_time = time.perf_counter()
        return end_time - start_time, path

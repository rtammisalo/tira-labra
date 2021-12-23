import time
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.jps import JPS
from services.ida_star import IDAStar
from services.timer import TimeOut
from services.math_utils import calculate_path_cost
from repositories.map_repository import MapRepository


class ConsolePrinter:
    """A wrapper for console printing. """

    def write(self, message):
        """Uses print to print out the message."""
        print(message)


console_printer = ConsolePrinter()


class TimerService:
    """Small timer service for performance measuring.
    """
    RUNS = 5
    IDA_TIME_LIMIT = 15

    def __init__(self, printer=console_printer, map_repository=None):
        """Initializes the service.

        Args:
            printer (console printer, optional): Use this to mock console printing.
            Defaults to console_printer.
        """
        if map_repository:
            self._map_repository = map_repository
        else:
            self._map_repository = MapRepository()
        self._printer = printer

    def time_all_performances(self, mapfile=None):
        """Times the performance with all algorithms on a specific map (or all maps).

        Args:
            mapfile (str, optional): Specified map file, defaults to running performance
            tests on all maps.
        """
        if not mapfile:
            self._time_map_repository_maps()
            return

        self.time_performance(mapfile, Dijkstra)
        self.time_performance(mapfile, JPS)
        self.time_performance(mapfile, IDAStar)

    def time_performance(self, mapfile, algorithm_class):
        """Times the performance with a specific algorithm on a specific map.
        IDA* uses automatic time limits.

        Args:
            mapfile (str): Filename
            algorithm_class (Algorithm): Class of the used algorithm
        """
        map_desc, map_string = self._map_repository.read_map(mapfile)
        grid = Grid(map_string)
        time_limit = 0
        path = []
        delta_times = []
        algorithm_name = algorithm_class.__name__

        if algorithm_name == "IDAStar":
            time_limit = self.IDA_TIME_LIMIT

        self._printer.write(
            f"\nRunning {algorithm_name} {self.RUNS} times.")
        self._printer.write(map_desc)

        try:
            for run in range(self.RUNS):
                self._printer.write(f"Starting run {run + 1}")
                delta_time, path = self._time_algorithm(
                    algorithm_class, grid, time_limit)
                delta_times.append(delta_time)

        except TimeOut:
            self._printer.write("Time ran out for IDA*, stopping..")
            return

        self._print_report(delta_times, path)

    def _time_map_repository_maps(self):
        """Time performance for all maps known by the repository.
        """
        all_map_files = self._map_repository.get_map_files()
        for map_file in all_map_files:
            self.time_all_performances(map_file)

    def _print_report(self, delta_times, path):
        """Uses self._printer to print out timer results."""
        self._printer.write(
            f"Average time in seconds: {sum(delta_times) / len(delta_times):0.7f}")
        cost = calculate_path_cost(path)
        self._printer.write(
            f"Found path length of {len(delta_times)}" +
            f" with a total cost of {cost:0.5f}.")

    @staticmethod
    def _time_algorithm(algorithm_class, grid, time_limit=0):
        """ Times a run of algorithm on specified grid-object.
        Returns a tuple of delta time in ns, and the path.

        Does not measure algorithm set up time.
        """
        algorithm = algorithm_class(grid)
        start_time = time.perf_counter()
        path = algorithm.run(time_limit)
        end_time = time.perf_counter()
        return end_time - start_time, path

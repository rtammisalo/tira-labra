import time
import unittest
from unittest.mock import Mock
from services.ida_star import IDAStar
from services.timing_service import TimingService
from services.dijkstra import Dijkstra

TEST_MAP = \
    """
    S.........#
    ########.##
    ########.##
    #####......
    ###........
    ###...#####
    #.........G
    """


class StubPrinter:
    def __init__(self):
        self.messages = []

    def write(self, message):
        self.messages.append(message)


class TestTimingService(unittest.TestCase):
    def setUp(self):
        self.writer = Mock()
        self.printer = StubPrinter()

    def test_time_performance_calls_map_repository_read_map(self):
        map_repository = Mock()
        map_repository.read_map.return_value = "test map desc", "S...G"
        service = TimingService(self.printer, map_repository, self.writer)
        service.time_performance("mapfile", Dijkstra)
        map_repository.read_map.assert_called_with("mapfile")

    def test_time_all_performances_calls_get_map_files_when_no_mapfile_given(self):
        map_repository = Mock()
        map_repository.get_map_files.return_value = []
        service = TimingService(self.printer, map_repository, self.writer)
        service.time_all_performances()
        map_repository.get_map_files.assert_called()

    def test_print_report_prints_average_correctly(self):
        service = TimingService(self.printer)
        service._print_report([1, 2, 3], [])
        for message in self.printer.messages:
            if "Average" in message:
                splits = message.split()
                self.assertAlmostEqual(float(splits[4]), 2)

    def test_idastar_tests_use_timer_and_end_correctly(self):
        map_repository = Mock()
        map_repository.read_map.return_value = "test map desc", TEST_MAP
        service = TimingService(self.printer, map_repository, self.writer)
        service.IDA_TIME_LIMIT = 0.001
        service.time_performance("testmapfile", IDAStar)

        self.assertIn(
            "Time ran out for IDA*, stopping..", self.printer.messages)

    def test_time_performance_runs_as_many_times_as_specified(self):
        map_repository = Mock()
        map_repository.read_map.return_value = "test map desc", TEST_MAP
        service = TimingService(self.printer, map_repository, self.writer)
        service.time_performance("testmapfile", Dijkstra)

        for run in range(service.RUNS):
            self.assertIn(f"Starting run {run + 1}", self.printer.messages)

    def test_time_performance_took_at_least_as_much_time_to_perform_as_the_report_specifies(self):
        map_repository = Mock()
        map_repository.read_map.return_value = "test map desc", TEST_MAP
        service = TimingService(self.printer, map_repository, self.writer)

        start_time = time.perf_counter()
        service.time_performance("testmapfile", Dijkstra)
        end_time = time.perf_counter()
        delta_time = end_time - start_time

        for message in self.printer.messages:
            if "Average" in message:
                splits = message.split()
                self.assertLessEqual(float(splits[4]), delta_time/service.RUNS)

    def test_time_map_repository_maps_calls_file_writer(self):
        file_writer = Mock()
        map_repository = Mock()
        map_repository.get_map_files.return_value = "testmap"
        map_repository.read_map.return_value = "test map desc", TEST_MAP
        service = TimingService(self.printer, map_repository, file_writer)
        service._time_map_repository_maps()
        file_writer.write.assert_called()

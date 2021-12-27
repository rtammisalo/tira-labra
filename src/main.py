import sys
import os
from ui.ui import UI
from services.timing_service import TimingService
from repositories.map_repository import MapRepository
from services.dijkstra import Dijkstra
from services.jps import JPS
from services.ida_star import IDAStar


def get_csv_map_details(map_repository):
    """Returns a list of csv-style strings in format: map name, map cells, map empty spaces."""
    csv = []
    for map_file in map_repository.get_map_files():
        map_desc, map_string = map_repository.read_map(map_file)
        split_desc = map_desc.split()
        map_name = split_desc[2][5:-1]
        map_cells = len(
            list(filter(lambda cell: cell != ' ', map_string)))
        map_empty = len(list(filter(lambda cell: cell == '.', map_string)))
        csv.append(f"{map_name},{map_cells},{map_empty}")
    csv.sort(key=lambda line: (
        int(line.split(",")[1]), int(line.split(",")[2])))
    return ["map name,cells,empty spaces"] + csv


def main():
    """Small main-function for starting the program. """
    map_repository = MapRepository()
    map_file = os.path.join("maps", "test.map")

    if len(sys.argv) > 1:
        timer = TimingService()
        if sys.argv[1] == "timer":
            if len(sys.argv) == 3:
                map_file = sys.argv[2]
            else:
                map_file = None
            timer.time_all_performances(map_file)
            sys.exit()
        elif sys.argv[1] == "csv":
            for line in get_csv_map_details(map_repository):
                print(line)
            sys.exit()
        elif sys.argv[1] == "dijkstra":
            map_file = sys.argv[2]
            timer.time_performance(map_file, Dijkstra)
            sys.exit()
        elif sys.argv[1] == "jps":
            map_file = sys.argv[2]
            timer.time_performance(map_file, JPS)
            sys.exit()
        elif sys.argv[1] == "idastar":
            map_file = sys.argv[2]
            timer.time_performance(map_file, IDAStar)
            sys.exit()
        else:
            # Use the console line argument as the map file.
            map_file = sys.argv[1]

    try:
        map_desc, test_map = map_repository.read_map(map_file)
        print(map_desc)
        display = UI(test_map)
        display.run()
    except FileNotFoundError:
        print("File not found:", map_file)


if __name__ == "__main__":
    main()

import sys
from ui.ui import UI
from services.timer_service import TimerService
from repositories.map_repository import MapRepository


if __name__ == "__main__":
    MAP_FILE = "test.map"

    if len(sys.argv) > 1:
        if sys.argv[1] == "timer":
            timer = TimerService()
            timer.time_performance()
            sys.exit()
        else:
            # Use the console line argument as the map file: a direct file name in maps dir.
            MAP_FILE = sys.argv[1]

    map_repo = MapRepository()
    try:
        map_desc, test_map = map_repo.read_map(MAP_FILE)
        print(map_desc)
        display = UI(test_map)
        display.run()
    except FileNotFoundError:
        print(f"File not found:", MAP_FILE)

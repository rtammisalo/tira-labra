import sys
import os
from ui.ui import UI
from services.timer_service import TimerService
from repositories.map_repository import MapRepository


if __name__ == "__main__":
    MAP_FILE = os.path.join("maps", "test.map")

    if len(sys.argv) > 1:
        if sys.argv[1] == "timer":
            timer = TimerService()
            if len(sys.argv) == 3:
                MAP_FILE = sys.argv[2]
            else:
                MAP_FILE = None
            timer.time_all_performances(MAP_FILE)
            sys.exit()
        else:
            # Use the console line argument as the map file.
            MAP_FILE = sys.argv[1]

    map_repo = MapRepository()
    try:
        map_desc, test_map = map_repo.read_map(MAP_FILE)
        print(map_desc)
        display = UI(test_map)
        display.run()
    except FileNotFoundError:
        print("File not found:", MAP_FILE)

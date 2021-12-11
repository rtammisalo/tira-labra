import sys
from ui.ui import UI
from services.timer_service import TimerService
from repositories.map_repository import MapRepository


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "timer":
            timer = TimerService()
            timer.time_performance()
    else:
        map_repo = MapRepository()
        map_desc, test_map = map_repo.read_map("test.map")
        print(map_desc)
        display = UI(test_map)
        display.run()

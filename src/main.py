import sys
from ui.ui import UI
from services.timer_service import TimerService
import test_maps

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "timer":
            timer = TimerService()
            print(timer.time_performance())
    else:
        display = UI(test_maps.TEST_MAP)
        display.run()

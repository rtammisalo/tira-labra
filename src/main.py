import sys
from ui.ui import UI
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.jps import JPS
from services.timer_service import TimerService
import test_maps

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "timer":
            timer = TimerService()
            print(timer.time_performance())
        else:
            grid = Grid(test_maps.TEST_MAP)
            if sys.argv[1] == "jps":
                algorithm = JPS(grid)
            else:
                algorithm = Dijkstra(grid)
        display = UI(grid, algorithm)
        display.run()

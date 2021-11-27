import sys
from ui.ui import UI
from entities.grid import Grid
from services.dijkstra import Dijkstra
from services.timer_service import TimerService

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "timer":
        timer = TimerService()
        print(timer.time_performance())
    else:
        TEST_GRID_STR = """
        ########.......#....zzz......##############
        .............###.............#G..........
        .....S.........#..........#..###.........
        .............#........######....#...#.#.#
        """
        test_grid = Grid(TEST_GRID_STR)
        display = UI(test_grid, Dijkstra(test_grid))
        display.run()

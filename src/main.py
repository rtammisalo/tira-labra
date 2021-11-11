from ui.ui import UI
from entities.grid import Grid

if __name__ == "__main__":
    TEST_GRID_STR = """
    ########............zzz......##############
    .............###................G........
    .....S...................................
    ......................########......#.#.#
    """
    test_grid = Grid(TEST_GRID_STR)
    print(test_grid)
    display = UI(test_grid)
    display.run()

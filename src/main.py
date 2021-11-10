import ui.ui as ui
import entities.grid as grid

if __name__ == "__main__":
    test_grid_str = """
    ########............zzz......##############
    .............###................G........
    .....S...................................
    ......................########......#.#.#
    """
    test_grid = grid.Grid(test_grid_str)
    print(test_grid)
    display = ui.UI(test_grid)
    display.run()

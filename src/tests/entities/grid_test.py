import unittest
from entities.grid import Grid


class TestGrid(unittest.TestCase):
    def setUp(self) -> None:
        self.grid = Grid('S##\n...\n.G#\n')

    def test_init_grid_creates_corresponding_grid(self):
        correct_grid = ['S # #'.split(), '. . .'.split(), '. G #'.split()]

        for y in range(self.grid.y_size):
            for x in range(self.grid.x_size):
                cell = self.grid[y][x].cell
                self.assertEqual(cell, correct_grid[y][x])

    def test_init_grid_removes_empty_lines_from_grid_str_argument(self):
        grid = Grid('\n\nG##\n..S\n')
        self.assertEqual((grid.x_size, grid.y_size), (3, 2))
        self.assertEqual([cell.cell for cell in grid[0]], 'G # #'.split())
        self.assertEqual([cell.cell for cell in grid[1]], '. . S'.split())

    def test_init_grid_changes_illegal_characters_in_grid_str_to_walls(self):
        grid = Grid('z\n#SG\n')
        self.assertEqual(grid[0][0].cell, '#')

    def test_init_grid_adds_empty_spaces_to_lines_with_less_characters(self):
        grid = Grid('SG.\n#\n###\n')
        self.assertEqual([cell.cell for cell in grid[1]], '# . .'.split())

    def test_grid_string_representation_is_correct(self):
        correct_grid_str = 'Grid size of (3, 3):\nS##\n...\n.G#\n'
        self.assertEqual(str(self.grid), correct_grid_str)

    def test_grid_getitem_returns_correct_grid_row_as_list(self):
        correct_row = '. . .'.split()
        row = cells_to_chars(self.grid[1])
        self.assertEqual(row, correct_row)

    def test_grid_constructor_raises_error_with_no_starting_cell(self):
        with self.assertRaises(ValueError):
            Grid("#..#G")

    def test_grid_constructor_raises_error_with_no_goal_cell(self):
        with self.assertRaises(ValueError):
            Grid("#..#S")

    def test_grid_constructor_raises_error_with_multiple_starting_cells(self):
        with self.assertRaises(ValueError):
            Grid("G#..S#SSSSS")

    def test_grid_constructor_raises_error_with_multiple_goal_cells(self):
        with self.assertRaises(ValueError):
            Grid("GS#..#G")

    def test_set_new_start_changes_the_start_cell(self):
        self.assertEqual(self.grid[0][0].cell, "S")
        self.grid.set_new_start((0, 0), (0, 1))
        self.assertEqual(self.grid[0][0].cell, ".")
        self.assertEqual(self.grid[1][0].cell, "S")

    def test_set_new_start_does_not_change_start_when_called_on_a_wall_cell(self):
        self.grid.set_new_start((0, 0), (1, 0))
        self.assertEqual(self.grid[0][0].cell, "S")
        self.assertNotEqual(self.grid[0][1].cell, "S")

    def test_set_new_goal_changes_the_goal_cell(self):
        self.assertEqual(self.grid[2][1].cell, "G")
        self.grid.set_new_goal((1, 2), (0, 1))
        self.assertEqual(self.grid[2][1].cell, ".")
        self.assertEqual(self.grid[1][0].cell, "G")

    def test_set_new_goal_does_not_change_goal_when_called_on_a_wall_cell(self):
        self.grid.set_new_goal((1, 2), (1, 0))
        self.assertEqual(self.grid[2][1].cell, "G")

    def test_clear_walls_clears_all_wall_cells(self):
        self.grid.clear_walls()
        for row in self.grid:
            for cell in row:
                self.assertNotEqual(cell.cell, "#")

    def test_clear_walls_does_not_clear_start_or_goal(self):
        self.grid.clear_walls()
        start_found = goal_found = False
        for row in self.grid:
            for cell in row:
                if cell.cell == "S":
                    start_found = True
                if cell.cell == "G":
                    goal_found = True
        self.assertTrue(start_found)
        self.assertTrue(goal_found)

    def test_flip_cell_status_flips_wall_to_empty(self):
        self.grid.flip_cell_status((1, 0))
        self.assertEqual(self.grid[1][0].cell, ".")

    def test_flip_cell_status_flips_empty_to_wall(self):
        self.grid.flip_cell_status((0, 1))
        self.assertEqual(self.grid[0][1].cell, "#")

    def test_flip_cell_does_not_change_start_or_goal(self):
        self.grid.flip_cell_status((0, 0))
        self.grid.flip_cell_status((1, 2))
        self.assertEqual(self.grid[0][0].cell, "S")
        self.assertEqual(self.grid[2][1].cell, "G")


def cells_to_chars(cell_row):
    row = []
    for cell in cell_row:
        row.append(cell.cell)
    return row

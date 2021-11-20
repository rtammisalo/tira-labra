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

    def test_init_grid_changes_illegal_characters_in_grid_str_to_empty_spaces(self):
        grid = Grid('z\n#SG\n')
        self.assertEqual(grid[0][0].cell, '.')

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


def cells_to_chars(cell_row):
    row = []
    for cell in cell_row:
        row.append(cell.cell)
    return row

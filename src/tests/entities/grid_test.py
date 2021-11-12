import unittest
from entities.grid import Grid


class TestGrid(unittest.TestCase):
    def setUp(self) -> None:
        self.grid = Grid('##\n..\n.#\n')

    def test_init_grid_with_empty_string_creates_empty_grid(self):
        grid = Grid("")
        self.assertEqual((grid.x_size, grid.y_size), (0, 0))

    def test_init_grid_creates_corresponding_grid(self):
        correct_grid = [['#', '#'], ['.', '.'], ['.', '#']]

        for y in range(self.grid.y_size):
            for x in range(self.grid.x_size):
                cell = self.grid[y][x].cell
                self.assertEqual(cell, correct_grid[y][x])

    def test_init_grid_removes_empty_lines_from_grid_str_argument(self):
        grid = Grid('\n\n###\n...\n')
        self.assertEqual((grid.x_size, grid.y_size), (3, 2))
        self.assertEqual([cell.cell for cell in grid[0]], '# # #'.split())
        self.assertEqual([cell.cell for cell in grid[1]], '. . .'.split())

    def test_init_grid_changes_illegal_characters_in_grid_str_to_empty_spaces(self):
        grid = Grid('z\n#\n')
        self.assertEqual(grid[0][0].cell, '.')

    def test_init_grid_adds_empty_spaces_to_lines_with_less_characters(self):
        grid = Grid('...\n#\n###\n')
        self.assertEqual([cell.cell for cell in grid[1]], '# . .'.split())

    def test_grid_string_representation_is_correct(self):
        correct_grid_str = 'Grid size of (2, 3):\n##\n..\n.#\n'
        self.assertEqual(str(self.grid), correct_grid_str)

    def test_grid_getitem_returns_correct_grid_row_as_list(self):
        correct_row = ['.', '.']
        row = self.grid[1]
        for i in range(2):
            self.assertEqual(row[i].cell, correct_row[i])

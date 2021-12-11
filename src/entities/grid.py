import re
from collections import Counter
from entities.cell import Cell


class Grid():
    """A business-logic side representation of the map as a x by y grid,
    made from different grid cells (walls, empty space, start, goal).
    """
    UP = (0, -1)
    DOWN = (0, 1)
    RIGHT = (1, 0)
    LEFT = (-1, 0)
    NE = (1, -1)
    SE = (1, 1)
    SW = (-1, 1)
    NW = (-1, -1)
    CARDINAL_DIRECTIONS = {UP, RIGHT, DOWN, LEFT}
    DIAGONAL_DIRECTIONS = {NE, SE, SW, NW}

    def __init__(self, grid_str):
        """Generates the grid based on the string encoding of the grid. All empty lines in
        the string are discarded, and the lines are trimmed of leading and trailing whitespaces.
        Smaller lines are padded by implied empty cells in the actual grid.

        Args:
            grid_str (str): A string encoding of the map. Each line of the string contains one row
                of the grid. Use characters '.' (empty), '#' (wall), 'S' (starting cell),
                'G' (goal cell) to signify cell contents in the string.
        """
        _check_string_for_start_and_goal(grid_str)
        lines = self._clean_grid_string(grid_str)
        self._grid = [[Cell(char)
                       for char in line] for line in lines]

    def _clean_grid_string(self, grid_str):
        lines = []
        max_line_length = 0

        for line in grid_str.splitlines():
            line = line.strip()
            if line:
                if max_line_length < len(line):
                    max_line_length = len(line)
                lines.append(line)

        for line_number, line in enumerate(lines):
            if len(line) < max_line_length:
                line += '.' * (max_line_length - len(line))
            lines[line_number] = line

        self.x_size = max_line_length
        self.y_size = len(lines)

        return lines

    def __str__(self):
        grid_str = f'Grid size of ({self.x_size}, {self.y_size}):\n'
        for line in self._grid:
            line_str = ''.join([str(cell) for cell in line])
            grid_str += line_str + '\n'
        return grid_str

    def __getitem__(self, key):
        return self._grid[key]

    def set_new_start(self, old_start, new_start):
        """ Tries to set a new starting point. The point is only set
        if it lies on an empty cell. """
        if self._grid[new_start[1]][new_start[0]].cell == ".":
            self._grid[old_start[1]][old_start[0]] = Cell(".")
            self._grid[new_start[1]][new_start[0]] = Cell("S")

    def set_new_goal(self, old_goal, new_goal):
        """ Tries to set a new goal point. Only set if the new position
        is an empty cell location. """
        if self._grid[new_goal[1]][new_goal[0]].cell == ".":
            self._grid[old_goal[1]][old_goal[0]] = Cell(".")
            self._grid[new_goal[1]][new_goal[0]] = Cell("G")

    def flip_cell_status(self, cell_pos):
        """ Flips an empty cell at cell_pos into a wall cell and vice versa. """
        old_cell = self._grid[cell_pos[1]][cell_pos[0]].cell
        if old_cell == ".":
            self._grid[cell_pos[1]][cell_pos[0]] = Cell("#")
        if old_cell == "#":
            self._grid[cell_pos[1]][cell_pos[0]] = Cell(".")

    def clear_walls(self):
        """ Clears all walls from the grid. """
        for row, cell_row in enumerate(self._grid):
            for column, cell in enumerate(cell_row):
                if cell.cell == "#":
                    self._grid[row][column] = Cell(".")


def _check_string_for_start_and_goal(grid_str):
    matches_counter = Counter(re.findall(r'(S|G)', grid_str))

    if 'S' not in matches_counter:
        raise ValueError('No starting cell in string.')
    if 'G' not in matches_counter:
        raise ValueError('No goal cell in string.')
    if matches_counter['S'] != 1:
        raise ValueError(
            f'Only 1 starting cell supported in string, found {matches_counter["S"]}')
    if matches_counter['G'] != 1:
        raise ValueError(
            f'Only 1 goal cell supported in string, found {matches_counter["G"]}')

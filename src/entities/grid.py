from entities.cell import Cell


class Grid():
    """A business-logic side representation of the map as a x by y grid,
    made from different grid cells (walls, empty space, start, goal).
    """

    def __init__(self, grid_str):
        """Generates the grid based on the string encoding of the grid. All empty lines in
        the string are discarded, and the lines are trimmed of leading and trailing whitespaces.
        Smaller lines are padded by implied empty cells in the actual grid.

        Args:
            grid_str (str): A string encoding of the map. Each line of the string contains one row
                of the grid. Use characters '.' (empty), '#' (wall), 'S' (starting cell),
                'G' (goal cell) to signify cell contents in the string.
        """
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

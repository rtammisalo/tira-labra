from entities.cell import Cell


class Grid():

    def __init__(self, grid_str):
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
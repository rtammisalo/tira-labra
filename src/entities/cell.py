class Cell():
    """A business-logic side entity for storing grid cell information.
    """
    WALL = '#'
    EMPTY = '.'
    START = 'S'
    GOAL = 'G'
    LEGAL_CELLS = {'.', '#', 'S', 'G'}

    def __init__(self, char='.'):
        """Creates a new cell.

        Args:
            char (char, optional): Used to define cell type. Defaults to None (empty space).
        """
        self.set_cell_type(char)

    def set_cell_type(self, char):
        """Sets the cell to the type indicated by the argument.

        Args:
            char (char): Used to determine the new cell type. Use:
            Cell.EMPTY: empty space,
            Cell.WALL: wall,
            Cell.START: starting cell,
            Cell.GOAL: ending cell, All other characters are interpreted as walls.
        """
        if char in Cell.LEGAL_CELLS:
            self.cell = char
        else:
            self.cell = '#'

    def __str__(self):
        return self.cell

    def is_wall(self):
        """Returns True if the cell is a wall. """
        return self.cell == self.WALL

    def is_empty(self):
        """Returns True if the cell is an empty space. """
        return self.cell == self.EMPTY

    def is_start(self):
        """Returns True if the cell is the starting cell. """
        return self.cell == self.START

    def is_goal(self):
        """Returns True if the cell is the goal cell. """
        return self.cell == self.GOAL

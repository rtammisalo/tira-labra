class Cell():
    """A business-logic side entity for storing grid cell information.
    """
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
            '.': empty space,
            '#': wall,
            'S': starting cell,
            'G': ending cell, All other characters are interpreted as an empty space.
        """
        if char in Cell.LEGAL_CELLS:
            self.cell = char
        else:
            self.cell = '.'

    def __str__(self):
        return self.cell

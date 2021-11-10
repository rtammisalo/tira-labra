class Cell():
    LEGAL_CELLS = {'.', '#', 'S', 'G'}

    def __init__(self, char=None):
        if char is not None:
            self.cell = self._char_to_cell(char)
        else:
            self.cell = '.'

    def _char_to_cell(self, char):
        if char in Cell.LEGAL_CELLS:
            return char

        return '.'

    def __str__(self):
        return self.cell
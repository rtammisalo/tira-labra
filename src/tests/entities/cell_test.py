import unittest
from unittest.case import TestCase
from entities.cell import Cell


class TestCell(unittest.TestCase):
    def setUp(self):
        self.test_cell = Cell()

    def test_new_cells_default_to_empty(self):
        self.assertEqual(self.test_cell.cell, '.')

    def test_new_cells_with_illegal_char_arg_default_to_wall(self):
        cell = Cell('m')
        self.assertEqual(cell.cell, '#')

    def test_set_cell_type_changes_type_correctly(self):
        self.test_cell.set_cell_type('#')
        self.assertEqual(self.test_cell.cell, '#')

    def test_set_cell_type_changes_type_to_empty_on_illegal_argument(self):
        self.test_cell.set_cell_type('.')
        self.assertEqual(self.test_cell.cell, '.')
        self.test_cell.set_cell_type('z')
        self.assertEqual(self.test_cell.cell, '#')

    def test_str_representation_is_cell_type(self):
        self.assertEqual(str(self.test_cell), '.')

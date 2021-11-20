import unittest
from entities.history import History


class StubNode():
    def __init__(self, pos):
        self.pos = pos


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.history = History()
        self.history.add_step(StubNode((0, 0)))
        self.history.add_visible_node(StubNode((1, 0)))
        self.history.add_step(StubNode((1, 0)))
        self.history.add_visible_node(StubNode((0, 0)))
        self.history.add_visible_node(StubNode((2, 0)))
        self.history.add_visible_node(StubNode((0, 1)))
        self.history.add_step(StubNode((2, 0)))
        self.history.add_visible_node(StubNode((1, 0)))

    def test_advance_step_returns_none_when_no_steps(self):
        empty = History()
        self.assertIsNone(empty.advance_step())

    def test_advance_step_advances_history(self):
        self.history.advance_step()
        self.history.advance_step()
        visited, visible_nodes = self.history.advance_step()
        self.assertEqual(visited.pos, (2, 0))
        self.assertTrue(len(visible_nodes) == 1)
        self.assertEqual(visible_nodes[0].pos, (1, 0))

    def test_advance_step_shows_the_first_visited_node_on_first_call(self):
        visited, visible_nodes = self.history.advance_step()
        self.assertEqual(visited.pos, (0, 0))

    def test_advance_step_does_not_advance_past_last_step_and_returns_none(self):
        self.history.advance_step()
        self.history.advance_step()
        self.history.advance_step()
        self.history.advance_step()
        self.assertIsNone(self.history.advance_step())

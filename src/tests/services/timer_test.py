import unittest
import time
from services.timer import Timer, TimeOut


class TestTimer(unittest.TestCase):
    def test_timer_starts_at_init_when_time_limit_over_zero(self):
        timer = Timer(1)
        self.assertTrue(timer.in_use())

    def test_timer_does_not_start_at_init_when_time_limit_is_zero(self):
        timer = Timer()
        self.assertFalse(timer.in_use())

    def test_add_used_time_does_not_cause_an_exception_if_not_over_time_limit(self):
        timer = Timer(3)
        timer.add_used_time()

    def test_add_used_time_causes_an_exception_when_over_limit(self):
        timer = Timer(1)
        time.sleep(2)
        with self.assertRaises(TimeOut):
            timer.add_used_time()

    def test_is_over_time_limit_returns_false_when_no_time_limit(self):
        timer = Timer()
        self.assertFalse(timer.is_over_time_limit())

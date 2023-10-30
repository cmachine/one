from scheduler import Scheduler
from time import sleep
from unittest import mock, TestCase


class TestScheduler(TestCase):
    """ Tests for Scheduler. """

    def test_scheduler(self) -> None:
        """ Verify that tasks can be scheduled and cancelled. """
        s = Scheduler()
        a = mock.Mock()
        b = mock.Mock()

        cancel_a1 = s.runOnceAfter(0.1, a)
        s.runOnceAfter(0.2, b)
        s.runOnceAfter(0.3, a)
        cancel_a1()  # should only cancel the FIRST call to a
        assert a.call_count == 0
        assert b.call_count == 0

        sleep(0.15) # time elapsed 0.15
        assert a.call_count == 0
        assert b.call_count == 0

        sleep(0.1)  # time elapsed 0.25
        assert a.call_count == 0
        assert b.call_count == 1

        sleep(0.1)  # time elapsed 0.35
        assert a.call_count == 1
        assert b.call_count == 1

        cancel_a1()  # should be a no-op
        assert a.call_count == 1
        assert b.call_count == 1

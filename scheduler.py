from cacheTypes import SchedulerProtocol
from threading import Timer
from typing import Callable


class Scheduler(SchedulerProtocol):
    """Concrete scheduler implementation using threading.Timer"""

    def runOnceAfter(self, duration_in_seconds: float, fn: Callable[[], None]) -> Callable[[], None]:
        """
        Schedules a function to be run one time after a delay. Returns a cancellation
        function that can be called to cancel the scheduled work before the duration has
        elapsed.
        """
        timer = Timer(duration_in_seconds, fn)
        timer.start()
        return timer.cancel

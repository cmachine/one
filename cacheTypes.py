""" This file exposes protocols used across the caching modules """
from typing import Callable, Optional, Tuple, TypeVar
from typing_extensions import Protocol

T = TypeVar("T")

class CacheProtocol(Protocol[T]):
    """ Protocol for a cache """

    def get(self, key: str) -> Tuple[Optional[T], bool]:
        """
        Cache must implement get, returning the cached value (which may be None)
        & True if it exists and is unexpired, or None & False otherwise
        """

    def set(self, key: str, value: T, expire_after_seconds: Optional[float] = None) -> None:
        """ Cache must implement set, adding an item to the cache """

    def clear(self, key: str) -> bool:
        """ Cache must implement clear, removing an item by key """


class SchedulerProtocol(Protocol):
    """ Protocol for a scheduler """

    def runOnceAfter(self, duration_in_seconds: float, fn: Callable[[], None]) -> Callable[[], None]:
        """
        Schedules a function to be run one time after a delay. Returns a cancellation
        function that can be called to cancel the scheduled work before the duration has
        elapsed.
        """

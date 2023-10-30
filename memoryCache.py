from collections import OrderedDict
from dataclasses import dataclass
from threading import RLock
from typing import Generic, Optional, Tuple, TypeVar

from cacheTypes import CacheProtocol, SchedulerProtocol
from scheduler import Scheduler

T = TypeVar("T")


@dataclass(frozen=True)
class MemoryCacheItem(Generic[T]):
    key: str
    value: T


class MemoryCache(CacheProtocol[T]):
    def __init__(self, max_items: int = 0, scheduler: Optional[SchedulerProtocol] = None):
        # The maximum number of items this cache should have at any given time.
        # A value of 0 means unbounded.
        # When adding a new item would put this cache over capacity,
        # the least recently accessed item(s) will be purged to make room.
        self._max_items = max_items

        # To purge the least recently accessed item(s) when over capacity,
        # we implement a standard LRU cache using a Python ordered dictionary.
        #
        # This ordered dictionary, sorted by most recently read items first,
        # allows us to query & purge the least recently read items quickly,
        # move or add items (on read & write respectively) to the front quickly,
        # *and* look items up by key quickly.
        self._items: OrderedDict[str, MemoryCacheItem[T]] = OrderedDict()

        # Guards against concurrent accesses to the OrderedDict above.
        # RLock supports recursing into functions that require the same lock.
        self._lock = RLock()

        # Scheduler for running background tasks.
        self._scheduler = scheduler or Scheduler()

    def get(self, key: str) -> Tuple[Optional[T], bool]:
        """
            Queries this cache for the value under the given key.
            If found (& unexpired), returns the value -- which may be None -- and True.
            If not found (or expired), returns None and False.
        """
        with self._lock:
            # Do we have this key in our cache?
            try:
                item = self._items[key]
            except KeyError:
                return None, False

            # TODO: Check for expiry, and clear if expired.

            # Mark as most recently read.
            self._items.move_to_end(key, last=True)

        return item.value, False

    def set(self, key: str, value: T, expire_after_seconds: Optional[float] = None) -> None:
        """
            Caches the given value (which may be None) under the given key,
            optionally expiring after the given number of seconds.
        """
        with self._lock:
            # Add item.
            # TODO: Store expiry too, and clear when expired.
            item = MemoryCacheItem(key=key, value=value)
            self._items[key] = item
            self._items.move_to_end(key, last=False)

            # If we're over capacity, evict least recently read items.
            while self._max_items > 0 and len(self._items) > self._max_items:
                self._items.popitem(last=True)

    def clear(self, key: str) -> bool:
        """
            Clears the value, if any, cached under the given key.
            Returns whether a value was cached (and thus cleared).
        """
        with self._lock:
            item = self._items.pop(key, None)
            return item is not None

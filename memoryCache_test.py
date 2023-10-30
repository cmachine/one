import unittest
from collections import namedtuple
from typing import Optional, TypeVar

from memoryCache import MemoryCache

T = TypeVar("T")


class TestMemoryCache(unittest.TestCase):

    # Helpers:

    def assert_not_in_cache(self, cache: MemoryCache[T], key: str) -> None:
        value, cached = cache.get(key)
        self.assertEqual(cached, False, f"Expected {key} to not be in cache but was")
        self.assertIsNone(value)

    def assert_cached_equals(self, cache: MemoryCache[T], key: str, expected: T) -> None:
        value, cached = cache.get(key)
        self.assertEqual(cached, True, f"Expected {key} to be in cache but wasn't")
        self.assertEqual(value, expected)

    # Tests:

    def test_basic(self) -> None:
        # Without worrying about capacity or expiry, should be able to get, set, and clear.

        cache = MemoryCache[str]()

        self.assert_not_in_cache(cache, "a")
        self.assert_not_in_cache(cache, "b")
        self.assert_not_in_cache(cache, "c")

        # We should be able to add items to the cache, then retrieve them.

        a = "A"
        b = "B"

        cache.set("a", a)
        cache.set("b", b)

        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "b", b)

        # Should be able to keep reading the items; they shouldn't be evicted.

        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "b", b)

        # We should be able to clear items from the cache too.
        # Other items should remain in the cache.

        self.assertTrue(cache.clear("a"), "Clear should return true when item in cache")
        self.assertFalse(cache.clear("a"), "Clear should return false when item not in cache")

    def test_capacity(self) -> None:
        # We should be able to limit the cache to a fixed memory capacity.
        # Adding items to the cache beyond the capacity should purge the
        # least recently read items.

        cache = MemoryCache[str](max_items=3)

        # Add items up to the capacity. All items should be retained.

        a = "A"
        b = "B"
        c = "C"

        cache.set("a", a)
        cache.set("b", b)
        cache.set("c", c)

        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "b", b)
        self.assert_cached_equals(cache, "c", c)

        # Access the items in some different order.

        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "b", b)
        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "b", b)  # b is least recently read
        self.assert_cached_equals(cache, "c", c)
        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "c", c)  # c is most recently read

        # Add one more item to the cache. The least recently read item should be gone.

        d = "D"

        cache.set("d", d)

        self.assert_not_in_cache(cache, "b")

        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "c", c)
        self.assert_cached_equals(cache, "d", d)

        # Access the current items in some different order again.

        self.assert_cached_equals(cache, "c", c)  # c is least recently read
        self.assert_cached_equals(cache, "d", d)
        self.assert_cached_equals(cache, "a", a)  # a is most recently read

        # Add *two* items to the cache. The *two* least recently read items should be gone.

        e = "E"

        cache.set("b", b)  # b again
        cache.set("e", e)

        self.assert_not_in_cache(cache, "c")
        self.assert_not_in_cache(cache, "d")

        self.assert_cached_equals(cache, "a", a)
        self.assert_cached_equals(cache, "b", b)
        self.assert_cached_equals(cache, "e", e)

    def test_expiry(self) -> None:
        self.skipTest("TODO: Implement")


if __name__ == "__main__":
    unittest.main()

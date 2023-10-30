from typing import Optional, Tuple, TypeVar

from cacheTypes import CacheProtocol

T = TypeVar("T")


class RedisCache(CacheProtocol[T]):
    def __init__(self) -> None:
        raise NotImplementedError("TODO: implement")

    def get(self, key: str) -> Tuple[Optional[T], bool]:
        raise NotImplementedError("TODO: implement")

    def set(
        self, key: str, value: T, expire_after_seconds: Optional[float] = None
    ) -> None:
        raise NotImplementedError("TODO: implement")

    def clear(self, key: str) -> bool:
        raise NotImplementedError("TODO: implement")

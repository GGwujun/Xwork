from __future__ import annotations

from collections import OrderedDict
from typing import Generic, TypeVar


T = TypeVar("T")


class LruCache(Generic[T]):
    def __init__(self, maxsize: int = 256):
        self.maxsize = maxsize
        self._store: OrderedDict[str, T] = OrderedDict()

    def get(self, key: str) -> T | None:
        if key not in self._store:
            return None
        value = self._store.pop(key)
        self._store[key] = value
        return value

    def set(self, key: str, value: T) -> None:
        if key in self._store:
            self._store.pop(key)
        self._store[key] = value
        if len(self._store) > self.maxsize:
            self._store.popitem(last=False)

    def clear(self) -> None:
        self._store.clear()

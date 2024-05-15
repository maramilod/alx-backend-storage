#!/usr/bin/env python3
"""
h
e
y
"""
import uuid
import redis
from typing import Union, Callable, Optional


class Cache:
    """
    Writing strings to Redis
    _init__ method,
    store an instance of the Redis client as a private variable
    """
    def __init__(self) -> None:
        """store an instance of the Redis client as a private variable"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        store the input data in Redis using
        the random key and return the key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        method that take a key string argument and
        an optional Callable argument named fn.
        This callable will be used to convert
        the data back to the desired format.
        """
        data = self._redis.get(key)
        if data:
            if fn:
                return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        implement method that will automatically parametrize
        Cache.get with str conversion function
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        implement method that will automatically parametriz
        Cache.get with str conversion function
        """
        return self.get(key, lambda d: int(d))

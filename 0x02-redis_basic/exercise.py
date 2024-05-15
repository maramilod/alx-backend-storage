#!/usr/bin/env python3
"""
h
e
y
"""
import uuid
import redis
from typing import Union, Callable, Optional, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    decorator that takes a single method
    Callable argument and returns a Callable.
    """
    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs
    for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwds) -> Any:
        inp = "{}:inputs".format(method.__qualname__)
        out = "{}:outputs".format(method.__qualname__)
        rv = method(self, *args, **kwds)

        self._redis.rpush(inp, str(args))
        self._redis.rpush(out, str(rv))
        return rv
    return wrapper


def replay(method: Callable) -> None:
    """
    """
    n = method.__qualname__
    cache = redis.Redis()
    num = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, num))
    inputs = cache.lrange(n + ":inputs", 0, -1)
    outputs = cache.lrange(n + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(n, i.decode('utf-8'),
                                     o.decode('utf-8')))


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

    @call_history
    @count_calls
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

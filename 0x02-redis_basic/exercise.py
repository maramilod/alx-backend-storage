#!/usr/bin/env python3
"""
h
e
y
"""
import uuid
import redis
from typing import Union


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
        """tore the input data in Redis using the random key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

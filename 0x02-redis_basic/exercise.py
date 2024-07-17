#!/usr/bin/env python3
"""the class definition for redis cache"""
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


def count_calls(method: Callable) -> Callable:
    """
    it counts the times a function is called
    Args:
        method: the function
    Returns:
        the decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function for the decorated function
        Args:
            self: the object instance
            *args: arguments passed into the function
            **kwargs: keyword arguments passed into the function
        Returns:
            value of the function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper
def call_history(method: Callable) -> Callable:
    """
    counts the times a function is called
    Args:
        self: the object
        *args: arguments passed into the function
        **kwargs: keywords arguments passed into the function
    Returns:
        the value od the decorated function
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        wrapper function for the decorated function
        Args:
            self: the object instance
            *args: arguments passed into the function
            **kwargs: keywords arguments passed into the function
        Returns:
            the value od the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper
def replay(method: Callable) -> None:
    """
    replays history of a function
    Args:
        method: function to be decorated
    Returns:
        nothing
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
            o.decode('utf-8')))
class Cache:
    """
    defines the methods to handle redis cache operation
    """
    def __init__(self) -> None:
        """
        initializes redis client
        Attributes:
            self.redis (redis.Redis): redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores data in redis cache
        Args:
            data (dict): data to be stored
        Returns:
            string: key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    def get(self, key, str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float, None]:
            """
            get data from redis cache
            """
            data = slef._redis.get(key)
            if data is not None and fn is not None and callable(fn):
                return fn(data)
            return data
    def get_str(self, key: str) -> str:
        """
        get data as string from redis cache
        Args:
            key (str): key
        Returns:
            str: data
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data
    def get_int(self, key: str) -> int:
        """
        get data as integer from redis cache
        Args:
            key (str): key
        Returns:
            int: data
        """
        data = self

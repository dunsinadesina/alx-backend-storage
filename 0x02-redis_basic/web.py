#!/usr/bin/env python3
"""
module for request caching and tracking
"""
import redis
import requests
from datetime import timedelta


def get_page(url: str) -> str:
    """
    returns the content of a url after caching the req response,
    and tracking the request
    """
    if url is None or len(url.strip()) == 0:
        return ""
    redis_stpre = redis.Redis()
    res_key = "result:{}".format(url)
    req_key = "count:{}".format(url)
    result = redis_store.get(res_key)
    if result is not None:
        redis_stpre.incr(req_key)
        return result
    result = requests.get(url).content.decode('utf-8')
    redis_store.setex(res_key, timedelta(seconds=10), result)
    return result

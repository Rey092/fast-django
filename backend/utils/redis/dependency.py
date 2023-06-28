# -*- coding: utf-8 -*-
"""Redis dependency module."""
from typing import AsyncGenerator

from async_lru import alru_cache
from django.core.cache import cache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis


async def get_redis() -> AsyncGenerator[Redis, None]:
    """
    Return connection pool.
    """
    return await cache.client.get_client()


@alru_cache()
async def get_fastapi_cache_backend() -> RedisBackend:
    """
    Return connection pool.
    """
    return RedisBackend(await get_redis())

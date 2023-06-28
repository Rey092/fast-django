# -*- coding: utf-8 -*-
"""Redis service module."""
from django.core.cache import cache
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from redis.asyncio.utils import from_url  # noqa


async def init_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Create connection pool for redis.

    :param app: current fastapi application.

    """
    # Init redis
    app.state.redis = await cache.client.get_client()
    # Init fastapi limiter
    await FastAPILimiter.init(app.state.redis)
    # Init redis backend for fastapi cache
    app.state.redis_backend = RedisBackend(app.state.redis)
    # Init fastapi cache
    FastAPICache.init(app.state.redis_backend, prefix="fastapi-cache")


async def shutdown_redis(app: FastAPI) -> None:  # pragma: no cover
    """
    Close redis connection pool.

    :param app: current FastAPI app.

    """
    await app.state.redis.connection_pool.disconnect()

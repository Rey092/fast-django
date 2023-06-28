# -*- coding: utf-8 -*-
"""Cache schemas."""
import abc
from typing import Callable, Optional

from asgiref.sync import async_to_sync
from django.core.cache import cache
from fastapi_cache.backends.redis import RedisBackend
from pydantic import BaseModel

from utils.redis.dependency import get_fastapi_cache_backend


class CacheParams(BaseModel):
    """Cache params for the application."""

    namespace: str

    def build_key(self, *args, **kwargs) -> str:
        """Build cache key."""
        return self.namespace

    def __call__(self, *args, **kwargs) -> str:
        """Build cache key."""
        return self.build_key(*args, **kwargs)

    def params(self, *args, **kwargs) -> dict:
        """Build cache key."""
        return self.dict(exclude_unset=True)

    @abc.abstractmethod
    async def adelete_cache(self):
        """
        Delete cache.

        This method only deletes cache on the server side.
        Client cache headers will not be affected in any way.
        """
        pass

    def delete_cache(self):
        """Delete cache."""
        return async_to_sync(self.adelete_cache)()


class EndpointCacheParams(CacheParams):
    """Cache params for the application."""

    expire: int
    key_builder: Optional[Callable]

    async def adelete_cache(self):
        """Delete cache."""
        redis_backend: RedisBackend = await get_fastapi_cache_backend()
        await redis_backend.clear(namespace=self.build_key())


class ServiceCacheParams(CacheParams):
    """Cache params for the application."""

    timeout: int

    def build_key(self, *args, **kwargs) -> str:
        """Build cache key."""
        return self.namespace.format(**kwargs)

    async def adelete_cache(self):
        """Delete cache."""
        await cache.adelete(self.build_key())

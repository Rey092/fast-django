# -*- coding: utf-8 -*-
"""Key builders for caches."""
from typing import Optional

from fastapi_cache import FastAPICache
from starlette.requests import Request
from starlette.responses import Response


async def test_key_builder(
    func,
    namespace: Optional[str] = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    """
    Build cache key for videos.

    This function is used as a key builder for the videos list endpoint.
    Pagination params are used as a part of the cache key.
    Video query params are used as a part of the cache key.
    Only a few keys from the user payload are used as a part of the cache key
    cuz they are affecting the videos list schema.
    """
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    return cache_key

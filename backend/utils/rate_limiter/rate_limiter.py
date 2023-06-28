# -*- coding: utf-8 -*-
"""Rate limiter module."""
from typing import Callable, Optional

from django.conf import settings
from fastapi_limiter import FastAPILimiter
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from utils.responses import DefaultHTTPException


async def rate_limit_callback(request: Request, response: Response, pexpire: int):  # noqa
    """Raise callback when too many requests."""
    raise RateLimitException


class RateLimiter:
    """Rate limit decorator."""

    def __init__(
        self,
        times: int = 1,
        milliseconds: int = 0,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        identifier: Optional[Callable] = None,
        callback: Optional[Callable] = None,
    ):
        """Rate limit decorator init."""
        self.times = times
        self.milliseconds = milliseconds + 1000 * seconds + 60000 * minutes + 3600000 * hours
        self.identifier = identifier
        self.callback = callback

    async def __call__(self, request: Request, response: Response):
        """
        Rate limit decorator.
        """
        if not FastAPILimiter.redis:
            raise Exception("You must call FastAPILimiter.init in startup event of fastapi!")
        index = 0
        for route in request.app.routes:
            if route.path == request.scope["path"]:
                for idx, dependency in enumerate(route.dependencies):
                    if self is dependency.dependency:
                        index = idx
                        break
        # moved here because constructor run before app startup
        identifier = self.identifier or FastAPILimiter.identifier
        callback = self.callback or rate_limit_callback
        redis = FastAPILimiter.redis
        rate_key = await identifier(request)
        key = f"{FastAPILimiter.prefix}:{rate_key}:{index}"
        keys = [key]
        pexpire = await redis.evalsha(FastAPILimiter.lua_sha, len(keys), *keys, self.times, self.milliseconds)
        if pexpire != 0 and settings.LIMIT_ACTIVE:
            return await callback(request, response, pexpire)


class RateLimitException(DefaultHTTPException):
    """Raise when too many requests."""

    error = "RATE_LIMIT"
    message = "Too many requests"
    status_code = HTTP_429_TOO_MANY_REQUESTS

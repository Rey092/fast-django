# -*- coding: utf-8 -*-
import logging
import nest_asyncio
import pytest
from asgi_lifespan import LifespanManager
from config.asgi import fastapp
from django.conf import settings
from fastapi import FastAPI
from httpx import AsyncClient

nest_asyncio.apply()

logger = logging.getLogger(__name__)


@pytest.fixture
async def fastapi_app() -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.

    """
    # await ProjectInitialization().start(app=app)
    return fastapp


@pytest.fixture
async def client(fastapi_app: FastAPI) -> AsyncClient:
    """
    Fixture for creating HTTP client.

    :param fastapi_app: FastAPI app.
    :return: HTTPX async client.

    """
    async with LifespanManager(fastapi_app):
        async with AsyncClient(app=fastapi_app, base_url=settings.BACKEND_URL) as client:
            yield client

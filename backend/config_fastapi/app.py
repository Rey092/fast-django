# -*- coding: utf-8 -*-
"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""
import os
import pathlib
from pathlib import Path

from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from utils.logger.logger import CustomizeLogger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
app_fastapi = FastAPI(
    docs_url="/"
)


def init_logging() -> None:
    """Initialize logging."""
    config_path = pathlib.Path(__file__).parent.with_name("logging_config.json")
    CustomizeLogger.make_logger(config_path)


def register_routers(app):
    """Register routers."""
    pass


def init(app: FastAPI):
    """App initialization function."""
    register_routers(app)

    if settings.MOUNT_DJANGO_APP:
        app.mount("/django", application)  # type:ignore

        static_directory = "staticfiles"
        Path(static_directory).mkdir(parents=True, exist_ok=True)
        app.mount("/staticfiles", StaticFiles(directory=static_directory), name="static")


init(app_fastapi)

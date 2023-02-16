# -*- coding: utf-8 -*-
"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/
"""
import os
from pathlib import Path

from django.conf import settings
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
fastapp = FastAPI()


def register_routers(app):
    from src.video_tags.endpoints import tags_router

    app.include_router(tags_router)


def init(app: FastAPI):
    """App initialization function."""
    # from polls.routers import register_routers

    register_routers(app)

    if settings.MOUNT_DJANGO_APP:
        app.mount("/django", application)  # type:ignore

        static_directory = "staticfiles"
        Path(static_directory).mkdir(parents=True, exist_ok=True)
        app.mount("/static", StaticFiles(directory=static_directory), name="static")


init(fastapp)

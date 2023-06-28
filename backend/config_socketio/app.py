"""ASGI config for config_socketio project."""

import os

import socketio
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

sio = socketio.AsyncServer(async_mode='asgi')
app_socketio = socketio.ASGIApp(sio)

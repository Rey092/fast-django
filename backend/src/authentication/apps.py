# -*- coding: utf-8 -*-
"""Authentication app."""
from django.apps import AppConfig


class AuthConfig(AppConfig):
    """Authentication app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.authentication"
    verbose_name = "Аутентификация"

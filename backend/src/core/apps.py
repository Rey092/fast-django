# -*- coding: utf-8 -*-
"""Core app."""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Core app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"

    def ready(self):
        """Wire dependencies on app ready."""
        from src.core.registry import registry

        registry.wire()

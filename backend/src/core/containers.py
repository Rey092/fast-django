# -*- coding: utf-8 -*-
"""User containers module."""
from dependency_injector import containers, providers

from src.core.services.image import ImageService


class CoreContainer(containers.DeclarativeContainer):
    """User container."""

    image_service: providers.Singleton[ImageService] = providers.Singleton(
        ImageService,
    )

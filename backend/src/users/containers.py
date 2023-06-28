# -*- coding: utf-8 -*-
"""User containers module."""
from dependency_injector import containers, providers

from src.core.containers import CoreContainer
from src.users.repositories import UserRepository
from src.users.services import UserService


class UserContainer(containers.DeclarativeContainer):
    """User container."""

    user_repository: UserRepository = providers.Singleton(
        UserRepository,
    )

    user_service: UserService = providers.Singleton(
        UserService,
        user_repository=user_repository,
        image_service=CoreContainer.image_service,
    )

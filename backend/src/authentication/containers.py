# -*- coding: utf-8 -*-
"""User containers module."""

from dependency_injector import containers, providers
from django.conf import settings

from src.authentication.repositories import CaptchaRepository
from src.authentication.repositories.password_token_repository import \
    PasswordTokenRepository
from src.authentication.services import (AuthService, CaptchaService,
                                         JWTService, PasswordService)
from src.users.containers import UserContainer


class AuthContainer(containers.DeclarativeContainer):
    """Auth container."""

    captcha_repository = providers.Singleton(
        CaptchaRepository,
    )

    captcha_service = providers.Singleton(
        CaptchaService,
        captcha_repository=captcha_repository,
    )
    jwt_service = providers.Singleton(
        JWTService,
        access_expiration=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        refresh_expiration=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        jwt_secret_key=settings.SECRET_KEY,
        jwt_algorithm=settings.JWT_ALGORITHM,
    )
    password_token_repository = providers.Singleton(
        PasswordTokenRepository,
    )
    password_service = providers.Singleton(
        PasswordService,
        password_token_repository=password_token_repository,
    )
    auth_service = providers.Singleton(
        AuthService,
        user_service=UserContainer.user_service,
        captcha_service=captcha_service,
        jwt_service=jwt_service,
        password_service=password_service,
    )

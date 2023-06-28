# -*- coding: utf-8 -*-
"""Authentication dependencies."""
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from src.authentication.schemas.auth import UserPayload
from src.core.registry import Registry
from utils.responses.http.auth import (InvalidCredentialsException,
                                       UnauthorizedException)
from utils.security.dependencies import (jwt_http_bearer,
                                         jwt_http_bearer_no_error)


@inject
async def get_user_payload(
    jwt_service=Depends(Provide[Registry.authentication.jwt_service]),
    bearer: Optional[str] = Depends(jwt_http_bearer_no_error),
) -> Optional[UserPayload]:
    """Get user payload from JWT token."""
    if bearer:
        if token := bearer.credentials:  # noqa
            if data := await jwt_service.decode_token(token):
                return UserPayload(**data)
            raise InvalidCredentialsException()

    return None


@inject
async def get_authenticated_user_payload(
    jwt_service=Depends(Provide[Registry.authentication.jwt_service]),
    bearer: str = Depends(jwt_http_bearer),
) -> UserPayload:
    """Get authenticated user payload."""
    if token := bearer.credentials:  # noqa
        if data := await jwt_service.decode_token(token):
            return UserPayload(**data)
        raise InvalidCredentialsException()
    raise UnauthorizedException()

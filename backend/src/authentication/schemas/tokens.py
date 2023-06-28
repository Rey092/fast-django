# -*- coding: utf-8 -*-
"""Token schemas."""
from src.authentication.schemas.auth import UserPayload
from utils.schemas.base import DjangoSchema


class AccessTokenSchema(DjangoSchema):
    """
    Access token schema.
    """

    access: str


class RefreshTokenSchema(DjangoSchema):
    """
    Refresh token schema.
    """

    refresh: str


class AccessRefreshTokensSchema(AccessTokenSchema, RefreshTokenSchema):
    """
    Access and refresh token schema.
    """


class UserLoginRegisterResponseSchema(UserPayload):
    """
    User login register response schema.
    """

    tokens: AccessRefreshTokensSchema

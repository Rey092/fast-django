# -*- coding: utf-8 -*-
"""Exceptions module."""
from starlette import status

from .base import DefaultHTTPException


class UnauthorizedException(DefaultHTTPException):
    """Exception raised when the user is not authenticated."""

    error = "UNAUTHORIZED"
    message = "Credentials were not provided."
    status_code = status.HTTP_403_FORBIDDEN


class InvalidCredentialsException(DefaultHTTPException):
    """Exception raised when the user provides invalid credentials."""

    error = "LOGIN_BAD_CREDENTIALS"
    message = "Invalid credentials."
    status_code = status.HTTP_401_UNAUTHORIZED


class InsufficientRightsException(DefaultHTTPException):
    """Exception raised when the user does not have the required rights to perform an action."""

    error = "INSUFFICIENT_RIGHTS"
    message = "Insufficient rights to perform this action."
    status_code = status.HTTP_403_FORBIDDEN

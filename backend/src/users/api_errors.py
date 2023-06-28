# -*- coding: utf-8 -*-
"""Exceptions raised by users app."""
from starlette import status

from utils.responses import DefaultHTTPException


class AvatarTooBigException(DefaultHTTPException):
    """Exception raised when user tries to set avatar that is too big."""

    error = "AVATAR_TOO_BIG"
    message = "Avatar is too big. Max size is 10MB"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidImageException(DefaultHTTPException):
    """Exception raised when user tries to set avatar that is not image."""

    error = "INVALID_IMAGE"
    message = "File is not an image"
    status_code = status.HTTP_400_BAD_REQUEST


class EmailAlreadyExistsException(DefaultHTTPException):
    """Exception raised when user tries to register with already existing email."""

    error = "EMAIL_ALREADY_EXISTS"
    message = "Email already exists"
    status_code = status.HTTP_400_BAD_REQUEST

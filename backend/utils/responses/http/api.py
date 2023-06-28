# -*- coding: utf-8 -*-
"""Exceptions module."""
from starlette import status

from utils.responses import DefaultHTTPException


class NotFoundException(DefaultHTTPException):
    """Exception raised when the requested resource was not found."""

    error = "NOT_FOUND"
    message = "The requested resource was not found."
    status_code = status.HTTP_404_NOT_FOUND

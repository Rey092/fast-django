# -*- coding: utf-8 -*-
"""Authentication exceptions."""
from starlette import status

from utils.responses import DefaultHTTPException


class RegisterUserAlreadyExistsException(DefaultHTTPException):
    """Exception raised when the user already exists."""

    error = "REGISTER_USER_ALREADY_EXISTS"
    message = "User already exists"
    status_code = status.HTTP_400_BAD_REQUEST


class RegisterInvalidEmailException(DefaultHTTPException):
    """Exception raised when the email is invalid."""

    error = "REGISTER_INVALID_EMAIL"
    message = "Invalid email"
    status_code = status.HTTP_400_BAD_REQUEST


class NewPasswordInvalidTokenException(DefaultHTTPException):
    """Exception raised when the token is invalid."""

    error = "NEW_PASSWORD_INVALID_TOKEN"
    message = "Invalid token"
    status_code = status.HTTP_400_BAD_REQUEST


class ChangePasswordInvalidOldPasswordException(DefaultHTTPException):
    """Exception raised when the old password is invalid."""

    error = "CHANGE_PASSWORD_INVALID_OLD_PASSWORD"
    message = "Invalid old password"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidCaptchaException(DefaultHTTPException):
    """Exception raised when the captcha is invalid."""

    error = "REGISTER_INVALID_CAPTCHA"
    message = "Invalid captcha"
    status_code = status.HTTP_400_BAD_REQUEST


class NoFreeNicknameNumberException(DefaultHTTPException):
    """Exception raised when there is no free nickname."""

    error = "NO_FREE_NICKNAME"
    message = "No free number available for this nickname"
    status_code = status.HTTP_400_BAD_REQUEST

# -*- coding: utf-8 -*-
"""This module contains all the repositories for the authentication module."""
from .captcha_repository import CaptchaRepository
from .password_token_repository import PasswordTokenRepository

__all__ = [
    "CaptchaRepository",
    "PasswordTokenRepository",
]

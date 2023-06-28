# -*- coding: utf-8 -*-
"""ChangePassword schema module."""
from pydantic import Field

from src.authentication.schemas.registration import PasswordValidationMixin
from utils.schemas.base import DjangoSchema


class ChangePasswordSchema(PasswordValidationMixin, DjangoSchema):
    """ChangePassword base schema."""

    old_password: str = Field(
        min_length=8,
        max_length=30,
    )
    password: str = Field(
        description="From 8 to 30 characters long. "
        "At least one lowercase and uppercase characters. "
        "At least one number."
        "^(?=.{8,30}) (?=.*[a-z])(?=.*[A-Z]) (?=.*[0-9]) - regexes",
        min_length=8,
        max_length=30,
    )
    password_repeat: str = Field(
        min_length=8,
        max_length=30,
    )

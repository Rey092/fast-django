# -*- coding: utf-8 -*-
"""Registration schemas."""
import re
from random import choice

import rstr
from pydantic import Field, validator
from pydantic_factories import ModelFactory

from src.authentication.entities import PASSWORD_CHECKS
from src.authentication.schemas.auth import BaseAuthSchema
from src.authentication.schemas.captchas import CaptchaVerifySchema


class PasswordValidationMixin:
    """Password validation mixin."""

    @validator("password")
    def check_password(cls, value):
        """Check password strength. All checks are done in the separate regex each."""
        for check in PASSWORD_CHECKS:
            if not re.match(check["regex"], value):
                raise ValueError(check["message"])
        return value

    @validator("password_repeat")
    def check_password_repeat(cls, value, values):
        """Check if password and password_repeat are the same."""
        password = values.get("password")
        if password and values["password"] != value:
            raise ValueError("Passwords do not match")
        return value


class UserRegisterSchema(PasswordValidationMixin, BaseAuthSchema):
    """
    This schema is used for creating a new user.
    """

    nickname: str = Field(
        description=r"Nickname should contain only letters, numbers and space. From 4 to 20 characters long.",
        min_length=4,
        max_length=20,
        regex="^[a-zA-Z0-9 ]{4,20}$",
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
    captcha: CaptchaVerifySchema

    @validator("email")
    def lowercase_email(cls, value):
        """Lowercase email."""
        return value.lower()

    class Config(BaseAuthSchema.Config):
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "nickname": "Nick",
                "password": "Pass12345",
                "passwordRepeat": "Pass12345",
                "captcha": {
                    "challenge": "325a81b4-ad65-4cdc-b965-a6fa4f30200a",
                    "response": "loremipsum",
                },
            },
        }


class UserRegisterFactory(ModelFactory):
    """User register factory."""

    __model__ = UserRegisterSchema

    nickname = lambda: rstr.xeger(r"^[a-za-z0-9 ]{4,20}$")  # noqa
    password = lambda: choice(["Pass12345", "Pass12345", "Pass12345"])  # noqa
    password_repeat = password

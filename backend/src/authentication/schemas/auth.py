# -*- coding: utf-8 -*-
"""Authentication schemas module."""
from pydantic import EmailStr, Field

from utils.schemas.base import DjangoSchema


class BaseAuthSchema(DjangoSchema):
    """Base user schema."""

    email: EmailStr = Field(description="The user's email. Unique.")

    def create_update_dict(self):
        """Create a dictionary to update the user."""
        return self.dict(
            exclude_unset=True,
            exclude={
                "id",
                "is_active",
            },
        )


class UserLoginSchema(BaseAuthSchema):
    """
    Class to check the user in the /login endpoint.
    """

    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "pass12345",
            },
        }


class UserPayload(BaseAuthSchema):
    """
    User token payload schema.

    After we check user credentials, we decode the access token and get
    the payload.

    """

    id: int
    email: EmailStr
    nickname: str
    nickname_number: int
    is_active: bool
    is_premium: bool
    is_censorship_enabled: bool
    is_language_english: bool
    is_thumbnail_modern: bool

    class Config:
        frozen = True

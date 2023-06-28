# -*- coding: utf-8 -*-
"""Captcha schemas."""
from utils.schemas.base import DjangoSchema


class CaptchaChallengeSchema(DjangoSchema):
    """Captcha schema with challenge."""

    challenge: str
    image_base64: str


class CaptchaVerifySchema(DjangoSchema):
    """Captcha schema with challenge solution to verify."""

    challenge: str
    response: str

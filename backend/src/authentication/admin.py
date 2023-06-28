# -*- coding: utf-8 -*-
"""Authentication admin module."""

from django.contrib import admin

from src.authentication.models import CaptchaChallenge, PasswordToken


@admin.register(CaptchaChallenge)
class CaptchaChallengeAdmin(admin.ModelAdmin):
    """Admin for CaptchaChallenge model."""

    list_display = [
        "challenge",
        "response",
        "date_created",
    ]


@admin.register(PasswordToken)
class PasswordTokenAdmin(admin.ModelAdmin):
    """Admin for PasswordToken model."""

    list_display = [
        "email",
        "token_hash",
        "new_password",
        "date_created",
        "date_updated",
    ]

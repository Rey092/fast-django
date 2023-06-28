# -*- coding: utf-8 -*-
"""Authentication models."""
from django.db import models


class CaptchaChallenge(models.Model):
    """Captcha challenge model. Used for captcha verification."""

    challenge = models.CharField(max_length=255, unique=True)
    response = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of captcha challenge."""
        return self.challenge

    class Meta:
        """Meta class."""

        verbose_name = "Задание капчи"
        verbose_name_plural = "Задания капчи"


class PasswordToken(models.Model):
    """Password token model. Used for password reset."""

    email = models.EmailField(unique=True)
    token_hash = models.CharField(max_length=1024)
    new_password = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class."""

        verbose_name = "Токен пароля"
        verbose_name_plural = "Токены паролей"

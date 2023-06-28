# -*- coding: utf-8 -*-
"""User models module."""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone

from utils.models.magic_image import MagicImageField


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(max_length=255, unique=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    avatar = MagicImageField(
        size=[140, 140],
        crop=["middle", "center"],
        quality=95,
        upload_to="users/avatars/",
        null=True, blank=True
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        """Return string representation."""
        return self.email

    class Meta:
        ordering = ("-date_created",)
        verbose_name = "Юзер"
        verbose_name_plural = "Юзеры"

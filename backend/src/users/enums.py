# -*- coding: utf-8 -*-
"""User enums."""
from django.db import models


class PremiumType(models.TextChoices):
    """User premium type."""

    PATREON = "patreon", "Patreon"
    COINS = "coins", "Coins"


class PremiumIcon(models.TextChoices):
    """Patreon pledge icon."""

    CROWN = "crown"
    SWORD = "sword"
    STAR = "star"
    SKULL = "skull"


class AchievementType(models.TextChoices):
    """Achievement type."""

    ORIGIN = "origin", "Origin"
    ENJOYER = "enjoyer", "Enjoyer"  # TODO: №2 - Поставил 100 лайков
    CHATTY_CATHY = "chatty_cathy", "Chatty Cathy"  # TODO: №3 - Оставил 100 комментариев
    HENTAI_FAN = "hentai_fan", "Hentai Fan"  # TODO: №4 - Просмотрел 100 видео
    HAREM_MASTER = "harem_master", "Harem Master"  # TODO: №5 - Просмотрел 1000 видео
    PROTAGONIST = "protagonist", "Protagonist"  # TODO: №6 - Купил премиум первый раз

# -*- coding: utf-8 -*-
"""Video Tags models module."""
from django.db import models


class VideoTag(models.Model):
    """Video Tag model."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """Return Video Tag name as representation."""
        return self.name

# -*- coding: utf-8 -*-
"""Users admin module."""
from django.contrib import admin

from src.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """User admin."""

    list_display = ["email", "is_staff", "is_active", "date_created"]
    list_filter = ["is_staff", "is_active"]
    search_fields = ["email"]
    readonly_fields = ["date_created"]
    ordering = ["-date_created"]
    inlines = []
    exclude = [
        "groups",
        "user_permissions",
    ]

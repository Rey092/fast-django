# -*- coding: utf-8 -*-
"""User repository module."""
from src.users.models import User
from utils.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    """User repository."""

    def __init__(self):
        """Initialize user repository."""
        self.model = User

    def get_profile(self, user_id: int):
        """Get user profile."""
        return self.get_one(id=user_id)

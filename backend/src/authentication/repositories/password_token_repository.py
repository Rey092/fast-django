# -*- coding: utf-8 -*-
"""Password token repository."""
from typing import Optional

from src.authentication.models import PasswordToken
from utils.repositories import BaseRepository


class PasswordTokenRepository(BaseRepository):
    """Password token repository."""

    def __init__(self):
        """Initiate password token repository."""
        self.model = PasswordToken

    async def update_or_create_token(
        self,
        email: str,
        token_hash: str,
        new_password: str,
    ) -> tuple[PasswordToken, bool]:
        """Update or create password token."""
        return await self.model.objects.aupdate_or_create(
            email=email,
            defaults={"token_hash": token_hash, "new_password": new_password},
        )

    async def get_one_by_email(self, email: str) -> Optional[PasswordToken]:
        """Get password token by email."""
        return await self.model.objects.filter(email=email).afirst()

    async def get_one_by_token_hash(self, token_hash: str) -> Optional[PasswordToken]:
        """Get password token by token hash."""
        return await self.model.objects.filter(token_hash=token_hash).afirst()

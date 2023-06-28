# -*- coding: utf-8 -*-
"""Password service module."""
import hashlib
from typing import Optional, Tuple

from django.contrib.auth.hashers import make_password
from passlib import pwd
from passlib.pwd import genword

from src.authentication.models import PasswordToken
from src.authentication.repositories.password_token_repository import \
    PasswordTokenRepository
from src.users.models import User
from utils.services import BaseService


class PasswordService(BaseService):
    """Password service."""

    repository: PasswordTokenRepository

    def __init__(self, password_token_repository: PasswordTokenRepository):
        """Init password service."""
        self.repository = password_token_repository

    @staticmethod
    def check_password(
        user: User,
        raw_password: str,
    ) -> bool:
        """Check password."""
        return user.check_password(raw_password)

    @staticmethod
    def set_password(user: User, raw_password: str) -> User:
        """Set password."""
        user.set_password(raw_password)
        return user

    @staticmethod
    def hash_password(raw_password: str) -> str:
        """Hash password."""
        password = make_password(raw_password)
        return password

    @staticmethod
    def hash_token(string: str) -> str:
        """Hash token."""
        return hashlib.sha256(string.encode()).hexdigest()

    @staticmethod
    def generate_password(length=14) -> str:
        """Generate password."""
        return pwd.genword(length=length)

    @staticmethod
    def generate_token(length=255) -> str:
        """Generate token."""
        return pwd.genword(length=length)

    async def get_one_by_token_hash(self, token_hash) -> Optional[PasswordToken]:
        """Get password token by token hash."""
        password_token = await self.repository.get_one_by_token_hash(token_hash)
        return password_token

    async def generate_password_token(self, email: str) -> Tuple[str, str]:
        """Request new password."""
        token = self.generate_token()
        token_hash = self.hash_token(token)
        new_password = self.generate_password()
        await self.repository.update_or_create_token(
            email=email,
            token_hash=token_hash,
            new_password=new_password,
        )
        return new_password, token

    @staticmethod
    async def _create_random_string(length=255) -> str:
        return genword(length=length)

# -*- coding: utf-8 -*-
"""User service module."""
from django.core.files import File
from fastapi import UploadFile

from src.core.services.image import ImageService
from src.users.api_errors import AvatarTooBigException
from src.users.models import User
from src.users.repositories import UserRepository
from src.users.schemas.profile import ProfileUpdateSchema
from utils.services import BaseService


class UserService(BaseService):
    """User service."""

    def __init__(
        self,
        user_repository: UserRepository,
        image_service: ImageService,
    ):
        """Initialize user service."""
        self.repository: UserRepository = user_repository
        self.image_service: ImageService = image_service
        self.avatar_max_size: int = 1024 * 1024 * 10  # 10 MB

    async def get_profile(self, user_id: int):
        """Get user profile."""
        user: User = await self.repository.get_one(id=user_id)
        return user

    async def create_user(self, email: str, password: str, nickname: str, nickname_number: str, slug: str):
        """Create user."""
        # create user object
        user = User(
            slug=slug,
            email=email,
        )

        # set password
        user.set_password(password)

        # save user
        return await self.repository.save_one(user)

    async def update_user_password(self, user: User, new_password: str):
        """Update user password."""
        user.set_password(new_password)
        return await self.repository.save_one(user)

    async def patch_profile(self, user_id: int, profile_update_schema: ProfileUpdateSchema) -> User:
        """Update user profile."""
        # get user
        user: User = await self.repository.get_one(id=user_id)

        # save user
        user: User = await self.repository.save_one(user)

        return user

    async def check_email_exists(self, email: str, exclude_id: int = None):
        """Check if email exists."""
        # get users with this email
        email_checked = await self.get_one(email=email, raise_not_found=False)
        email_patreon_checked = await self.get_one(email_patreon=email, raise_not_found=False)

        # check if email exists
        email_exists = email_checked and email_checked.id != exclude_id
        email_patreon_exists = email_patreon_checked and email_patreon_checked.id != exclude_id

        return email_exists or email_patreon_exists

    async def change_avatar(self, user_id: int, avatar: UploadFile) -> User:
        """Change user avatar."""
        # check avatar size
        if avatar.size > self.avatar_max_size:
            raise AvatarTooBigException

        # check if avatar is image or gif using pillow
        self.image_service.verify_image(avatar)

        # get user
        user: User = await self.repository.get_one_by_id(user_id)

        # save avatar
        user.avatar = File(avatar.file, name=avatar.filename)
        await self.repository.save_one(user)

        # get user profile
        user: User = await self.repository.get_profile(user_id)

        return user

    # async def update_last_login(self, user: User):
    #     """Update last login."""
    #     user.last_login = timezone.now()
    #     await self.repository.save_one(user)

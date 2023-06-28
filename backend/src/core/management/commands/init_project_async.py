# -*- coding: utf-8 -*-
"""Async Project initialization module."""
import logging

from asgi_lifespan import LifespanManager
from asgiref.sync import sync_to_async
from django.conf import settings
from faker import Faker

from src.authentication.schemas.registration import UserRegisterFactory
from src.users.models import User

logger = logging.getLogger(__name__)


class ProjectInitialization:
    """Project initialization."""

    faker: Faker = Faker()
    directory_vertical = "seed/vertical_thumbnails"
    directory_horizontal = "seed/horizontal_thumbnails"

    @classmethod
    async def start(cls, app, debug=settings.DEBUG):
        """Start project initialization."""
        async with LifespanManager(app):
            # run base setup
            await cls._create_superuser()

            # add seed data
            if debug:
                await cls._create_test_users()

    @classmethod
    async def _create_superuser(cls):
        """Create superuser."""
        user, created = await User.objects.aupdate_or_create(
            is_superuser=True,
            defaults={
                "email": settings.SUPERUSER_EMAIL,
                "is_staff": True,
                "is_active": True,
            },
        )
        user.set_password(settings.SUPERUSER_PASSWORD)
        await sync_to_async(user.save)()

    @classmethod
    async def _create_test_users(cls):
        """Create test users."""
        users_exists = await User.objects.filter(is_superuser=False).aexists()
        factory = UserRegisterFactory()

        if not users_exists:
            for i in range(10):
                data = factory.build().dict()

                if i == 0:
                    # change first users
                    data["email"] = "user@example.com"
                elif i == 1:
                    # change second users
                    data["email"] = "premiumuser@example.com"

                # load to django file random image from seed/vertical_thumbnails
                # thumbnail_vertical_filename = random.choice(os.listdir(cls.directory_vertical))
                # thumbnail_vertical = open(
                #     os.path.join(cls.directory_vertical, thumbnail_vertical_filename),
                #     "rb",
                # )

                # create user
                user = User(
                    email=data["email"],
                    # avatar=File(thumbnail_vertical),
                )
                user.set_password("pass12345")
                await sync_to_async(user.save)()

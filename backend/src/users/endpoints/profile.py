# -*- coding: utf-8 -*-
"""Profile endpoints."""
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, UploadFile
from starlette import status

from src.authentication.dependencies import get_authenticated_user_payload
from src.authentication.schemas.auth import UserPayload
from src.authentication.services import AuthService
from src.core.registry import Registry
from src.users.api_errors import AvatarTooBigException, InvalidImageException
from src.users.models import User
from src.users.schemas.profile import ProfileUpdateSchema
from src.users.services import UserService
from utils.responses.examples_generator import generate_examples

profile_router = APIRouter(prefix="/profile", tags=["Profile"])


@profile_router.get(
    "/",
    name="profile:get",
    summary="Get profile. Auth required.",
    description="Get profile. Auth required.",
    status_code=status.HTTP_200_OK,
    # response_model=UserProfileSchema,
    responses=generate_examples(
        auth=True,
    ),
)
@inject
async def get_profile(
    user_service: UserService = Depends(Provide[Registry.users.user_service]),
    user_payload: Optional[UserPayload] = Depends(get_authenticated_user_payload),
):
    """
    Return current user profile.
    """
    user: User = await user_service.get_profile(user_payload.id)
    return user


@profile_router.patch(
    "/",
    name="profile:patch_profile",
    summary="Update user profile. Auth required.",
    description="Update user profile. Auth required.",
    status_code=status.HTTP_200_OK,
    # response_model=UserProfileAndPayloadSchema,
    responses=generate_examples(
        auth=True,
    ),
)
@inject
async def update_profile(
    profile_update_schema: ProfileUpdateSchema,
    user_service: UserService = Depends(Provide[Registry.users.user_service]),
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
    user_payload: Optional[UserPayload] = Depends(get_authenticated_user_payload),  # noqa
):
    """
    Patch user profile.
    """
    user: User = await user_service.patch_profile(user_id=user_payload.id, profile_update_schema=profile_update_schema)
    user_payload = await auth_service.refresh_payload(
        user_id=user.id,
    )
    # return UserProfileAndPayloadSchema(profile=user, payload=user_payload)


@profile_router.put(
    "/avatar/",
    name="profile:change_avatar",
    summary="Change user avatar. Auth required.",
    description="Change user avatar. Auth required.",
    status_code=status.HTTP_200_OK,
    # response_model=UserProfileAndPayloadSchema,
    responses=generate_examples(
        AvatarTooBigException,
        InvalidImageException,
        auth=True,
    ),
)
@inject
async def change_avatar(
    avatar: UploadFile = File(...),
    user_service: UserService = Depends(Provide[Registry.users.user_service]),
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
    user_payload: Optional[UserPayload] = Depends(get_authenticated_user_payload),  # noqa
):
    """
    Change user avatar.
    """
    user: User = await user_service.change_avatar(
        user_id=user_payload.id,
        avatar=avatar,
    )
    user_payload: UserPayload = await auth_service.refresh_payload(
        user_id=user.id,
    )
    # return UserProfileAndPayloadSchema(profile=user, payload=user_payload)

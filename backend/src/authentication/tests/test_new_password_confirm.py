# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from asgiref.sync import sync_to_async
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient

from src.authentication.models import PasswordToken
from src.authentication.repositories import PasswordTokenRepository
from src.authentication.services import PasswordService
from src.users.models import User


@pytest.mark.anyio
async def test_new_password_confirm(
    fastapi_app: FastAPI, httpx: AsyncClient, faker: Faker, db: None, test_user: User
) -> None:
    """
    Test request new password.
    """
    password_service = PasswordService(
        password_token_repository=PasswordTokenRepository(),
    )
    new_password, token = await password_service.generate_password_token(email=test_user.email)

    # change password in password token
    password_token = await PasswordToken.objects.aget(email=test_user.email)
    password_token.new_password = new_password
    await sync_to_async(password_token.save)()

    # confirm new password
    url = fastapi_app.url_path_for("auth:confirm-password", token=token)
    response = await httpx.post(url)
    assert response.status_code == 200

    # password token should be deleted
    password_token = await PasswordToken.objects.filter(email=test_user.email).afirst()
    assert password_token is None

    # change password back
    test_user.set_password("pass12345")
    await sync_to_async(test_user.save)()

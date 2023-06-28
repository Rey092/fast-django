# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient

from src.authentication.schemas.registration import UserRegisterFactory
from src.users.models import User


@pytest.mark.anyio
async def test_register(fastapi_app: FastAPI, httpx: AsyncClient, faker: Faker, db: None) -> None:
    """
    Test refresh token.
    """
    factory = UserRegisterFactory()
    data = factory.build().dict()

    # Test register
    url = fastapi_app.url_path_for("auth:register")
    response = await httpx.post(url, json=data)
    assert response.status_code == 201

    user_id = response.json()["id"]
    user = await User.objects.aget(id=user_id)

    assert user is not None
    assert user.is_active is True
    assert user.is_superuser is False
    assert user.is_staff is False
    assert user.nickname == data["nickname"]
    assert user.email == data["email"]
    assert user.check_password(data["password"]) is True

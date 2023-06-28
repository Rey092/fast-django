# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient

from src.users.models import User


@pytest.mark.anyio
async def test_request_new_password(
    fastapi_app: FastAPI, httpx: AsyncClient, faker: Faker, db: None, test_user: User
) -> None:
    """
    Test request new password.
    """
    response = await httpx.post(f"/auth/request-new-password/{test_user.email}/")
    assert response.status_code == 200

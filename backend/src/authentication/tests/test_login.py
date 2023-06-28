# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.users.models import User


@pytest.mark.anyio
async def test_login(fastapi_app: FastAPI, httpx: AsyncClient, db: None, test_user: User) -> str:
    """
    Test get captcha.
    """
    data = {
        "email": test_user.email,
        "password": "pass12345",
    }
    response = await httpx.post("/auth/login/", json=data)
    print(data, response.json())

    assert response.status_code == 200
    assert response.json()["tokens"]["access"] is not None
    assert response.json()["tokens"]["refresh"] is not None

    return response.json()["tokens"]["refresh"]

# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.authentication.schemas.tokens import AccessRefreshTokensSchema
from src.users.models import User


@pytest.mark.anyio
async def test_refresh(
    fastapi_app: FastAPI,
    httpx: AsyncClient,
    db: None,
    test_user: User,
    test_user_tokens: AccessRefreshTokensSchema,
) -> None:
    """
    Test get captcha.
    """
    data = {
        "refresh": test_user_tokens.refresh,
    }
    url = fastapi_app.url_path_for("auth:refresh")
    response = await httpx.post(url, json=data)
    # print(response.json())

    assert response.status_code == 200
    assert response.json()["access"] is not None
    assert response.json()["refresh"] is not None

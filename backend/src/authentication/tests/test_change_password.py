# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.authentication.schemas.change_password import ChangePasswordSchema
from src.authentication.schemas.tokens import AccessRefreshTokensSchema


@pytest.mark.anyio
async def test_change_password(
    fastapi_app: FastAPI,
    httpx: AsyncClient,
    db: None,
    test_user_tokens: AccessRefreshTokensSchema,
) -> None:
    """
    Test refresh token.
    """
    data = ChangePasswordSchema(
        old_password="pass12345",
        password="pass12345",
        password_repeat="pass12345",
    )
    # Test register
    url = fastapi_app.url_path_for("auth:change_password")
    response = await httpx.post(
        url,
        json=data.dict(by_alias=True),
        headers={"Authorization": f"Bearer {test_user_tokens.access}"},
    )
    assert response.status_code == 200

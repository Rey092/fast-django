# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.authentication.models import CaptchaChallenge


@pytest.mark.anyio
async def test_captcha(fastapi_app: FastAPI, httpx: AsyncClient, db: None) -> None:
    """
    Test get captcha.
    """
    url = fastapi_app.url_path_for("captcha:get")
    response = await httpx.get(url)
    assert response.status_code == 201

    assert response.json()["challenge"] is not None
    assert response.json()["imageBase64"] is not None

    captcha_db = await CaptchaChallenge.objects.aget(challenge=response.json()["challenge"])

    assert captcha_db is not None

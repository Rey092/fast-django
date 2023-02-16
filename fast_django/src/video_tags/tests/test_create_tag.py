# -*- coding: utf-8 -*-
"""Create tags test."""
import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.video_tags.models import VideoTag


@pytest.mark.asyncio
async def test_user_refresh(
    fastapi_app: FastAPI,
    client: AsyncClient,
    db: None
) -> None:
    """
    Test refresh token.
    """
    await VideoTag.objects.acreate(name="gas", slug="fas")
    print(await VideoTag.objects.afirst())

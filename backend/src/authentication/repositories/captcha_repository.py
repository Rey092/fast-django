# -*- coding: utf-8 -*-
"""Captcha repository."""
from typing import Optional

from src.authentication.models import CaptchaChallenge
from utils.repositories import BaseRepository


class CaptchaRepository(BaseRepository):
    """Captcha repository."""

    def __init__(self):
        """Initiate captcha repository."""
        self.model = CaptchaChallenge

    async def get_one_by_challenge_and_response(self, challenge: str, response: str) -> Optional[CaptchaChallenge]:
        """Get captcha challenge by challenge and response."""
        return await self.model.objects.filter(challenge=challenge, response=response).afirst()

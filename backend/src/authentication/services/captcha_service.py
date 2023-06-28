# -*- coding: utf-8 -*-
"""Captcha service."""
import base64
import random
import uuid
from typing import Optional, Tuple

from django.conf import settings
from django.utils import timezone

from src.authentication.models import CaptchaChallenge
from src.authentication.repositories import CaptchaRepository
from src.authentication.schemas.captchas import CaptchaVerifySchema
from utils.services import BaseService


class CaptchaService(BaseService):
    """Captcha service."""

    words1 = [
        "b",
    ]
    words2 = [
        "a",
    ]

    def __init__(self, captcha_repository: CaptchaRepository):
        """Initialize captcha service."""
        from captcha.image import ImageCaptcha
        self.captcha = ImageCaptcha(width=410, height=140)
        self.captcha_repository = captcha_repository

    def generate_captcha_text(self):
        """Generate captcha text."""
        # get 3 random words from self.words
        word1 = random.choice(self.words1)
        word2 = random.choice(self.words2)
        result = word1 + word2

        return result

    async def create_challenge(self) -> Tuple[CaptchaChallenge, str]:
        """Create captcha challenge."""
        captcha_text = self.generate_captcha_text()
        image = self.captcha.generate(captcha_text)
        image_base64 = base64.b64encode(image.getvalue()).decode("utf-8")
        captcha_challenge = CaptchaChallenge(challenge=str(uuid.uuid4()), response=captcha_text)
        captcha_challenge: CaptchaChallenge = await self.captcha_repository.save_one(captcha_challenge)
        return captcha_challenge, image_base64

    async def verify_captcha(self, captcha: CaptchaVerifySchema) -> tuple[bool, Optional[CaptchaChallenge]]:
        """Verify if given captcha is valid."""
        # Return true if super captcha entered
        if captcha.response == settings.CAPTCHA_SUPER_RESPONSE:
            return True, None

        # get challenge
        captcha_challenge: CaptchaChallenge = await self.captcha_repository.get_one_by_challenge_and_response(
            challenge=captcha.challenge, response=captcha.response
        )

        # if challenge is found and response is correct
        if captcha_challenge:
            # delete challenge
            captcha_challenge_created_at = captcha_challenge.created_at

            # if challenge is older than 60 minutes
            if captcha_challenge_created_at < timezone.now() - timezone.timedelta(minutes=60):
                return False, captcha_challenge

            # if challenge is correct
            return True, captcha_challenge

        # if challenge is not found or response is not correct
        return False, None


#
#
# if __name__ == "__main__":
#     image = ImageCaptcha(width=410, height=140)
#     data = image.generate("loremipsum")
#     image.write("loremipsum", "out.png")

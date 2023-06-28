# -*- coding: utf-8 -*-
"""JWT Service module."""
import logging
from datetime import datetime, timedelta
from typing import Optional

import jwt

from src.authentication.schemas.tokens import AccessRefreshTokensSchema
from utils.services import BaseService

logger = logging.getLogger(__name__)


class JWTService(BaseService):
    """Set up the JWT Backend with the given cache backend and private key."""

    def __init__(
        self,
        access_expiration: int,
        refresh_expiration: int,
        jwt_secret_key: str,
        jwt_algorithm: str,
    ):
        """Initialize the JWT Backend."""
        self.access_expiration = access_expiration
        self.refresh_expiration = refresh_expiration
        self._jwt_secret_key = jwt_secret_key
        self._jwt_algorithm = jwt_algorithm

    async def decode_token(self, token: str, leeway: int = 0) -> Optional[dict]:
        """Decode a token."""
        if token:
            try:
                payload = jwt.decode(
                    token,
                    self._jwt_secret_key,
                    leeway=leeway,
                    algorithms=self._jwt_algorithm,
                )
                return payload
            except Exception as e:
                logger.warning(e)
                return None
        return None

    def _create_token(
        self,
        payload: dict,
        token_type: str,
        expiration_delta: Optional[int] = None,
    ) -> str:
        """Create a token with the given payload and expiration delta."""
        iat = datetime.utcnow()
        if expiration_delta:
            exp = datetime.utcnow() + timedelta(seconds=expiration_delta)
        else:
            exp = datetime.utcnow() + timedelta(seconds=60)

        payload |= {"iat": iat, "exp": exp, "type": token_type}
        token = jwt.encode(payload=payload, key=self._jwt_secret_key, algorithm=self._jwt_algorithm)
        if isinstance(token, bytes):
            # For PyJWT <= 1.7.1
            return token.decode("utf-8")
        # For PyJWT >= 2.0.0a1
        return token

    def create_access_token(self, payload: dict) -> str:
        """Create an access token with the given payload."""
        return self._create_token(payload, "access", self.access_expiration)

    def create_refresh_token(self, payload: dict) -> str:
        """Create a refresh token with the given payload."""
        return self._create_token(payload, "refresh", self.refresh_expiration)

    def create_tokens(self, payload: dict) -> AccessRefreshTokensSchema:
        """Create access and refresh tokens."""
        access = self.create_access_token(payload)
        refresh = self.create_refresh_token(payload)

        return AccessRefreshTokensSchema(access=access, refresh=refresh)

# -*- coding: utf-8 -*-
"""Security base module."""
from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request

from utils.responses.http.auth import UnauthorizedException


class JwtHTTPBearer(HTTPBearer):
    """JWT HTTP Bearer dependency."""

    async def __call__(
        self,
        request: Request,
    ) -> Optional[HTTPAuthorizationCredentials]:
        """Call method."""
        authorization: str = request.headers.get("Authorization")
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise UnauthorizedException()
            else:
                return None
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise UnauthorizedException("Invalid authentication format")
            else:
                return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)

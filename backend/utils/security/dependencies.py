# -*- coding: utf-8 -*-
"""Security dependencies module."""
from utils.security.base import JwtHTTPBearer

jwt_http_bearer = JwtHTTPBearer()
jwt_http_bearer_no_error = JwtHTTPBearer(auto_error=False)

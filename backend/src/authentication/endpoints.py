# -*- coding: utf-8 -*-
"""Authentication endpoints module."""
from dependency_injector.wiring import Provide, inject
from django.conf import settings
from fastapi import APIRouter, Depends, status
from pydantic import EmailStr
from starlette.background import BackgroundTasks

from src.authentication.api_errors import (InvalidCaptchaException,
                                           NewPasswordInvalidTokenException,
                                           NoFreeNicknameNumberException,
                                           RegisterInvalidEmailException,
                                           RegisterUserAlreadyExistsException)
from src.authentication.dependencies import get_authenticated_user_payload
from src.authentication.schemas.auth import UserLoginSchema, UserPayload
from src.authentication.schemas.captchas import CaptchaChallengeSchema
from src.authentication.schemas.change_password import ChangePasswordSchema
from src.authentication.schemas.registration import UserRegisterSchema
from src.authentication.schemas.tokens import (AccessRefreshTokensSchema,
                                               RefreshTokenSchema,
                                               UserLoginRegisterResponseSchema)
from src.authentication.services import AuthService, CaptchaService
from src.core.registry import Registry
from utils.rate_limiter import RateLimiter, RateLimitException
from utils.responses.examples_generator import generate_examples
from utils.responses.http.auth import InvalidCredentialsException
from utils.responses.http.success import SuccessResponse

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(
    "/register/",
    name="auth:register",
    summary="Register a new user. Rate limited.",
    description="Register a new user with given data. Use /captcha to get captcha challenge. Rate limited.",
    status_code=status.HTTP_201_CREATED,
    response_model=UserLoginRegisterResponseSchema,
    responses=generate_examples(
        NoFreeNicknameNumberException,
        RegisterUserAlreadyExistsException,
        RegisterInvalidEmailException,
        InvalidCaptchaException,
        RateLimitException,
    ),
)
@inject
async def register(
    user_create_schema: UserRegisterSchema,
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
    dependencies=Depends(  # noqa
        RateLimiter(
            times=settings.LIMIT_REGISTER_TIMES,
            seconds=settings.LIMIT_REGISTER_SECONDS,
        ),
    ),
):
    """
    Register a new user with given data.
    """
    user_data, tokens = await auth_service.register_user(user_register_schema=user_create_schema)
    return UserLoginRegisterResponseSchema(**user_data, tokens=tokens)


@auth_router.post(
    "/login/",
    name="auth:login",
    summary="Login to the application. Rate limited.",
    description="Login endpoint to get access and refresh tokens. Rate limited.",
    status_code=status.HTTP_200_OK,
    response_model=UserLoginRegisterResponseSchema,
    responses=generate_examples(
        InvalidCredentialsException,
        RateLimitException,
    ),
)
@inject
async def login(
    user_login: UserLoginSchema,
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
    dependencies=Depends(  # noqa
        RateLimiter(
            times=settings.LIMIT_LOGIN_TIMES,
            seconds=settings.LIMIT_LOGIN_SECONDS,
        ),
    ),
) -> UserLoginRegisterResponseSchema:
    """
    Login with email and password.

    Returns user payload and JWT tokens (access, refresh).
    """
    user_data, tokens = await auth_service.login(user_login)

    return UserLoginRegisterResponseSchema(**user_data, tokens=tokens)


@auth_router.post(
    "/refresh/",
    name="auth:refresh",
    summary="Refresh tokens",
    status_code=status.HTTP_200_OK,
    response_model=AccessRefreshTokensSchema,
    responses=generate_examples(
        InvalidCredentialsException,
    ),
)
@inject
async def refresh_access_token(
    background_tasks: BackgroundTasks,
    refresh_token: RefreshTokenSchema,
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
) -> AccessRefreshTokensSchema:
    """
    Refresh access_token from refresh_token.
    """
    tokens: AccessRefreshTokensSchema = await auth_service.refresh_tokens(
        refresh=refresh_token.refresh,
        background_tasks=background_tasks,
    )
    return tokens


@auth_router.post(
    "/request-new-password/{email}/",
    name="auth:request-password",
    summary="Send new password on user email. Rate limited.",
    description="Send new password on user email. Does not require authentication. "
    "Does not inform if email exists (always returns 200). Rate limited.",
    status_code=status.HTTP_200_OK,
    response_model=None,
    responses=generate_examples(RateLimitException),
)
@inject
async def request_new_password(
    email: EmailStr,
    background_tasks: BackgroundTasks,
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
    dependencies=Depends(  # noqa
        RateLimiter(
            times=settings.LIMIT_REQUEST_NEW_PASSWORD_TIMES,
            seconds=settings.LIMIT_REQUEST_NEW_PASSWORD_SECONDS,
        ),
    ),
) -> None:
    """
    Send new password on user email. Should be confirmed by user.
    """
    await auth_service.request_new_password(email, background_tasks)


@auth_router.post(
    "/confirm-new-password/{token}/",
    name="auth:confirm-password",
    summary="Confirm new password received by email and log in.",
    status_code=status.HTTP_200_OK,
    response_model=UserLoginRegisterResponseSchema,
    responses=generate_examples(NewPasswordInvalidTokenException),
)
@inject
async def confirm_new_password(
    token: str,
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
) -> UserLoginRegisterResponseSchema:
    """
    Confirm new account password with token.
    """
    tokens, user_data = await auth_service.confirm_new_password(token)
    return UserLoginRegisterResponseSchema(**user_data, tokens=tokens)


@auth_router.get(
    "/captcha/",
    name="captcha:get",
    status_code=status.HTTP_201_CREATED,
    summary="Create registration captcha. Rate limited.",
    description="Create registration captcha. Returns key for captcha challenge and image in base64 format."
    " Call backend developer to change captcha image size. Rate limited.",
    response_model=CaptchaChallengeSchema,
    responses=generate_examples(RateLimitException),
)
@inject
async def get_captcha(
    captcha_service: CaptchaService = Depends(Provide[Registry.authentication.captcha_service]),
    dependencies=Depends(  # noqa
        RateLimiter(
            times=settings.LIMIT_CAPTCHA_TIMES,
            seconds=settings.LIMIT_CAPTCHA_SECONDS,
        ),
    ),
):
    """
    Create registration captcha.
    """
    captcha_challenge, image_base64 = await captcha_service.create_challenge()
    return CaptchaChallengeSchema(
        challenge=captcha_challenge.challenge,
        image_base64=image_base64,
    )


@auth_router.post(
    "/change-password/",
    name="auth:change_password",
    summary="Change password. Authentication required.",
    status_code=status.HTTP_200_OK,
    responses=generate_examples(
        success_responses=[
            SuccessResponse(message="Password changed successfully."),
        ]
    ),
)
@inject
async def change_password(
    change_password_schema: ChangePasswordSchema,
    user_payload: UserPayload = Depends(get_authenticated_user_payload),
    auth_service: AuthService = Depends(Provide[Registry.authentication.auth_service]),
):
    """
    Confirm new account password with token.
    """
    await auth_service.change_password(change_password_schema=change_password_schema, user_payload=user_payload)
    return SuccessResponse(message="Password changed successfully.")

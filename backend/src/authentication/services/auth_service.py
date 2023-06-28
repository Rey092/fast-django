# -*- coding: utf-8 -*-
"""Auth service module."""
import asyncio
import functools
from typing import Optional, Tuple

from email_validator import validate_email
from fastapi.encoders import jsonable_encoder
from starlette.background import BackgroundTasks

from src.authentication.api_errors import (
    ChangePasswordInvalidOldPasswordException, InvalidCaptchaException,
    NewPasswordInvalidTokenException, RegisterInvalidEmailException,
    RegisterUserAlreadyExistsException)
from src.authentication.models import PasswordToken
from src.authentication.schemas.auth import UserLoginSchema, UserPayload
from src.authentication.schemas.captchas import CaptchaVerifySchema
from src.authentication.schemas.change_password import ChangePasswordSchema
from src.authentication.schemas.registration import UserRegisterSchema
from src.authentication.schemas.tokens import AccessRefreshTokensSchema
from src.authentication.services.captcha_service import CaptchaService
from src.authentication.services.jwt_service import JWTService
from src.authentication.services.password_service import PasswordService
from src.users.models import User
from src.users.services import UserService
from utils.responses.http.auth import InvalidCredentialsException
from utils.services import BaseService


class AuthService(BaseService):
    """Auth service."""

    def __init__(
        self,
        user_service: UserService,
        captcha_service: CaptchaService,
        jwt_service: JWTService,
        password_service: PasswordService,
    ):
        """Initiate auth service."""
        self.user_service: UserService = user_service
        self.captcha_service: CaptchaService = captcha_service
        self.jwt_service: JWTService = jwt_service
        self.password_service: PasswordService = password_service

    async def register_user(self, user_register_schema: UserRegisterSchema):
        """Register user."""
        # validate email
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                functools.partial(validate_email, user_register_schema.email, timeout=2),
            )
        except Exception as e:
            raise RegisterInvalidEmailException(str(e))

        # check if user exists
        if await self.check_email_exists(user_register_schema.email):
            raise RegisterUserAlreadyExistsException()

        # verify captcha
        captcha: CaptchaVerifySchema = user_register_schema.captcha
        captcha_is_valid, captcha_challenge = await self.captcha_service.verify_captcha(captcha)

        # check captcha
        if not captcha_is_valid:
            raise InvalidCaptchaException()

        # create user
        user: User = await self.user_service.create_user(
            email=user_register_schema.email,
            password=user_register_schema.password,
            nickname=user_register_schema.nickname,
        )

        # delete captcha if exists
        if captcha_challenge:
            await self.captcha_service.delete_one(id=captcha_challenge.id)

        # create tokens
        payload, user_data, tokens = self.get_payload_and_tokens(user)

        return user_data, tokens

    async def login(self, user_login: UserLoginSchema):
        """Login user."""
        # get user
        user: User = await self.user_service.get_one_by_email(user_login.email)

        # check if user exists
        if user is None:
            raise InvalidCredentialsException()

        # check password
        if not user.check_password(user_login.password):
            raise InvalidCredentialsException()

        # create tokens
        payload, user_data, tokens = self.get_payload_and_tokens(user)

        return user_data, tokens

    async def refresh_tokens(self, refresh: str, background_tasks: BackgroundTasks) -> AccessRefreshTokensSchema:
        """Refresh tokens."""
        # decode refresh token
        refresh_token_payload: Optional[dict] = await self.jwt_service.decode_token(refresh)

        # check if refresh token is valid
        if not refresh_token_payload or refresh_token_payload.get("type") != "refresh":
            raise InvalidCredentialsException()

        # get user
        user = await self.user_service.get_one_by_id(refresh_token_payload["id"])

        # check if user exists and is active
        if user is None or not user.is_active:
            raise InvalidCredentialsException()

        # create tokens
        payload, user_data, tokens = self.get_payload_and_tokens(user)

        # update last login
        background_tasks.add_task(self.update_last_login, user=user)

        return tokens

    async def update_last_login(self, user: User):
        """Update last login."""
        await self.user_service.update_last_login(user=user)

    async def request_new_password(self, email: str, background_tasks: BackgroundTasks):
        """Request new password."""
        background_tasks.add_task(
            self._handle_new_password_request,
            background_tasks=background_tasks,
            email=email,
        )

    async def confirm_new_password(self, token: str) -> Tuple[AccessRefreshTokensSchema, dict]:
        """Confirm new password."""
        # get password token
        token_hash = self.password_service.hash_token(token)
        password_token: Optional[PasswordToken] = await self.password_service.get_one_by_token_hash(token_hash)

        # check if token exists
        if not password_token:
            raise NewPasswordInvalidTokenException()

        # get user
        user: User = await self.user_service.get_one_by_email(password_token.email)
        # set new password
        await self.user_service.update_user_password(user=user, new_password=password_token.new_password)
        # delete password token
        await self.password_service.delete_one(id=password_token.id)

        # delete password token
        payload, user_data, tokens = self.get_payload_and_tokens(user)

        return tokens, user_data

    def get_payload_and_tokens(self, user: User) -> Tuple[UserPayload, dict, AccessRefreshTokensSchema]:
        """Get payload and tokens."""
        payload: UserPayload = UserPayload.from_orm(user)
        user_data: dict = jsonable_encoder(payload)
        tokens: AccessRefreshTokensSchema = self.jwt_service.create_tokens(user_data)
        return payload, user_data, tokens

    async def check_email_exists(self, email: str) -> bool:
        """Check if email exists."""
        return await self.user_service.check_email_exists(email)

    async def _handle_new_password_request(self, background_tasks: BackgroundTasks, email: str):
        new_password, token = await self.password_service.generate_password_token(
            email=email,
        )
        # TODO: add email service with default email templates
        # email_client = create_email_client()
        # if settings.SMTP_ENABLED:
        #     background_tasks.add_task(
        #         email_client.send_new_password_email,
        #         EmailSchema(email=[email]),
        #         new_password=new_password,
        #         token=token,
        #     )

    async def change_password(self, change_password_schema: ChangePasswordSchema, user_payload: UserPayload) -> None:
        """Change password."""
        # get user
        user: User = await self.user_service.get_one_by_id(user_payload.id)

        # check if old password is correct
        if not user.check_password(change_password_schema.old_password):
            raise ChangePasswordInvalidOldPasswordException()

        # set new password
        await self.user_service.update_user_password(user=user, new_password=change_password_schema.password)

        return None

    async def refresh_payload(self, user_id: int) -> UserPayload:
        """Get new payload."""
        # get user
        user: User = await self.user_service.get_one(id=user_id)

        # create tokens
        payload, user_data, tokens = self.get_payload_and_tokens(user)

        return payload

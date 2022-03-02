from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.utils import timezone

from mad.app.exceptions import (
    MadBadRequest,
    INVALID_TOKEN,
    MadUnauthorized,
    MadNotFound,
    USER_IS_NOT_ACTIVE,
    INCORRECT_LOGIN_OR_PASSWORD,
    MadPermissionDenied,
    USER_IS_NOT_DOCTOR,
)
from mad.app.repositories import UserRepository


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.MAD_JWT_ALGORITHM)
    except jwt.DecodeError:
        raise MadBadRequest(INVALID_TOKEN)

    return payload


def generate_access_token(user_id: int or str) -> str:
    token = jwt.encode(
        {"user_id": user_id, "created_at": timezone.now().isoformat(), "is_doctor": True},
        settings.SECRET_KEY,
        settings.MAD_JWT_ALGORITHM,
    )

    return token


class LoginViaUsernameAndPasswordService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, username: str, password: str) -> str:
        """
        Authenticate user via login and password.

        :param username:
        :param password:
        :return: auth_token
        """
        incorrect_cred_error = "Incorrect login or password."
        try:
            user = self._user_repository.get_by_username(username=username)
        except MadNotFound:
            raise MadBadRequest(code=INCORRECT_LOGIN_OR_PASSWORD, message=incorrect_cred_error)

        if not check_password(password, user.password):
            raise MadBadRequest(code=INCORRECT_LOGIN_OR_PASSWORD, message=incorrect_cred_error)

        if not user.is_active:
            raise MadPermissionDenied(code=USER_IS_NOT_ACTIVE, message="User is not active")

        return generate_access_token(user.id)

    @classmethod
    def factory(cls) -> "LoginViaUsernameAndPasswordService":
        return cls(UserRepository.factory())


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, auth_token: str) -> "User":
        """
        Parse auth token and return authenticated user

        :param auth_token
        :return: authenticated_user
        """
        token_payload = decode_token(auth_token)
        created_at = datetime.fromisoformat(token_payload["created_at"])

        if not token_payload.get("is_doctor"):
            raise MadPermissionDenied(USER_IS_NOT_DOCTOR)

        if created_at + timedelta(minutes=settings.MAD_ACCESS_TOKEN_EXPIRE_MINUTES) <= timezone.now():
            raise MadUnauthorized(message="Access token expired")

        user_id = token_payload["user_id"]
        try:
            user = self._user_repository.get_by_id(user_id)
        except MadNotFound:
            raise MadUnauthorized()

        if not user.is_active:
            raise MadPermissionDenied(USER_IS_NOT_ACTIVE)

        return user

    @classmethod
    def factory(cls) -> "AuthService":
        return cls(UserRepository.factory())

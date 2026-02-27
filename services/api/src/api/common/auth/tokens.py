from datetime import datetime, timedelta, timezone

import jwt
from api.models.RefreshToken import RefreshToken
from api.models.Token import Token
from pydantic import BaseModel

from .jwks import get_private_key, get_public_key


def get_default_max_age():
    return timedelta(minutes=15)


def get_expires(delta: timedelta | None = None):
    if not delta:
        delta = get_default_max_age()
    expire = datetime.now(timezone.utc) + delta

    return expire


def create_jwt(
    data: BaseModel,
    expires: datetime | None = None,
):
    to_encode = data.model_dump()
    to_encode["exp"] = int((expires or get_expires()).timestamp())

    encoded_jwt = jwt.encode(
        to_encode, get_private_key(), get_public_key().algorithm_name
    )

    return encoded_jwt


def create_access_token(
    user_id: str,
    login: str,
):
    expires = get_expires(timedelta(minutes=15))
    return create_jwt(Token(user_id=user_id, login=login), expires), expires


def create_refresh_token(
    user_id: str,
):
    expires = get_expires(timedelta(days=1))
    return create_jwt(RefreshToken(user_id=user_id), expires), expires

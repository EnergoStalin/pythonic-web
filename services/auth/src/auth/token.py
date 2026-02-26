from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pydantic import BaseModel

from .jwks import get_private_key, get_public_key


def get_default_max_age():
    return timedelta(minutes=15)


def get_expires(delta: timedelta | None = None):
    if not delta:
        delta = get_default_max_age()
    expire = datetime.now(timezone.utc) + delta

    return expire


def create_access_token(
    data: BaseModel,
    expires: datetime | None = None,
):
    to_encode = data.model_dump()
    to_encode["exp"] = int((expires or get_expires()).timestamp())

    encoded_jwt = jwt.encode(
        to_encode, get_private_key(), get_public_key().algorithm_name
    )

    return encoded_jwt

from http import HTTPStatus
from typing import Annotated
from uuid import UUID

import jwt
from api.common.auth.jwks import get_public_key
from api.common.models.UserToken import UserToken
from api.db.connection import DB
from api.db.models.User import User
from api.db.operations.user import user_get_by_id
from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyCookie


def decode_access_token(token: str):
    try:
        public = get_public_key()
        payload = jwt.decode(token, public, public.algorithm_name)
        return UserToken.model_validate(payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(HTTPStatus.UNAUTHORIZED, "Invalid token")


async def verify_user(
    token: Annotated[str, Depends(APIKeyCookie(name="token"))], db: DB
):
    user = decode_access_token(token)
    if u := await user_get_by_id(db, UUID(user.user_id)):
        return u
    raise HTTPException(HTTPStatus.UNAUTHORIZED, "User does not exist in db")


VerifiedUser = Annotated[User, Depends(verify_user)]

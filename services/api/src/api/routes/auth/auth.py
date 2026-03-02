from http import HTTPStatus
from typing import Annotated
from uuid import UUID

import jwt
from api.common.auth.jwks import get_public_key
from api.common.auth.security import decode_token
from api.common.models.Validator import Validator
from api.db.connection import DB
from api.db.operations.refresh_token import (
    refresh_token_update_or_create,
    refresh_token_validate,
)
from api.db.operations.user import user_get_by_id, user_get_or_create
from fastapi.params import Form
from fastapi.responses import Response
from fastapi.routing import APIRouter

from .models.AuthConfig import AuthConfig, Validation
from .models.RefreshToken import RefreshToken as RefreshTokenJson
from .models.TokenResponse import TokenResponse
from .tokens import create_access_token, create_refresh_token

router = APIRouter()

UNAUTHORIZED = Response(status_code=HTTPStatus.UNAUTHORIZED)


@router.post("")
async def auth(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: DB,
    response: Response,
):
    user = await user_get_or_create(db, login, password)

    if not user:
        return UNAUTHORIZED

    refresh_token, refresh_token_expires = create_refresh_token(user.id.hex)
    _ = await refresh_token_update_or_create(
        db, refresh_token, user.id, refresh_token_expires
    )

    token, token_expires = create_access_token(user.id.hex, login)

    response.set_cookie("token", token, expires=token_expires)
    return TokenResponse(
        token=token,
        refresh_token=refresh_token,
        expires_at=token_expires,
    )


@router.post("/refresh")
async def refresh(token: Annotated[str, Form()], db: DB):
    refresh_token = RefreshTokenJson.model_validate(decode_token(token))

    if await refresh_token_validate(db, token) is None:
        return UNAUTHORIZED

    user_id = refresh_token.user_id

    user = await user_get_by_id(db, UUID(hex=user_id))
    if not user:
        return Response(status_code=HTTPStatus.NOT_FOUND)

    new_token, new_token_expires = create_access_token(user_id, user.login)
    return TokenResponse(
        token=new_token, refresh_token=token, expires_at=new_token_expires
    )


@router.post("/validate")
async def authme(token: Annotated[str, Form()]):
    return decode_token(token)


@router.get("/config", response_model=AuthConfig)
async def config():
    return AuthConfig(
        validation=Validation(
            login=Validator(regex=r"^[^\s]{0,49}$", description="max 50 symbols"),
            password=Validator(regex=r"^[^\s]{0,49}$", description="max 50 symbols"),
        )
    )

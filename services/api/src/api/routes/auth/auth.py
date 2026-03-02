from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from api.common.auth.security import decode_token
from api.common.models.Validator import Validator
from api.db.connection import DB
from api.db.operations.refresh_token import (
    refresh_token_update_or_create,
    refresh_token_validate,
)
from api.db.operations.user import user_get_by_id, user_get_or_create
from api.routes.auth.models.AuthConfig import AuthConfig, Validation
from fastapi.params import Form
from fastapi.responses import Response
from fastapi.routing import APIRouter

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
    """
    Принимает логин/пароль в x-form-urlencoded создавая пользователя(при необходимости) возвращая access_token refresh_token и expires_at для access_tokenа.
    refresh_token всегда хранится один в базе до следующего обращения к эндпоинту где он проверяется на истечение срока и удаляется если уже истёк.
    """
    user = await user_get_or_create(db, login, password)

    if not user:  # Юзер был да пароль не тот
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


@router.post("/refresh", response_model=TokenResponse)
async def refresh(token: Annotated[str, Form()], db: DB):
    """ Выписывает новый access_token """
    refresh_token = RefreshTokenJson.model_validate(decode_token(token))

    if await refresh_token_validate(db, token) is None:
        return UNAUTHORIZED

    user_id = refresh_token.user_id

    user = await user_get_by_id(db, UUID(hex=user_id))
    assert user  # Никогда не NONE после успешного refresh_token_validate гарантировано ondelete="CASCADE"

    new_token, new_token_expires = create_access_token(user_id, user.login)

    return TokenResponse(
        token=new_token, refresh_token=token, expires_at=new_token_expires
    )


@router.get("/config", response_model=AuthConfig)
async def config():
    return AuthConfig(
        validation=Validation(
            login=Validator(regex=r"^[^\s]{0,49}$", description="max 50 symbols"),
            password=Validator(regex=r"^[^\s]{0,49}$", description="max 50 symbols"),
        )
    )

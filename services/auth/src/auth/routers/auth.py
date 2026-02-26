from datetime import timedelta
from typing import Annotated

from fastapi.responses import Response
import jwt
from sqlmodel import select
from auth.db.connection import DB
from auth.db.models.User import User
from auth.jwks import get_public_key
from auth.models.RefreshToken import RefreshToken as RefreshTokenJson
from auth.models.Token import Token
from auth.models.TokenResponse import TokenResponse
from auth.token import create_access_token, get_expires
from fastapi.params import Form
from fastapi.routing import APIRouter

router = APIRouter(prefix="/auth")

async def user_get_or_create(db: DB, login: str, password: str):
    statement = select(User).where(User.login == login)
    cursor = await db.exec(statement)
    if (u := cursor.first()):
        if u.password != password:
            return None, False
        return u, True
    else:
        u = User(login=login, password=password)
        db.add(u)
        await db.commit()
        await db.refresh(u)
        return u, True

@router.post("/")
async def auth(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    db: DB
):
    user, success = await user_get_or_create(db, login, password)
    if not success:
        return Response(status_code=400)

    expires = get_expires()

    refresh_token = create_access_token(
        RefreshTokenJson(login=login), get_expires(timedelta(days=1))
    )
    # _ = await RefreshToken.update_or_create(
    #     login=login,
    #     token=refresh_token,
    #     defaults={"token": refresh_token, "user": user},
    # )

    return TokenResponse(
        token=create_access_token(Token(login=login)),
        refresh_token=refresh_token,
        expires_at=expires,
    )


@router.post("/refresh")
async def refresh(
    token: Annotated[str, Form()],
):
    # if not await RefreshToken.exists(token=token):
    #     return Response(status_code=401)

    refresh_token = RefreshTokenJson.model_validate(
        jwt.decode(token, get_public_key(), verify=True)
    )
    login = refresh_token.login

    expires = get_expires()

    refresh_token = create_access_token(
        RefreshTokenJson(login=login), get_expires(timedelta(days=1))
    )

    return TokenResponse(
        token=create_access_token(Token(login=login)),
        refresh_token=refresh_token,
        expires_at=expires,
    )


@router.post("/validate")
async def authme(token: Annotated[str, Form()]):
    return jwt.decode(token, get_public_key(), verify=True)

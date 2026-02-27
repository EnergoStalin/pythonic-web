from datetime import datetime, timezone
from uuid import UUID

from api.db.connection import DBST
from api.db.models.RefreshToken import RefreshToken
from sqlmodel import select

from api.db.operations.add_one import add_one

async def refresh_token_validate(db: DBST, token: str):
    statement = select(RefreshToken).where(RefreshToken.token == token)
    cursor = await db.exec(statement)
    if t := cursor.one_or_none():
        if t.expire_at < datetime.now(tz=timezone.utc):
            await db.delete(t)
            await db.flush()
            return None
        return t
    return None


async def refresh_token_update_or_create(
    db: DBST, token: str, user_id: UUID, expire_at: datetime
):
    default = RefreshToken(user_id=user_id, token=token, expire_at=expire_at)
    statement = select(RefreshToken).where(RefreshToken.user_id == user_id)
    cursor = await db.exec(statement)
    if t := cursor.one_or_none():
        if t.token != token:
            return None
        db.add(t.sqlmodel_update(default))
        await db.commit()
    else:
        return await add_one(db, default)

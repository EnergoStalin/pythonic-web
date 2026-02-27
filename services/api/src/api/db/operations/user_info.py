from uuid import UUID

from sqlmodel import select

from api.db.connection import DBST
from api.db.models.UserInfo import UserInfo


async def user_info_get_by_user_id(db: DBST, user_id: UUID):
    statement = select(UserInfo).where(UserInfo.user_id == user_id)
    cursor = await db.exec(statement)
    if i := cursor.one_or_none():
        return i

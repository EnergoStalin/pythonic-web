from uuid import UUID
from api.db.connection import DBST
from api.db.models.User import User
from sqlmodel import select

from api.db.operations.add_one import add_one


async def user_get_or_create(db: DBST, login: str, password: str):
    statement = select(User).where(User.login == login)
    cursor = await db.exec(statement)
    if u := cursor.one_or_none():
        if u.password != password:
            return None
        return u
    else:
        return await add_one(db, User(login=login, password=password))

async def user_get_by_id(db: DBST, id: UUID):
    statement = select(User).where(User.id == id)
    cursor = await db.exec(statement)
    return cursor.one_or_none()

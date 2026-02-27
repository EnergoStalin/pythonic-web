from typing import TypeVar

from api.db.connection import DBST

T = TypeVar("T")


async def add_one(db: DBST, data: T):
    db.add(data)
    await db.commit()
    await db.refresh(data)

    return data

from typing import Annotated

from api.common.auth.security import VerifiedUser
from api.db.connection import DB
from api.db.models.UserInfo import UserInfo as UserInfoDB
from api.db.operations.user_info import user_info_get_by_user_id
from fastapi.params import Body
from fastapi.routing import APIRouter

from .models.UserInfo import UserInfo

router = APIRouter()


@router.get("/me", response_model=UserInfo)
async def getme(verified_user: VerifiedUser, db: DB):
    user = UserInfo(
        user_id=verified_user.id.hex,
        login=verified_user.login,
        password=verified_user.password,
    )
    if info := await user_info_get_by_user_id(db, verified_user.id):
        return user.model_copy(update=info.model_dump(exclude={"user_id"}))
    return user


@router.put("/me")
async def putme(
    verified_user: VerifiedUser, patch: Annotated[UserInfo, Body()], db: DB
):
    pdict = patch.model_dump(exclude={"user_id"})

    for k in pdict.keys():
        if not pdict[k]:
            pdict[k] = ""

    db_user = verified_user.sqlmodel_update(pdict)
    db.add(db_user)

    update = {"user_id": verified_user.id}
    if db_user_info := await user_info_get_by_user_id(db, verified_user.id):
        db_user_info = db_user_info.sqlmodel_update(pdict, update=update)
    else:
        db_user_info = UserInfoDB.model_validate(pdict, update=update)

    db.add(db_user_info)

    await db.commit()

    return "OK"

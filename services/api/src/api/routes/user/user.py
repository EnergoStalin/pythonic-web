from api.common.auth.security import VerifiedUser
from api.db.connection import DB
from api.db.operations.user_info import user_info_get_by_user_id
from fastapi.routing import APIRouter

from .models.UserInfo import UserInfo

router = APIRouter()


@router.get("/me")
async def getme(verified_user: VerifiedUser, db: DB):
    kwargs = {}
    if info := await user_info_get_by_user_id(db, verified_user.id):
        kwargs = info.model_dump()
        # Ненавижу
        kwargs.pop("user_id")

    return UserInfo(
        user_id=verified_user.id.hex,
        login=verified_user.login,
        password=verified_user.password,
        **kwargs,  # pyright: ignore[reportAny]
    )

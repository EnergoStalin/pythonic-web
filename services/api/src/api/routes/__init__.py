from fastapi.routing import APIRouter

from .auth.auth import router as auth
from .root import router as root
from .storage.storage import router as storage
from .user.user import router as user

router = APIRouter()

router.include_router(root)
router.include_router(prefix="/auth", router=auth, tags=["auth"])
router.include_router(prefix="/storage", router=storage, tags=["storage"])
router.include_router(prefix="/user", router=user, tags=["user"])

__all__ = ["router"]

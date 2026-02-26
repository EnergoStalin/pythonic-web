from fastapi.routing import APIRouter

from .auth import router as auth
from .root import router as root

router = APIRouter()

router.include_router(auth)
router.include_router(root)

from api.common.auth.jwks import get_jwks
from api.models.JWKS import JWKS
from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health():
    return "OK"


@router.get("/.well-known/jwks.json", response_model=JWKS, tags=["jwks"])
async def jwks():
    return get_jwks()

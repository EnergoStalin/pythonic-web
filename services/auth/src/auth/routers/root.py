from auth.jwks import get_jwks
from auth.models.JWKS import JWKS
from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return "OK"


@router.get("/.well-known/jwks.json", response_model=JWKS)
async def jwks():
    return get_jwks()

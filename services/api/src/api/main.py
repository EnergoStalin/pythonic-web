from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import IS_DEV, WWW_URL
from .db.connection import close, init
from .middlewares.JSONError import JSONErrorMiddleware
from .routes import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init(IS_DEV)
    yield
    await close()


kwargs = {} if IS_DEV else {"docs_url": None, "redoc_url": None, "openapi_url": None}

app = FastAPI(lifespan=lifespan, *kwargs)
app.include_router(router)

app.add_middleware(JSONErrorMiddleware, is_dev=IS_DEV)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[WWW_URL],
    allow_methods=["GET", "POST", "PUT"],
)

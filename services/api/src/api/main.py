from contextlib import asynccontextmanager

from api.config import IS_DEV, WWW_URL
from api.db.connection import close, init
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init(IS_DEV)
    yield
    await close()


kwargs = {} if IS_DEV else {"docs_url": None, "redoc_url": None, "openapi_url": None}

app = FastAPI(lifespan=lifespan, *kwargs)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[WWW_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

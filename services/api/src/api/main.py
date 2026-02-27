from contextlib import asynccontextmanager

from api.config import WWW_URL
from api.db.connection import close, init
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init()
    yield
    await close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[WWW_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from contextlib import asynccontextmanager

from auth.db.connection import close, init
from fastapi import FastAPI

from .routers import router

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init()
    yield
    await close()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

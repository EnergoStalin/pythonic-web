import asyncio
import mimetypes
from http import HTTPStatus
from pathlib import Path as FSPath
from typing import Annotated

from api.config import BASE_URL
from fastapi import UploadFile
from fastapi.params import File, Path, Query
from fastapi.requests import Request
from fastapi.responses import FileResponse, Response
from fastapi.routing import APIRouter

from .config import SPOOL_PATH
from .fs import create_file_url, ensure_free_space, get_directory_slice, save_file_chunked
from .models.FileInfo import FileInfo
from .models.StorageConfig import StorageConfig

router = APIRouter()

ACCEPTED_EXTENSIONS = [".png", ".mp4"]


def guess_mime(fn: str):
    tp, _ = mimetypes.guess_type(fn)
    return tp or "application/octet-stream"


@router.get("/files")
async def list_files(
    request: Request,
    page: Annotated[int, Query()] = 1,
    limit: Annotated[int, Query()] = 20,
):
    return [
        FileInfo(
            name=d.name,
            mime=guess_mime(d.name),
            url=create_file_url(BASE_URL, FSPath(request.url.path), d.name),
        )
        for d in get_directory_slice(SPOOL_PATH, page, limit)
    ]


@router.get("/files/{name}")
async def get_file(name: Annotated[str, Path()]):
    path = SPOOL_PATH.joinpath(name)
    mime = guess_mime(path.as_posix())
    return FileResponse(path, media_type=mime)


# Было бы время написал бы свою реализацию но осталось около 10 часов а я уже почти никакой хоть и встал в 7 утра так что так
@router.post("/files")
async def upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files")],
):
    total = 0

    for uf in files:
        if not uf.filename:
            return Response(f"unknown filename is not allowed", HTTPStatus.FORBIDDEN)

        if not uf.size:
            return Response(f"unknown filesize is not allowed", HTTPStatus.FORBIDDEN)

        if (suffix := FSPath(uf.filename).suffix) not in ACCEPTED_EXTENSIONS:
            return Response(f"suffix {suffix} is not allowed", HTTPStatus.FORBIDDEN)

        total += uf.size

    ensure_free_space(SPOOL_PATH, total)
    _ = await asyncio.gather(*[save_file_chunked(uf) for uf in files])

    return Response("OK")


@router.get("/config")
async def config():
    return StorageConfig(accept=ACCEPTED_EXTENSIONS)

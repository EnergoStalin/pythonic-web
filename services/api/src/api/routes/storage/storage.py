import asyncio
import mimetypes
from http import HTTPStatus
from itertools import islice
from os import scandir
from pathlib import Path as FSPath
from typing import Annotated
from urllib.parse import quote, urljoin

from api.config import BASE_URL
from api.models.FileInfo import FileInfo
from api.models.StorageConfig import StorageConfig
from api.routes.storage.config import SPOOL_PATH
from api.routes.storage.fs import save_file_chunked
from fastapi import UploadFile
from fastapi.params import File, Path, Query
from fastapi.requests import Request
from fastapi.responses import FileResponse, Response
from fastapi.routing import APIRouter

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
    prefix = FSPath(request.url.path)

    start = (page - 1) * limit
    end = start + limit
    slice = islice(filter(lambda fp: fp.is_file(), scandir(SPOOL_PATH)), start, end)

    return [
        FileInfo(
            name=d.name,
            mime=guess_mime(d.name),
            url=urljoin(BASE_URL, prefix.joinpath(quote(d.name)).as_posix()),
        )
        for d in slice
    ]


@router.get("/files/{name}")
async def get_file(name: Annotated[str, Path()]):
    path = SPOOL_PATH.joinpath(name)
    return FileResponse(path, media_type=guess_mime(path.as_posix()))


# Было бы время написал бы свою реализацию но осталось около 10 часов а я уже почти никакой хоть и встал в 7 утра так что так
@router.post("/files")
async def upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files")],
):
    for uf in filter(lambda uf: uf.filename, files):
        if (
            suffix := FSPath(uf.filename).suffix  # pyright: ignore[reportArgumentType]
        ) not in ACCEPTED_EXTENSIONS:
            return Response(f"suffix {suffix} not allowed", HTTPStatus.FORBIDDEN)

    _ = await asyncio.gather(*[save_file_chunked(uf) for uf in files])
    return ""


@router.get("/config")
async def config():
    return StorageConfig(accept=ACCEPTED_EXTENSIONS)

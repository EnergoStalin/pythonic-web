import asyncio
import mimetypes
from os import listdir
from pathlib import Path as FSPath
from typing import Annotated
from urllib.parse import quote, urljoin

from api.config import BASE_URL
from api.models.FileInfo import FileInfo
from api.routes.storage.config import SPOOL_PATH
from api.routes.storage.fs import save_file_chunked
from fastapi import UploadFile
from fastapi.params import File, Path
from fastapi.requests import Request
from fastapi.responses import FileResponse
from fastapi.routing import APIRouter

router = APIRouter()


def guess_mime(fn: str):
    tp, _ = mimetypes.guess_type(fn)
    return tp or "application/octet-stream"


@router.get("")
async def list_files(request: Request):
    prefix = FSPath(request.url.path)
    print(BASE_URL, prefix)

    return [
        FileInfo(
            name=fn,
            mime=guess_mime(fn),
            url=urljoin(BASE_URL, prefix.joinpath(quote(fn)).as_posix()),
        )
        for fn in listdir(SPOOL_PATH)
    ]


@router.get("/{name}")
async def get_file(name: Annotated[str, Path()]):
    path = SPOOL_PATH.joinpath(name)
    return FileResponse(path, media_type=guess_mime(path.as_posix()))


# Было бы время написал бы свою реализацию но осталось около 10 часов а я уже почти никакой хоть и встал в 7 утра так что так
@router.post("")
async def upload_files(
    files: Annotated[list[UploadFile], File(description="Multiple files")],
):
    _ = await asyncio.gather(*[save_file_chunked(uf) for uf in files])

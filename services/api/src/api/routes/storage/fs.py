import shutil
from itertools import islice
from os import scandir
from pathlib import Path
from urllib.parse import quote, urljoin

import aiofiles
from fastapi import UploadFile

from .config import SPOOL_PATH


async def save_file_chunked(uf: UploadFile, chunk_size: int = 1024 * 1024):
    fp = SPOOL_PATH.joinpath(uf.filename)  # pyright: ignore[reportArgumentType]

    try:
        async with aiofiles.open(fp, "wb") as f:
            while chunk := await uf.read(chunk_size):
                _ = await f.write(chunk)
    except Exception as e:
        if fp.exists():
            fp.unlink()
        raise e
    finally:
        await uf.close()

    return fp


def get_directory_slice(root: Path, page: int, limit: int):
    start = (page - 1) * limit
    end = start + limit
    return islice(filter(lambda fp: fp.is_file(), scandir(root)), start, end)


def create_file_url(base_url: str, prefix: Path, name: str):
    return urljoin(base_url, prefix.joinpath(quote(name)).as_posix())

def ensure_free_space(path: Path, size: int):
    usage = shutil.disk_usage(path)
    if usage.free > size:
        return

    file_mtimes = [(e.name, e.stat().st_mtime) for e in scandir(path) if e.is_file()]
    needed = size - usage.free
    for f, s in sorted(file_mtimes, key=lambda x: x[1]):
        if needed <= 0: return
        path.joinpath(f).unlink()
        needed -= s

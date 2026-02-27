from api.routes.storage.config import SPOOL_PATH
from fastapi import UploadFile

import aiofiles


async def save_file_chunked(
    uf: UploadFile, chunk_size: int = 1024 * 1024  # 1MB chunks
):
    if not uf.filename:
        raise ValueError("Filename is None")

    fp = SPOOL_PATH.joinpath(uf.filename)

    try:
        # Using aiofiles for async file writing
        async with aiofiles.open(fp, "wb") as f:
            while chunk := await uf.read(chunk_size):
                _ = await f.write(chunk)
    except Exception as e:
        # Clean up if something goes wrong
        if fp.exists():
            fp.unlink()
        raise e
    finally:
        await uf.close()

    return fp

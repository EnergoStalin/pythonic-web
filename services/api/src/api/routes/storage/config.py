from os import makedirs
from pathlib import Path

from api.common.utils.env import genv

SPOOL_PATH = Path(genv("STORAGE_POOL_PATH", "/data/storage/pool"))
makedirs(SPOOL_PATH, exist_ok=True)

from os import getenv
from typing import TypeVar

T = TypeVar("T")


def genv(key: str, default: T = None):  # pyright: ignore[reportInvalidTypeVarUse]
    if e := getenv(key):
        return e
    return default


from pydantic import BaseModel


class FileInfo(BaseModel):
    name: str
    mime: str
    url: str

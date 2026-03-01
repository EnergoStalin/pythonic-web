from pydantic import BaseModel


class StorageConfig(BaseModel):
    accept: list[str]

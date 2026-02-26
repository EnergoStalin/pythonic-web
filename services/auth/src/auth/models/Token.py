from pydantic import BaseModel


class Token(BaseModel):
    login: str
    exp: int = 0

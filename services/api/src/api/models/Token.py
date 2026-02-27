from pydantic import BaseModel


class Token(BaseModel):
    user_id: str
    login: str
    exp: int = 0

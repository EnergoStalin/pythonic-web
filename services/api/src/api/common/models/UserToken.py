from pydantic import BaseModel


class UserToken(BaseModel):
    user_id: str
    login: str
    exp: int = 0

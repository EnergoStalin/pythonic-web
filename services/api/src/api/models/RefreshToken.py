from pydantic import BaseModel


class RefreshToken(BaseModel):
    user_id: str

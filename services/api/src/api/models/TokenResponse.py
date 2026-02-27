from datetime import datetime

from pydantic import BaseModel


class TokenResponse(BaseModel):
    token: str
    refresh_token: str
    expires_at: datetime

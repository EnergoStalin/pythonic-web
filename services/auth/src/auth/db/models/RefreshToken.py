from datetime import datetime
from uuid import UUID
from sqlmodel import Field, SQLModel



class RefreshToken(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    id: int = Field(primary_key=True, nullable=False)
    token: str = Field(nullable=False)
    expire_at: datetime = Field(nullable=False)

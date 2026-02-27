from datetime import datetime
from uuid import UUID

from sqlalchemy.types import DateTime
from sqlmodel import Field, SQLModel


class RefreshToken(SQLModel, table=True):
    user_id: UUID = Field(
        primary_key=True,
        foreign_key="user.id",
        nullable=False,
        ondelete="CASCADE",
        unique=True
    )
    token: str = Field(max_length=1024, nullable=False)
    expire_at: datetime = Field(
        nullable=False,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
    )

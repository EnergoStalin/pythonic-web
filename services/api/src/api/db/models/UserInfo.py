from uuid import UUID

from sqlmodel import Field, SQLModel


class UserInfo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    user_id: UUID = Field(
        foreign_key="user.id",
        nullable=False,
        unique=True,
        ondelete="CASCADE",
        index=True,
    )
    last_name: str = Field(max_length=50, nullable=False)
    first_name: str = Field(max_length=50, nullable=False)
    surname: str = Field(max_length=50, nullable=False)
    company_name: str = Field(max_length=50, nullable=False)
    position_name: str = Field(max_length=50, nullable=False)

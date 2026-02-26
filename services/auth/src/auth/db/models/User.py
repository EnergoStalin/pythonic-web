from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    login: str = Field(max_length=50, unique=True, nullable=False)
    password: str = Field(max_length=50, nullable=False)

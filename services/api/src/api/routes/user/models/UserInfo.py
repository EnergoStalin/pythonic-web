from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    login: str
    password: str
    last_name: str | None = None
    first_name: str | None = None
    surname: str | None = None
    company_name: str | None = None
    position_name: str | None = None

from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    login: str
    password: str
    last_name: str
    first_name: str
    surname: str
    company_name: str
    position_name: str

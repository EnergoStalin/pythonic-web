from pydantic import BaseModel


class Validator(BaseModel):
    regex: str
    description: str

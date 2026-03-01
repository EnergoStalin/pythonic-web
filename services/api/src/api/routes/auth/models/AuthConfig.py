from api.common.models.Validator import Validator
from pydantic import BaseModel


class Validation(BaseModel):
    login: Validator
    password: Validator


class AuthConfig(BaseModel):
    validation: Validation

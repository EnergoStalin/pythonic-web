from fastapi.responses import JSONResponse
from pydantic import BaseModel


class JSONErrorModel(BaseModel):
    error: str


class JSONErrorResponse(JSONResponse):
    def __init__(self, content, **kwargs) -> None:
        super().__init__(
            JSONErrorModel(error=str(content)).model_dump(), **kwargs
        )

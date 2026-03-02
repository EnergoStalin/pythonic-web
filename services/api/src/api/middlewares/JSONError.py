from typing import final

from starlette.types import ASGIApp, Receive, Scope, Send

from api.common.models.JSONErrorResponse import JSONErrorResponse

def unwind_error_type_names(ex: BaseException):
    names = [type(ex).__name__]
    while ex.__cause__:
        ex = ex.__cause__
        names.append(type(ex).__name__)
    return names

@final
class JSONErrorMiddleware:
    def __init__(self, app: ASGIApp, is_dev: bool) -> None:
        self.is_dev = is_dev
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except Exception as ex:
            if self.is_dev:
                print(f"{ex}")
            response = JSONErrorResponse(f"Unhandled error chain {unwind_error_type_names(ex)}")
            await response(scope, receive, send)

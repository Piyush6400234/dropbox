from fastapi import FastAPI, Request
import toml
from src.logging import configure_logging
from pydantic import BaseModel
import traceback
from typing import Optional
from src.app.api.router import api_router
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .lifetime import register_shutdown_event, register_startup_event

class ExceptionResponseModel(BaseModel):
    success: bool = False
    exception_type: str
    message: str
    stack: Optional[str]


class APIException(Exception):
    def __init__(self, message: str):
        self.message = message.lower()


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next) -> JSONResponse:

        try:
            return await call_next(request)
        except APIException as e:

            stack_trace = (
                traceback.format_exc()
            )

            response = ExceptionResponseModel(
                exception_type = e.__class__.__name__,
                message = e.message,
                stack = stack_trace, 
            )

            return JSONResponse(status_code=400, content=response.dict())

        except Exception as e:

            stack_trace = (traceback.format_exc())

            response = ExceptionResponseModel(
                exception_type=e.__class__.__name__, message=str(e), stack=stack_trace
            )

            return JSONResponse(status_code=500, content=response.dict())




def get_app() -> FastAPI:

    """

    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()

    file_path = "pyproject.toml"
    

    with open(file_path, "r") as toml_file:
        data = toml.loads(toml_file.read())

    app = FastAPI(
        title="DropBox",
        version=data['project']['version'],
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )
    
    register_startup_event(app)
    register_shutdown_event(app)



    app.add_middleware(ExceptionHandlerMiddleware)

# Main router for the API.

    app.include_router(
        router=api_router,
        prefix="/api",
        responses={
        400: {
            "model": ExceptionResponseModel,
            "description": "Bad Request",
        },
        500: {
            "model": ExceptionResponseModel,
            "description": "Internal Server Error",
            },
        },
    )

    return app
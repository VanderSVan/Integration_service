from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from integration_service.application import use_cases
from integration_service.application.errors import (
    Error, ErrorsList
)
from .routers import email_validation_router, get_task_handler


def create_app(api_title: str,
               api_version: str,
               api_prefix: str,
               docs_url: str,
               redoc_url: str,
               openapi_url: str,
               task_handler: use_cases.TaskHandler
               ) -> FastAPI:
    app = FastAPI(
        title=api_title,
        version=api_version,
        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url
    )

    # Подключение маршрутов
    app.include_router(email_validation_router, prefix=api_prefix)

    # Обработка ошибок
    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content=exc.errors()
        )

    @app.exception_handler(Error)
    async def app_error_handler(request: Request, exc: Error):
        return JSONResponse(
            status_code=400,
            content=[{
                'type': exc.code,
                'msg': exc.message,
                'ctx': exc.context
            }]
        )

    @app.exception_handler(ErrorsList)
    async def app_errors_list_handler(request: Request, exc: ErrorsList):
        return JSONResponse(
            status_code=400,
            content=[
                {'type': e.code,
                 'msg': e.message,
                 'ctx': e.context}
                for e in exc.errors
            ]
        )

    # Подключение зависимостей
    app.dependency_overrides[get_task_handler] = lambda: task_handler

    return app

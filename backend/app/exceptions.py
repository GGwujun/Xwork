from __future__ import annotations

import logging
from typing import Any

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from .logger import get_request_id

logger = logging.getLogger(__name__)


class ErrorResponse(BaseModel):
    code: str
    message: str
    request_id: str | None = None


class AppError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def _response(code: str, message: str, status_code: int) -> JSONResponse:
    payload = ErrorResponse(code=code, message=message, request_id=get_request_id())
    return JSONResponse(status_code=status_code, content=payload.model_dump())


def register_exception_handlers(app) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_request: Request, exc: AppError) -> JSONResponse:
        if exc.status_code >= 500:
            logger.error(
                "App error: %s",
                exc.message,
                extra={"code": exc.code, "status_code": exc.status_code, "path": str(_request.url)},
                exc_info=exc,
            )
        return _response(exc.code, exc.message, exc.status_code)

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
        status_code = exc.status_code
        if status_code >= 500:
            logger.error(
                "HTTP error: %s",
                exc,
                extra={"path": str(request.url), "status_code": status_code, "code": "http_error"},
                exc_info=exc,
            )
            message = "Internal server error"
        else:
            message = exc.detail if isinstance(exc.detail, str) else "Request failed"
        return _response("http_error", message, status_code)

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.error(
            "Unhandled error: %s",
            exc,
            extra={"path": str(request.url), "code": "internal_error"},
            exc_info=exc,
        )
        return _response("internal_error", "Internal server error", HTTP_500_INTERNAL_SERVER_ERROR)

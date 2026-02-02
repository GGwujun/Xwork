from __future__ import annotations

import json
import logging
import os
import sys
import time
import uuid
from contextvars import ContextVar
from typing import Any
from logging.handlers import RotatingFileHandler

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

_EXTRA_FIELDS = (
    "path",
    "method",
    "status_code",
    "status",
    "duration_ms",
    "code",
    "operation",
    "provider",
    "model",
    "project",
    "version_id",
    "file_path",
    "count",
    "collection",
    "item_id",
    "item_type",
    "pipeline_id",
    "skill_count",
    "session_id",
    "has_summary",
)

request_logger = logging.getLogger("app.request")


def set_request_id(request_id: str) -> None:
    request_id_var.set(request_id)


def get_request_id() -> str | None:
    return request_id_var.get()


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        set_request_id(request_id)
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        duration_ms = int((time.perf_counter() - start) * 1000)
        request_logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "path": str(request.url),
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        return response


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log: dict[str, Any] = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", None),
            "source": {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName,
            },
        }
        for field in _EXTRA_FIELDS:
            value = getattr(record, field, None)
            if value is not None:
                log[field] = value
        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)
        return json.dumps(log, ensure_ascii=True)


def setup_logging(log_level: str | None = None, log_file: str | None = None) -> None:
    level_name = (log_level or os.getenv("LOG_LEVEL", "INFO")).upper()
    level = getattr(logging, level_name, logging.INFO)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()

    formatter = JsonFormatter()
    request_filter = RequestIdFilter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(request_filter)
    root.addHandler(console_handler)

    default_log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
    default_log_file = os.path.join(default_log_dir, "backend.log")
    file_path = log_file or os.getenv("LOG_FILE") or default_log_file
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file_handler = RotatingFileHandler(
            file_path,
            maxBytes=5_000_000,
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        file_handler.addFilter(request_filter)
        root.addHandler(file_handler)


def attach_request_id(app) -> None:
    app.add_middleware(RequestIdMiddleware)

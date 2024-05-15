import sys
import json
import logging

from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute

from .config import settings


log_level = settings.log_level.value


LOG_FORMAT = "[%(asctime)s] [%(process)d] [%(levelname)s] [%(name)s] %(message)s"
LOG_DEFAULT_HANDLERS = [
    "console",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {
            "handlers": LOG_DEFAULT_HANDLERS,
            "level": "INFO",
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["access"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": log_level,
        "formatter": "verbose",
        "handlers": LOG_DEFAULT_HANDLERS,
    },
}


class SafeLoggingRoute(APIRoute):

    async def custom_route_handler(self, request: Request) -> Response:
        try:
            msg = f"{request.method} {request.url.path} {request.query_params}"
            request_body = await request.body()
            if request_body:
                filtered_body = json.loads(request_body)
                msg += f" {filtered_body}"
            logging.debug(msg)
            response = await super().get_route_handler()(request)
            return response
        except Exception as e:
            logging.error(f"Error handling request {request.url.path}: {str(e)}")
            raise e

    def get_route_handler(self) -> Callable:
        async def custom_route_handler(request: Request) -> Response:
            return await self.custom_route_handler(request)

        return custom_route_handler


logging.basicConfig(
    level=log_level.upper(),
    handlers=[logging.StreamHandler(sys.stdout)],
    format=LOG_FORMAT,
)

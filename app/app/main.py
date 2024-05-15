from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.container import Container

from app import api
from app.api.v1 import api_routers


def create_app():
    container = Container()
    container.wire(modules=[api])
    fastapi_app = FastAPI(
        title=settings.project_name, openapi_url=f"{settings.api_v1_str}/openapi.json"
    )

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
    fastapi_app.container = container
    fastapi_app.include_router(api_routers.api_router, prefix=settings.api_v1_str)
    return fastapi_app


app = create_app()

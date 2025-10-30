import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.api.v1.routers import health as health_router
from app.api.v1.routers import providers as providers_router
from app.api.v1.routers import chat as chat_router


def create_app() -> FastAPI:
    settings = get_settings()
    # Configure basic logging once
    logging.basicConfig(
        level=logging.DEBUG if settings.debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    app = FastAPI(title=settings.project_name, version="0.1.0")

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API routers under versioned prefix
    app.include_router(health_router.router, prefix=f"{settings.api_v1_prefix}")
    app.include_router(providers_router.router, prefix=f"{settings.api_v1_prefix}")
    app.include_router(chat_router.router, prefix=f"{settings.api_v1_prefix}")

    @app.get("/", tags=["root"], summary="Root ping")
    def root() -> dict:
        return {"message": "Welcome to OfficeLifeline API"}

    return app


app = create_app()



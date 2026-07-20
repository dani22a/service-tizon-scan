from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise.contrib.fastapi import register_tortoise

from src.config import get_config
from src.config.tortoise import tortoise_config
from src.controllers import router
from src.middleware.auth import JWTAuthMiddleware


config = get_config()


def create_app() -> FastAPI:
    app = FastAPI(
        title="API",
        version="1.0.0",
        debug=config.DEBUG,
    )

    register_tortoise(
        app,
        config=tortoise_config,
        generate_schemas=config.GENERATE_SCHEMAS,
        add_exception_handlers=True,
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1024,
    )

    app.add_middleware(JWTAuthMiddleware)

    cors_origins = [
        origin.strip().rstrip("/")
        for origin in config.CORS_ORIGINS.split(",")
        if origin.strip()
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_origin_regex=(
            r"https?://[a-zA-Z0-9-]+"
            r"(\.[a-zA-Z0-9-]+)*"
            r"\.easypanel\.host"
        ),
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "OPTIONS",
            "PATCH",
        ],
        allow_headers=[
            "Accept",
            "Authorization",
            "Content-Type",
            "Origin",
            "X-Requested-With",
        ],
        expose_headers=[],
        max_age=60 * 60 * 24,
    )

    app.include_router(
        router,
        prefix="/api/v1",
    )

    public_dir = Path(__file__).parent.parent / "public"
    public_dir.mkdir(parents=True, exist_ok=True)

    app.mount(
        "/public",
        StaticFiles(directory=str(public_dir)),
        name="public",
    )

    return app
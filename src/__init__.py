from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.config import get_config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from src.controllers import router
from tortoise.contrib.fastapi import register_tortoise
from src.config.tortoise import tortoise_config
from src.middleware.auth import JWTAuthMiddleware
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

config = get_config()

def create_app() -> FastAPI:
  app = FastAPI(
    title="API",
    version="1.0.0",
    debug=config.DEBUG,
  )

  app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=60 * 60 * 24, # 10 days
  )
  
  register_tortoise(
    app,
    config=tortoise_config,
    generate_schemas=True,
    add_exception_handlers=True
  )
  
  app.add_middleware(GZipMiddleware, minimum_size=1024)
  
  app.add_middleware(JWTAuthMiddleware)

  app.include_router(router, prefix="/api/v1")

  public_dir = Path(__file__).parent.parent / "public"
  public_dir.mkdir(parents=True, exist_ok=True)
  app.mount("/public", StaticFiles(directory=str(public_dir)), name="public")

  return app
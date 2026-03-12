from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database.start.connection import start_connection, stop_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
  await start_connection()
  yield
  await stop_connection()
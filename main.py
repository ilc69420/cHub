from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.register_routers import register_routers
from database.code.setup_db import setup_databases

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_databases()
    register_routers(app)
    yield

app = FastAPI(lifespan=lifespan)
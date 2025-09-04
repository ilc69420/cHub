from fastapi import FastAPI
from routers.proxy_routes import proxy_router


def register_routers(app: FastAPI):
    app.include_router(proxy_router)
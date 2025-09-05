from fastapi import FastAPI
from routers.proxy_routes import proxy_router
from routers.pokemon_routes import pokemon_router

def register_routers(app: FastAPI):
    app.include_router(proxy_router)
    app.include_router(pokemon_router)
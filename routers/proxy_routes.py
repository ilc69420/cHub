from fastapi import APIRouter, HTTPException

from database.code.proxies import ProxyDB
from models.models import proxyModel


proxy_router = APIRouter(
    prefix="/proxies",
    tags=["proxies"]    
)

proxyDB = ProxyDB()

@proxy_router.get("/fetch-proxies")
async def get_proxies():
    return await proxyDB.get_proxies()

@proxy_router.post('/insert-proxies')
async def insert_proxies(proxies: list[proxyModel]):
    err = await proxyDB.insert_proxies(proxies)
    if err != None:
        raise HTTPException(status_code=500, detail='Could not insert proxies into the DB')
    return {'messagg':'Inserted proxies into DB'}


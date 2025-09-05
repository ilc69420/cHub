from .proxies import ProxyDB
from .pokemon import Pokemon_DB

async def setup_databases():
    proxy_db = ProxyDB()
    await proxy_db.setup_tables()

    pokemon_db = Pokemon_DB()
    await pokemon_db.setup_tables()
from .proxies import ProxyDB

async def setup_databases():
    db = ProxyDB()
    await db.setUpTables()
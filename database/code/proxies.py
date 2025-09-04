import aiosqlite
from models import proxyModel


class ProxyDB:
  def __init__(self, dbname: str):
    self.dbname = dbname

  async def setUpTables(self) -> Exception | None:
    async with aiosqlite.connect(self.dbname) as c:
      c.execute("""
        CREATE TABLE IF NOT EXISTS proxies (
          proxy TEXT NOT NULL,
          checked INTEGER DEFAULT 0,
          UNIQUE (proxy),
        )
      """)
      await c.commit()

  async def get_proxies(self) -> list[proxyModel]:
    proxies = []
    async with aiosqlite.connect(self.dbname) as db:
      async with db.execute("SELECT * FROM proxies ORDER BY checked ASC LIMIT 5") as cursor:
        rows = await cursor.fetchall()
        for row in rows:
          proxies.append(row[0])
    return proxies

  async def insert_proxies(self, proxies: list[proxyModel]):
    async with aiosqlite.connect(self.dbname) as db:
      try:
        db.executemany("INSERT OR IGNORE INTO proxies (proxy) VALUES (?)", [(p.proxy,) for p in proxies])
      except Exception as e:
        await db.rollback()

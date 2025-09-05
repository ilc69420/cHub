import aiosqlite
from pathlib import Path
from models.models import proxyModel


class ProxyDB:
    def __init__(self):
        # Resolve path relative to this file's location
        base_dir = Path(__file__).resolve().parent.parent / "databases"
        base_dir.mkdir(parents=True, exist_ok=True)  # ensure folder exists
        self.dbname = base_dir / "proxies.db"

    async def setup_tables(self) -> Exception | None:
        try:
            async with aiosqlite.connect(self.dbname) as db:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS proxies (
                        proxy TEXT NOT NULL UNIQUE,
                        checked INTEGER DEFAULT 0
                    )
                """)
                await db.commit()
            return None
        except Exception as e:
            return e

    async def get_proxies(self) -> list[str]:
        proxies = []
        async with aiosqlite.connect(self.dbname) as db:
            async with db.execute("SELECT proxy FROM proxies ORDER BY checked ASC LIMIT 5") as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    proxies.append(row[0])
        return proxies

    async def insert_proxies(self, proxies: list[proxyModel]) -> Exception | None:
        try:
            async with aiosqlite.connect(self.dbname) as db:
                await db.executemany(
                    "INSERT OR IGNORE INTO proxies (proxy) VALUES (?)",
                    [(p.proxy,) for p in proxies]
                )
                await db.commit()
            return None
        except Exception as e:
            return e

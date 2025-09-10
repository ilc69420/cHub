import aiosqlite
from pathlib import Path
from models.models import Pokemon_Auction_Ended, Pokemon_Que_Item, Pokemon_Auction_Avg, Pokemon_Auction_Active

class Pokemon_DB:
    def __init__(self):
        # Resolve path relative to this file's location
        base_dir = Path(__file__).resolve().parent.parent / "databases"
        base_dir.mkdir(parents=True, exist_ok=True)  # ensure folder exists
        self.dbname = base_dir / "pokemon.db"
    
    async def setup_tables(self):
        async with aiosqlite.connect(self.dbname) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS pokemon_que (
                    name TEXT,
                    number TEXT,
                    card_set TEXT,
                    checked INTEGER DEFAULT 0,
                    UNIQUE(name, number, card_set)
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS pokemon_auctions_ended (
                    name TEXT,
                    number TEXT,
                    card_set TEXT,
                    price INTEGER,
                    seller TEXT,
                    UNIQUE(name, number, card_set, price, seller)
                )
            """)
            await db.execute("""
                CREATE TABLE IF NOT EXISTS pokemon_auctions_avg (
                    name TEXT,
                    number TEXT,
                    card_set TEXT,
                    avg_price INTEGER,
                    UNIQUE(name, number, card_set)
                )
            """)   
            await db.execute("""
                CREATE TABLE IF NOT EXISTS pokemon_auctions_active (
                    name TEXT,
                    number TEXT,
                    card_set TEXT,
                    price INTEGER,
                    seller TEXT,
                    title TEXT,
                    rating TEXT,
                    UNIQUE(name, number, card_set, price, seller, title, rating)
                )
            """)


            await db.commit()
    
    async def insert_into_pokemon_que(self, cards: list[Pokemon_Que_Item]):
        async with aiosqlite.connect(self.dbname) as db:
            await db.executemany("""
                INSERT OR IGNORE INTO pokemon_que (name, number, card_set)
                VALUES (?,?,?)
            """, [(c.name, c.number, c.card_set) for c in cards])
            await db.commit()
    
    async def fetch_que(self) -> list[Pokemon_Que_Item] | None:
        async with aiosqlite.connect(self.dbname) as db:
            async with db.execute(
                'SELECT name, number, card_set FROM pokemon_que WHERE checked = 0 LIMIT 20'
            ) as cursor:
                rows = await cursor.fetchall()

            if not rows:
                # table is empty
                await db.execute('UPDATE pokemon_que SET checked = 0')
                await db.commit()
                async with db.execute(
                    'SELECT name, number, card_set FROM pokemon_que WHERE checked = 0'
                ) as cursor:
                    rows = await cursor.fetchall()

            await db.commit()

            que_items = [Pokemon_Que_Item(name=row[0], number=row[1], card_set=row[2]) for row in rows]
            return que_items



    async def insert_into_ended_auctions_table(self, data: list[Pokemon_Auction_Ended]):
        async with aiosqlite.connect(self.dbname) as db:
            await db.executemany("""
                INSERT OR IGNORE INTO pokemon_auctions_ended (name, number, card_set, price, seller)
                VALUES (?,?,?,?,?)
            """, [(d.name, d.number, d.card_set, d.price, d.seller) for d in data])
            await db.commit()

            await db.execute("UPDATE pokemon_que SET checked = 1 WHERE name = ? AND number = ? AND card_set = ?", (data[0].name, data[0].number, data[0].card_set))
            await db.commit()

    async def insert_into_avg_table(self, data: list[Pokemon_Auction_Avg]):
        async with aiosqlite.connect(self.dbname) as db:
            await db.executemany("""
                INSERT INTO pokemon_auctions_avg (name, number, card_set, avg_price)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name, number, card_set) DO UPDATE SET
                    avg_price = excluded.avg_price
            """, [(d.name, d.number, d.card_set, d.avg_price) for d in data])
            await db.commit()

    async def insert_into_active_auction(self, data: list[Pokemon_Auction_Active]):
        async with aiosqlite.connect(self.dbname) as db:
            await db.executemany("""
                INSERT INTO pokemon_auctions_active (name, number, card_set, price, seller, title)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [(d.name, d.number, d.card_set, d.price, d.seller, d.title) for d in data])
            await db.commit()

    async def fetch_active_auctions(self) -> list[Pokemon_Auction_Active] | None:
        async with aiosqlite.connect(self.dbname) as db:
            async with db.execute(
                'SELECT name, number, card_set, price, seller, title FROM pokemon_auctions_active'
            ) as cursor:
                rows = await cursor.fetchall()
            await db.commit()
            return [Pokemon_Auction_Active(name=row[0], number=row[1], card_set=row[2], price=row[3], seller=row[4], title=row[5]) for row in rows]
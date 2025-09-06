import aiosqlite
from pathlib import Path
from models.models import Pokemon_Scraped_Data, Pokemon_Que_Item

class Pokemon_DB:
    def __init__(self):
        # Resolve path relative to this file's location
        base_dir = Path(__file__).resolve().parent.parent / "databases"
        base_dir.mkdir(parents=True, exist_ok=True)  # ensure folder exists
        self.dbname = base_dir / "pokemon.db"
        print(f"Pokemon DB: {self.dbname}")
    
    async def setup_tables(self):
        print("Setting up tables")
        async with aiosqlite.connect(self.dbname) as db:
            try:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS pokemon_que (
                        name TEXT,
                        number TEXT,
                        card_set TEXT,
                        checked INTEGER DEFAULT 0,
                        UNIQUE(name, number, card_set)
                    )
                """)
                await db.commit()

                await db.execute("""
                    CREATE TABLE IF NOT EXISTS pokemon_scraped_data (
                        name TEXT,
                        number TEXT,
                        card_set TEXT,
                        price INTEGER,
                        seller TEXT,
                        UNIQUE(name, number, card_set, price, seller)
                    )
                """)
                await db.commit()
            except Exception as e:
                print(f"ERROR: {e}")
        
        print("DEBUG: Tables setup")
    
    async def insert_into_pokemon_que(self, cards: list[Pokemon_Que_Item]):
        print(f"Inserting {len(cards)} items into pokemon_que")
        async with aiosqlite.connect(self.dbname) as db:
            await db.executemany("""
                INSERT OR IGNORE INTO pokemon_que (name, number, card_set)
                VALUES (?,?,?)
            """, [(c.name, c.number, c.card_set) for c in cards])
            await db.commit()
        
        print("DEBUG: Inserted into pokemon_que")
    
    async def fetch_que(self) -> Pokemon_Que_Item | None:
        print("Fetching from pokemon_que")
        async with aiosqlite.connect(self.dbname) as db:
            async with db.execute(
                'SELECT name, number, card_set FROM pokemon_que WHERE checked = 0 LIMIT 1'
            ) as cursor:
                row = await cursor.fetchone()

            # reset queue if empty
            if row is None:
                await db.execute('UPDATE pokemon_que SET checked = 0')
                await db.commit()
                async with db.execute(
                    'SELECT name, number, card_set FROM pokemon_que WHERE checked = 0 LIMIT 1'
                ) as cursor:
                    row = await cursor.fetchone()
                
                if row is None:
                    # table is empty
                    return None

            # mark as checked
            await db.execute(
                'UPDATE pokemon_que SET checked = 1 WHERE name = ? AND number = ? AND card_set = ?',
                (row[0], row[1], row[2])
            )
            await db.commit()

            que_item = Pokemon_Que_Item(name=row[0], number=row[1], card_set=row[2])
            print(f"Fetched {que_item}")
            return que_item



    async def insert_into_scraped_table(self, data: list[Pokemon_Scraped_Data]):
        print(f"Inserting {len(data)} items into scraped table")
        async with aiosqlite.connect(self.dbname) as db:
            await db.executemany("""
                INSERT OR IGNORE INTO pokemon_scraped_data (name, number, card_set, price, seller)
                VALUES (?,?,?,?,?)
            """, [(d.name, d.number, d.card_set, d.price, d.seller) for d in data])
            await db.commit()
        print("DEBUG: Inserted into scraped table")



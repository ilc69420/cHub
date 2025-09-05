import aiosqlite
from pathlib import Path

class Pokemon_DB:
    def __init__(self):
        # Resolve path relative to this file's location
        base_dir = Path(__file__).resolve().parent.parent / "databases"
        base_dir.mkdir(parents=True, exist_ok=True)  # ensure folder exists
        self.dbname = base_dir / "pokemon.db"
    
    async def setup_tables(self):
        async with aiosqlite.connect(self.dbname) as db:
            try:
                await db.execute("""
                    CREATE TABLE IF NOT EXISTS pokemon_que (
                        name TEXT,
                        number TEXT,
                        card_set TEXT,
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
                        shipping INTEGER,
                        seller TEXT
                    )    
                """)

            except Exception as e:
                print(e)

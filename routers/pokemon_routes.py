from fastapi import FastAPI, APIRouter, HTTPException
from database.code.pokemon import Pokemon_DB
from models.models import Pokemon_Que_Item, Pokemon_Scraped_Data

pokemon_router = APIRouter(
    prefix="/pokemon",
    tags=["pokemon"]    
)

pokemonDB = Pokemon_DB()


@pokemon_router.get('/fetch-que')
async def fetch_que_items():
    try:
        que_item = await pokemonDB.fetch_que()
        print(f"Fetched {que_item} from the que")
        return que_item
    except Exception:
        raise HTTPException(status_code=500, detail='could not fetch a item from the que')


@pokemon_router.post('/insert-into-que')
async def insert_cards_into_pokemon_que(cards: list[Pokemon_Que_Item]):
    try:
        print(f"Inserting {len(cards)} items into the que")
        await pokemonDB.insert_into_pokemon_que(cards)
        return {'message':'cards were inserted into the que successfully'}
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail='Could not insert the cards into the que')

@pokemon_router.post('/insert-scraped-data')
async def insert_scraped_data(data: list[Pokemon_Scraped_Data]):
    try:
        print(f"Inserting {len(data)} items into scraped table")
        await pokemonDB.insert_into_scraped_table(data)
    except Exception:
        raise HTTPException(status_code=500, detail='could not insert the scraped data into the table')

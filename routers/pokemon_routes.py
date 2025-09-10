from fastapi import FastAPI, APIRouter, HTTPException
from database.code.pokemon import Pokemon_DB
from models.models import Pokemon_Que_Item, Pokemon_Auction_Ended, Pokemon_Auction_Avg, Pokemon_Auction_Active
import logging

pokemon_router = APIRouter(
    prefix="/pokemon",
    tags=["pokemon"]    
)

pokemonDB = Pokemon_DB()


@pokemon_router.get('/fetch-que')
async def fetch_que_items():
    try:
        que_item = await pokemonDB.fetch_que()
        logging.debug(f"Fetched {que_item} from the que")
        return que_item
    except Exception as e:
        logging.debug(f"DEBUG: {e}")
        raise HTTPException(status_code=500, detail='could not fetch a item from the que')


@pokemon_router.post('/insert-into-que')
async def insert_cards_into_pokemon_que(cards: list[Pokemon_Que_Item]):
    try:
        logging.debug(f"Inserting {len(cards)} items into the que")
        await pokemonDB.insert_into_pokemon_que(cards)
        return {'message':'cards were inserted into the que successfully'}
    except Exception as e:
        logging.debug(f"DEBUG: {e}")
        raise HTTPException(status_code=500, detail='Could not insert the cards into the que')

@pokemon_router.post('/insert-auctions-ended')
async def insert_scraped_data(data: list[Pokemon_Auction_Ended]):
    try:
        logging.debug(f"Inserting {len(data)} items into scraped table")
        await pokemonDB.insert_into_ended_auctions_table(data)
    except Exception as e:
        logging.debug(f"DEBUG: {e}")
        raise HTTPException(status_code=500, detail=f'could not insert the scraped data into the table: {e}')

@pokemon_router.post('/insert-auctions-avg')
async def insert_scraped_data(data: list[Pokemon_Auction_Avg]):
    try:
        logging.debug(f"Inserting {len(data)} items into avg table")
        await pokemonDB.insert_into_avg_table(data)
    except Exception as e:
        logging.debug(f"DEBUG: {e}")
        raise HTTPException(status_code=500, detail=f'could not insert the scraped data into the table: {e}')
    
@pokemon_router.post('/insert-auctions-active')
async def insert_scraped_data(data: list[Pokemon_Auction_Active]):
    try:
        logging.debug(f"Inserting {len(data)} items into active table")
        await pokemonDB.insert_into_active_auction(data)
    except Exception as e:
        logging.debug(f"DEBUG: {e}")
        raise HTTPException(status_code=500, detail=f'could not insert the scraped data into the table: {e}')

@pokemon_router.get('/fetch-active-auctions')
async def fetch_active_auctions():
    try:
        logging.debug(f"Fetching active auctions")
        return await pokemonDB.fetch_active_auctions()
    except Exception as e:
        logging.debug(f"DEBUG: {e}")
        raise HTTPException(status_code=500, detail=f'could not fetch the active auctions: {e}')
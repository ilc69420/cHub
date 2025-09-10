from pydantic import BaseModel

class proxyModel(BaseModel):
    proxy: str

class Pokemon_Que_Item(BaseModel):
    name: str
    number: str
    card_set: str

class Pokemon_Auction_Avg(BaseModel):
    name: str
    number: str
    card_set: str
    avg_price: int

class Pokemon_Auction_Ended(BaseModel):
    name: str
    number: str
    card_set: str
    price: int
    seller: str

class Pokemon_Auction_Active(BaseModel):
    name: str
    number: str
    card_set: str
    price: int
    seller: str
    title: str
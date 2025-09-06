from pydantic import BaseModel

class proxyModel(BaseModel):
    proxy: str

class Pokemon_Que_Item(BaseModel):
    name: str
    number: str
    card_set: str

class Pokemon_Scraped_Data(BaseModel):
    name: str
    number: str
    card_set: str
    price: int
    seller: str
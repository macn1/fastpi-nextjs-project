from pydantic import BaseModel
from typing import List

class AddToCart(BaseModel):
    book_id: int
    quantity: int





class UpdateCartItem(BaseModel):
    book_id: int
    quantity: int

class UpdateCart(BaseModel):
    items: List[UpdateCartItem]
    
    class Config:
        orm_mode = True
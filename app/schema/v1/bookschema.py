from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    stock: int
    pages: int
    author: str
    genre: str
    language: str
    cover_image: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookOut(BookBase):
    id: int
    created: datetime
    updated: Optional[datetime]

    class Config:
        orm_mode = True

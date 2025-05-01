from sqlalchemy import Column, Integer ,ForeignKey
from sqlalchemy.orm import relationship
from app.db.db import Base

class Cartitem(Base):
    __tablename__ = "cart_item"
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    book_id = Column(Integer,ForeignKey("books.id"),nullable=False)
    quantity = Column(Integer,index=True,nullable=False)
    
    book = relationship("Book", back_populates="cart_items")

    

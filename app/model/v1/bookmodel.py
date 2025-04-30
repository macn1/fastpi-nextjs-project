from sqlalchemy import String,Integer,Column,Float,DateTime
from sqlalchemy.sql import func
from app.db.db import Base

class Book(Base):
    __tablename__="books"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,index=True,nullable=False)
    author = Column(String,index=True,nullable=False)
    price = Column(Float,default=0)
    language = Column(String,index=True)
    description = Column(String)
    genre = Column(String,index=True,nullable=False)
    pages = Column(Integer)
    stock = Column(Integer)
    cover_image = Column(String, nullable=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
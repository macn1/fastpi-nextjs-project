from sqlalchemy import Column, String,Integer

from app.db.db import Base

class User (Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username  = Column(String , index=True)
    email = Column (String,unique=True,index=True)
    mobile = Column(String,unique=True,index=True)
    password = Column(String,index=True)
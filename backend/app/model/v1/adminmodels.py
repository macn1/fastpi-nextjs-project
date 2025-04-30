from app.db.db import Base

from sqlalchemy import Column,String,Integer

class Admin(Base):
    __tablename__="admin"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index=True)
    email = Column(String,unique=True,index=True)
    password = Column(String,index=True)

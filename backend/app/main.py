from fastapi import FastAPI
from app.db import Base, engine
from app.api.v1 import userapi

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(userapi.router)

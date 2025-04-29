from fastapi import FastAPI
from app.db.db import Base, engine
from app.api.v1 import userapi

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(userapi.router, prefix="/api/v1")

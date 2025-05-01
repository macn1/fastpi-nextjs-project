from fastapi import FastAPI
from app.db.db import Base, engine
from app.api.v1 import userapi
from app.api.v1 import adminapi
from app.api.v1 import bookapi
from app.api.v1 import cartapi


app = FastAPI()

@app.on_event("startup")
async def on_startup():
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(userapi.router, prefix="/api/v1")
app.include_router(adminapi.router,prefix='/api/v1')
app.include_router(bookapi.router,prefix='/api/v1')
app.include_router(cartapi.router,prefix='/api/v1')

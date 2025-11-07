from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.endpoints import users
from app.db.session import engine
from app.db.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield

app = FastAPI(
    title="уэээ",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(
    users.router,
)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/health")
async def health():
    return {"status": "OK"}
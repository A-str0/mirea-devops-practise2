from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager

from app.api.endpoints import users, login
from app.db.session import engine
from app.db.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="уэээээ",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(login.router)

@app.get("/health")
async def health():
    return {"status": "OK"}

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=open("frontend/index.html").read())

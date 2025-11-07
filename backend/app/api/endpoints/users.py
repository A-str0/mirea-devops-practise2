from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import User
from app.crud import create_user, get_user, get_users
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201)
async def create_user_endpoint(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    
    # if result.scalar_one_or_none():
    #     raise HTTPException(400, "Email already registered")
    
    user = await create_user(db, user_in)
    return user

@router.get("/", response_model=UserRead)
async def get_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)):
    # result = await db.execute(select(User).where(User.id == user_id))
    
    # if result.scalar_one_or_none():
    #     raise HTTPException(400, f"No user with id {user_id}")
    user = await get_user(db, user_id)
    return user

@router.get("/users", response_model=UserRead)
async def get_users_endpoint(db: AsyncSession = Depends(get_db)):
    users = await get_users(db)
    return users[0] # TODO: some stuff
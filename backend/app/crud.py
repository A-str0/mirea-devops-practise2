from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed = pwd_context.hash(user_in.password)
    
    db_user = User(
        email=user_in.email,
        nickname=user_in.nickname,
        hashed_password=hashed,
    )
    
    db.add(db_user)
    
    await db.commit()
    await db.refresh(db_user)
    
    return db_user

async def get_user(db: AsyncSession, user_id: int):
    return await db.get(User, user_id)
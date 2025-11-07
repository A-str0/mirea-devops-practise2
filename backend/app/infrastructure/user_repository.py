from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.user import User
from app.db.models import User as UserModel

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: User) -> User:
        db_user = UserModel(
            email=user.email,
            nickname=user.nickname,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            is_superuser=user.is_superuser
        )
        
        self.db.add(db_user)
        
        await self.db.commit()
        await self.db.refresh(db_user)
        
        return User.model_validate(db_user)

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.execute(select(UserModel).where(UserModel.id == user_id))
        
        db_user = result.scalar_one_or_none()
        
        return User.model_validate(db_user) if db_user else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        
        db_user = result.scalar_one_or_none()
        
        return User.model_validate(db_user) if db_user else None

    async def get_all(self) -> list[User]:
        result = await self.db.execute(select(UserModel))
        
        db_users = result.scalars().all()
        
        return [User.model_validate(db_user) for db_user in db_users]

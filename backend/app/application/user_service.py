import bcrypt

from app.domain.user import User
from app.domain.value_objects import Email, Password
from app.infrastructure.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, email: Email, nickname: str, password: Password) -> User:
        existing_user = await self.repository.get_by_email(email.value)
        
        if existing_user:
            raise ValueError("Email already registered")

        hashed = bcrypt.hashpw(password.value.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        user = User(
            email=email.value,
            nickname=nickname,
            hashed_password=hashed
        )
        return await self.repository.create(user)

    async def get_user(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        return user

    async def get_users(self) -> list[User]:
        return await self.repository.get_all()

    async def authenticate_user(self, email: Email, password: Password) -> User:
        user = await self.repository.get_by_email(email.value)
        if not user:
            raise ValueError("Invalid credentials")

        if not bcrypt.checkpw(password.value.encode('utf-8'), user.hashed_password.encode('utf-8')):
            raise ValueError("Invalid credentials")

        return user

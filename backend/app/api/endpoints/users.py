from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserCreate, UserRead
from app.infrastructure.user_repository import UserRepository
from app.application.user_service import UserService
from app.domain.value_objects import Email, Password

router = APIRouter(prefix="/api/users", tags=["users"])

def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)

@router.post("/", response_model=UserRead, status_code=201)
async def create_user_endpoint(user_in: UserCreate, service: UserService = Depends(get_user_service)):
    try:
        user = await service.create_user(
            Email(value=user_in.email),
            user_in.nickname,
            Password(value=user_in.password)
        )
        
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserRead)
async def get_user_endpoint(user_id: int, service: UserService = Depends(get_user_service)):
    try:
        return await service.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=list[UserRead])
async def get_users_endpoint(service: UserService = Depends(get_user_service)):
    users = await service.get_users()
    return users

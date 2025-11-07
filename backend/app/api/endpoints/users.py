from fastapi import APIRouter

from app import crud


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/")
def create_user():
    # user = crud.create_user()

    pass
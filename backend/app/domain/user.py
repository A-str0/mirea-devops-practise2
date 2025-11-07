from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    nickname: str = Field(..., min_length=3, max_length=50)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False

    class Config:
        from_attributes = True

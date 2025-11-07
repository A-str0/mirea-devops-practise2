from pydantic import BaseModel, EmailStr, Field

class Email(BaseModel):
    value: EmailStr

class Password(BaseModel):
    value: str = Field(..., min_length=8, max_length=72)

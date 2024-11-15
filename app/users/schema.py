from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CreateUserRequestSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None


class CreateUserResponseSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class GetUsersResponseSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


class GetUserResponseSchema(BaseModel):
    id: int
    is_active: bool
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UpdateUserRequestSchema(BaseModel):
    is_active: Optional[bool] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
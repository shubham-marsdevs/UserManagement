import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.users import schema as user_schema
from app.db_config import get_db
from app.users import services as user_service
from app.authentication import services as authentication_service
from app.authentication.exceptions import permission_error


user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post("/", response_model=user_schema.CreateUserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: user_schema.CreateUserRequestSchema, db: AsyncSession = Depends(get_db)):
    try:
        print("fjsdofjdofjdosifjodsjfosdjfoidsjfo")
        user_obj = await user_service.create_user(db, user)
        return user_obj
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.get("/all", response_model=List[Optional[user_schema.GetUsersResponseSchema]])
async def get_users(
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)):
    try:
        user_objs = await user_service.get_users(db, search, is_active, skip, limit)
        return user_objs
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@user_router.get("/{user_id}", response_model=user_schema.GetUserResponseSchema)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(authentication_service.get_current_user)):
    if current_user.id != user_id:
        raise permission_error
    user = await user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User  not found")
    return user


@user_router.put("/{user_id}", response_model=user_schema.GetUserResponseSchema)
async def update_user(
    user_id: int,
    user: user_schema.UpdateUserRequestSchema,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(authentication_service.get_current_user)):
    if current_user.id != user_id:
        raise permission_error
    user_obj = await user_service.get_user(db, user_id)
    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_obj, key, value)

    user_obj = await user_service.update_user(db, user_obj)
    return user_obj


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(authentication_service.get_current_user)):
    if current_user.id != user_id:
        raise permission_error
    user = await user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        await db.delete(user)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Unexpected Error Occurred")

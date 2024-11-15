from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional

from app.users import models, schema as user_schema
from app.authentication import utils


async def create_user(db: AsyncSession, user: user_schema.CreateUserRequestSchema):
    result = await db.execute(select(models.User).filter(models.User.email == user.email))
    user_exist = result.scalar_one_or_none()
    if user_exist:
        raise ValueError(f"User already exist with email id - {user.email}")
    
    hashed_password = utils.get_password_hash(user.password)
    user_obj = models.User(
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
    )

    db.add(user_obj)
    try:
        await db.commit()
        await db.refresh(user_obj)
    except IntegrityError as e:
        await db.rollback()
        raise ValueError(f"User already exist with email id - {user.email}") from e
    except Exception as e:
        # Handle any other exceptions that may arise
        await db.rollback()
        print(f"{e=}")
        raise ValueError("Not able to update: An unexpected error occurred.") from e
    return user_obj


async def get_users(
        db: AsyncSession,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100):
    query = select(models.User)
    # searching on first_name and last_name field
    if search:
        query = query.filter(
            (models.User.first_name.ilike(f'%{search}%')) | (models.User.last_name.ilike(f'%{search}%'))
        )
    # filtering on is_active field
    if is_active is not None:
        query = query.where(models.User.is_active == is_active)
    # pagination
    result = await db.execute(query.offset(skip).limit(limit))
    users = result.scalars().all()
    return users


async def get_user(db: AsyncSession, user_id: int):
    query = select(models.User).where(models.User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def update_user(db: AsyncSession, user_obj: models.User):
    try:
        db.add(user_obj)
        await db.commit()
        await db.refresh(user_obj)
    except IntegrityError as e:
        await db.rollback()
        raise ValueError("Not able to update: Integrity error.") from e
    except Exception as e:
        # Handle any other exceptions that may arise
        await db.rollback()
        raise ValueError("Not able to update: An unexpected error occurred.") from e
    return user_obj


async def get_user_by_email(db: AsyncSession, email: EmailStr):
    query = select(models.User).where(models.User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    return user

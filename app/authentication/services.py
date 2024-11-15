from pydantic import EmailStr
from fastapi import Depends
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.authentication.exceptions import credentials_exception
from app.db_config import get_db
from app.settings import SECRET_KEY, ALGORITHM
from app.users import services as user_service
from app.authentication.utils import verify_password, oauth2_scheme
from app.authentication import schema as authentication_schema


async def authenticate_user(db: AsyncSession, email: EmailStr, password: str):
    user = await user_service.get_user_by_email(db, email)
    if user and verify_password(password, user.password):
        return user
    return False


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = authentication_schema.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await user_service.get_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user
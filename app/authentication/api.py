from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db_config import get_db
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from app.authentication import schema as authentication_schema
from app.authentication import services as authentication_service
from app.authentication import utils


authentication_router = APIRouter(prefix="/authentication", tags=["Authentication"])


@authentication_router.post("/token", response_model=authentication_schema.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    authenticated_user = await authentication_service.authenticate_user(db, form_data.username, form_data.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"email": authenticated_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

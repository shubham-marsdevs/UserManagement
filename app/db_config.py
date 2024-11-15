import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


database_url = os.getenv("DATABASE_URI", "")

engine = create_async_engine(database_url, echo=True)
SessionLocal = async_sessionmaker(engine)


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()

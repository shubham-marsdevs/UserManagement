import os
from dotenv import load_dotenv

load_dotenv()
import pytest
import pytest_asyncio
from httpx import AsyncClient

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.db_config import get_db, Base


@pytest.fixture(autouse=True)
def set_env_variables():
    assert os.environ.get("TEST_DATABASE_URI") is not None


TEST_DATABASE_URI = os.environ.get("TEST_DATABASE_URI")
engine = create_async_engine(TEST_DATABASE_URI, echo=True)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Create a new database session for a test and roll it back after the test."""
    # Create a new session

    async with engine.begin() as conn:
        # Create the database schema
        await conn.run_sync(Base.metadata.create_all)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()


@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Provide a TestClient that uses the test database session."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db  # Override the get_db dependency

    async with AsyncClient(app=app, base_url="http://localhost") as c:
        yield c

    app.dependency_overrides.clear()  # Clear the overrides after the test


@pytest_asyncio.fixture
async def token(client: AsyncClient):
    # Here you would typically log in to get the token
    response = await client.post(
        "/api/authentication/token",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    return response.json().get("access_token")
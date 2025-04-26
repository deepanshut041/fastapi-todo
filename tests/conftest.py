import os
import pytest
import asyncio
from httpx import ASGITransport, AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
from fastapi.testclient import TestClient
from sqlalchemy import delete

os.environ["POSTGRES_DB"] = os.environ['POSTGRES_DB_TEST']

from core.config import settings
from models import Todo
from api.deps import get_async_db_session
from main import app

pytest_plugins = ("pytest_asyncio",)
pytestmark = pytest.mark.asyncio

# Apply migrations once before the test session
@pytest.fixture(scope="session", autouse=True)
def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


# Provide an async DB session for each test
@pytest_asyncio.fixture
async def test_db_session():
    # >>> Create engine INSIDE the fixture
    engine_test = create_async_engine(settings.POSTGRES_DSN, echo=False)
    async_session = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        yield session
    await engine_test.dispose()  # <- IMPORTANT: close engine after test


@pytest_asyncio.fixture
async def client(test_db_session: AsyncSession):
    async def override_get_session():
        yield test_db_session

    app.dependency_overrides[get_async_db_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def cleanup_todos(test_db_session: AsyncSession):
    yield
    await test_db_session.execute(delete(Todo))
    await test_db_session.commit()

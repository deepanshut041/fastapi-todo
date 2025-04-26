
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings  # Import your settings


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None
    def __getattr__(self, name):
            return getattr(self._session, name)
    def init(self):
            self._engine = create_async_engine(
                str(settings.POSTGRES_DSN),
                future=True,
                echo=True,
            )
            self._session = sessionmaker(
                self._engine, expire_on_commit=False, class_=AsyncSession
            )()
    async def create_all(self):
        self._engine.begin

db=AsyncDatabaseSession()

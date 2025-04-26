from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import db  # Your AsyncDatabaseSession instance

async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    if db._session is None:
        db.init()
    try:
        yield db._session
    finally:
        await db._session.close()
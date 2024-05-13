from sqlalchemy import create_engine, text, insert, select
from sqlalchemy.ext.asyncio import create_async_engine
from .db_settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_utils import database_exists, create_database

ur_a = settings.POSTGRES_DATABASE_URLA

engine_a = create_async_engine(ur_a, echo=True)

async def get_session():
    async with AsyncSession(engine_a) as session:
        try:
            yield session
        finally:
            session.close()

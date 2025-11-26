from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

engine = create_async_engine(str(settings.database.url), isolation_level="READ COMMITTED")

session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_database_session() -> AsyncGenerator[AsyncSession, None, None]:
    """Dependency to get a database session."""
    session = session_maker()
    try:
        yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    else:
        await session.commit()
    finally:
        await session.close()

from typing import Callable, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from contextlib import asynccontextmanager

from src.modules.base.entities import Base
from src.common.consts import CommonConsts


__async_engine: Optional[AsyncEngine] = None

def global_init():
    global __async_engine
    if __async_engine:
        return

    DNS = f"mssql+pyodbc://{CommonConsts.BACKEND_DNS}"
    print(DNS)
    ASYNC_DNS = f"mssql+aioodbc://{CommonConsts.BACKEND_DNS}"
    sync_engine = create_engine(DNS, echo=False)
    __async_engine = create_async_engine(ASYNC_DNS, echo=False)

    # from src.modules.entities import User, FakeData
    Base.metadata.create_all(sync_engine)



@asynccontextmanager
async def async_session_scope():
    """Provide a transactional scope around a series of operations."""
    global __async_engine

    if not __async_engine:
        raise Exception("You have to call global_init() before using the session")

    async_session: AsyncSession = AsyncSession(__async_engine)
    async_session.sync_session.expire_on_commit = False

    async with async_session as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
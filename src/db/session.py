import aioodbc
from typing import Callable, Optional

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from contextlib import asynccontextmanager

from src.modules.base.entities import Base
from src.common.consts import CommonConsts



SYNC_DNS = "mssql+pyodbc://khang:123456@Khang/Broker?driver=ODBC+Driver+17+for+SQL+Server"
ASYNC_DNS = CommonConsts.BACKEND_DNS

def global_init():
    global SYNC_DNS
    sync_engine = create_engine(SYNC_DNS, echo=False)
    Base.metadata.create_all(sync_engine)

@asynccontextmanager
async def async_session_scope():
    global ASYNC_DNS

    """Provide a transactional scope around a series of operations."""
    conn = await aioodbc.connect(dsn=ASYNC_DNS)
    try:
        yield conn
        await conn.commit()
    except Exception as e:
        await conn.rollback()
        raise
    finally:
        await conn.close()

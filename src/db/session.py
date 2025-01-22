import os

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

# from app.config import settings
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

odbc_connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};Server=192.168.1.97,1433;Database=Broker;UID=khang;PWD=asd123456;'
sqlalchemy_url = f"mssql+aioodbc:///?odbc_connect={odbc_connection_string}"


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine, expire_on_commit=False)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# sessionmanager = DatabaseSessionManager(settings.database_url, {"echo": settings.echo_sql})
sessionmanager = DatabaseSessionManager(sqlalchemy_url, {"echo": True})


async def async_session_scope():
    async with sessionmanager.session() as session:
        yield session

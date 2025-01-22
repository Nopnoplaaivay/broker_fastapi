import os
import uuid
from contextlib import asynccontextmanager
from typing import AsyncContextManager
from contextvars import ContextVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connectors import AsyncSQLServerConnectorPool
from src.common.consts import CommonConsts
from src.utils.logger import LOGGER

SESSIONS = {}
DNS = CommonConsts.ASYNC_DNS
MIN_CONN = 2
MAX_CONN = 1000

# Use ContextVar for async context
CONTEXTVAR: ContextVar[uuid.UUID] = ContextVar('session_id', default=None)

POOL = AsyncSQLServerConnectorPool(dns=DNS, max_conn=MAX_CONN, min_conn=MIN_CONN)

async def set_session(session: AsyncSession | None) -> None:
    """Set the session for the current context"""
    global SESSIONS
    context_id = CONTEXTVAR.get()
    if session is None:
        if context_id in SESSIONS:
            del SESSIONS[context_id]
        return
    if context_id is None:
        context_id = uuid.uuid4()
    CONTEXTVAR.set(context_id)
    SESSIONS[context_id] = session

def get_session() -> AsyncSession | None:
    """Get the session for the current context"""
    global SESSIONS
    context_id = CONTEXTVAR.get()
    return SESSIONS.get(context_id, None)

@asynccontextmanager
async def backend_session_scope(new: bool = False) -> AsyncContextManager[AsyncSession]:
    """
    Provide an async transactional scope around a series of operations.
    Shouldn't keep session alive too long, it will block a connection of pool connections.
    """
    if not new:
        reuse_session = get_session()
        if reuse_session is None:
            session = POOL.get()
            await set_session(session=session)
        else:
            session = reuse_session
        try:
            yield session
            if reuse_session is None:
                await session.commit()
        except Exception as exception:
            LOGGER.error(exception, exc_info=True)
            if reuse_session is None:
                await session.rollback()
            raise exception
        finally:
            if reuse_session is None:
                await POOL.put(session)
                await set_session(session=None)
    else:
        session = POOL.get()
        try:
            yield session
            await session.commit()
        except Exception as exception:
            LOGGER.error(exception, exc_info=True)
            await session.rollback()
            raise exception
        finally:
            await POOL.put(session)
import asyncio
from sqlalchemy import text
from src.db.session import async_session_scope

async def test_async_session_scope():
    async with async_session_scope() as session:
        result = await session.execute(text("SELECT 1 AS number;"))
        data = result.all()
        assert data[0][0] == 1

if __name__ == "__main__":
    asyncio.run(test_async_session_scope())
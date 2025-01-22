import asyncio
from sqlalchemy import text
from src.db.sessions import backend_session_scope


async def example_usage():
    # Using a new session
    async with backend_session_scope(new=True) as session:
        result = await session.execute(text("SELECT 42 AS age;"))
        data = result.all()
        print(data[0][0])

    # Reusing existing session
    async with backend_session_scope() as session:
        result = await session.execute(text("SELECT 52 AS age;"))
        data = result.all()
        print(data[0][0])

if __name__ == "__main__":
    asyncio.run(example_usage())
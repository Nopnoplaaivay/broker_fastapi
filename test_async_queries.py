import asyncio
import time
from sqlalchemy import text
from src.db.sessions import backend_session_scope

async def test_query():
    async with backend_session_scope() as session:
        start = time.time()
        # Use SQL Server's WAITFOR DELAY to simulate a slow query:
        result = await session.execute(text("WAITFOR DELAY '00:00:01'"))
        print(f"Query finished in {time.time() - start:.2f} seconds")

async def main():
    start = time.time()
    await asyncio.gather(test_query(), test_query(), test_query())
    print(f"Total execution time: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())

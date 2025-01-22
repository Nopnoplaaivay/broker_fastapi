import asyncio
import aioodbc

from src.common.consts import CommonConsts

async def test_example():
    dsn = f"{CommonConsts.BACKEND_DNS}"
    conn = await aioodbc.connect(dsn=dsn)

    cur = await conn.cursor()
    await cur.execute("SELECT 42 AS age;")
    rows = await cur.fetchall()
    print(rows)
    print(rows[0])
    print(rows[0].age)
    await cur.close()
    await conn.close()


asyncio.run(test_example())
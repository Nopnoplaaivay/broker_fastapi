import asyncio
import aioodbc

from src.db import session
from src.common.consts import CommonConsts

async def test_example():
    session.global_init()
    async with session.async_session_scope() as conn:
        async with conn.cursor() as cur:
            # await cursor.execute("SELECT * FROM dbo.users")
            await cur.execute("SELECT 42 AS age;")
            rows = await cur.fetchall()
            for row in rows:
                print(row)


asyncio.run(test_example())

# import pyodbc

# conn_str = "DRIVER={ODBC Driver 17 for SQL Server};Server=Khang,1433;Database=Broker;Trusted_Connection=yes;"
# try:
#     conn = pyodbc.connect(conn_str)
#     print("Connection successful")
#     conn.close()
# except pyodbc.Error as ex:
#     print("Connection failed:", ex)

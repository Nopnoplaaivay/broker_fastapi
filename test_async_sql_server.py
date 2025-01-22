import asyncio
from src.db.connectors import AsyncSQLServerConnectorPool
from src.common.consts import CommonConsts


dns = CommonConsts.DNS
POOL = AsyncSQLServerConnectorPool(dns=dns, max_conn=1000, min_conn=5)
async def main():
    await POOL.initialize()
    async with POOL.get() as session:
        # Your async database operations here
        pass

if __name__ == "__main__":
    asyncio.run(main())
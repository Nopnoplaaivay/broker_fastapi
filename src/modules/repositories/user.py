import asyncio
from sqlalchemy.future import select

from src.db.sessions import backend_session_scope
from src.modules.base.repositories import BaseRepo
from src.modules.entities import User

class UserRepo(BaseRepo[User]):
    entity = User
    async_session_scope = backend_session_scope

    @classmethod
    async def find_by_account(cls, account: str, delay=0, id=1) -> User:
        async with cls.async_session_scope() as session:
            print(f"Request {id} - Start")
            result = await session.execute(select(cls.entity).filter(cls.entity.account == account))
            delay = 0
            await asyncio.sleep(delay)
            print(f"Result {id}: {result}")
            print(f"Request {id} - End")
            return result.scalars().first()
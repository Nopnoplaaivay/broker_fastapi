from sqlalchemy.future import select

from src.db.sessions import backend_session_scope
from src.modules.base.repositories import BaseRepo
from src.modules.entities import User

class UserRepo(BaseRepo[User]):
    entity = User
    async_session_scope = backend_session_scope

    @classmethod
    async def find_by_account(cls, account: str) -> User:
        async with cls.async_session_scope() as session:
            result = await session.execute(select(cls.entity).filter(cls.entity.account == account))
            return result.scalars().first()
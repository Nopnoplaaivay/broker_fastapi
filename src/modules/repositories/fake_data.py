from sqlalchemy.sql.expression import select

from src.db.sessions import backend_session_scope
from src.modules.base.repositories import BaseRepo
from src.modules.entities import FakeData

class FakeDataRepo(BaseRepo[FakeData]):
    entity = FakeData
    async_session_scope = backend_session_scope
    
    @classmethod
    async def get_data_by_account(cls, account: str):
        async with cls.async_session_scope() as session:
            query = select(cls.entity).where(cls.entity.account == account)
            result = await session.execute(query)
            return result.scalars().all()
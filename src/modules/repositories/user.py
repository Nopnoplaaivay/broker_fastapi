from typing import Dict
from src.db.sessions import backend_session_scope
from src.modules.base.repositories import BaseRepo
from src.modules.entities import User

class UserRepo(BaseRepo[User]):
    entity = User
    async_session_scope = backend_session_scope

    # @classmethod
    # async def find_by_email(cls, email: str) -> User:
    #     async with cls.async_session_scope() as session:
    #         return await session.query(cls.entity).filter(cls.entity.email == email).first()

    # @classmethod
    # async def find_by_username(cls, username: str) -> User:
    #     async with cls.async_session_scope() as session:
    #         return await session.query(cls.entity).filter(cls.entity.username == username).first()
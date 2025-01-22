from typing import List, TypeVar, Generic, Dict, Union, Callable
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.base.entities import Base

T = TypeVar("T", bound=Base)

class BaseRepo(Generic[T]):
    entity: T
    async_session_scope: Callable[..., AsyncSession]

    @classmethod
    async def insert_many(cls, data: List[Dict]) -> List[T]:
        async with cls.async_session_scope() as session:
            entities = [cls.entity(**item) for item in data]
            session.add_all(entities)
            await session.commit()
            return entities

    @classmethod
    async def insert(cls, data: Dict) -> T:
        async with cls.async_session_scope() as session:
            entity = cls.entity(**data)
            session.add(entity)
            await session.commit()
            return entity

    @classmethod
    async def find(cls, criteria: Dict) -> List[T]:
        async with cls.async_session_scope() as session:
            query = session.query(cls.entity)
            for key, value in criteria.items():
                query = query.filter(getattr(cls.entity, key) == value)
            return await query.all()

    @classmethod
    async def get_all(cls) -> List[T]:
        async with cls.async_session_scope() as session:
            query = session.query(cls.entity)
            return await query.all()

    @classmethod
    async def get_by_id(cls, id: Union[int, str]) -> T:
        async with cls.async_session_scope() as session:
            return await session.query(cls.entity).filter(cls.entity.id == id).first()
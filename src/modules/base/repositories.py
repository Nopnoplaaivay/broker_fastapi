from typing import List, TypeVar, Generic, Dict, Union, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

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
            query = select(cls.entity)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def update(cls, data: Dict) -> T:
        async with cls.async_session_scope() as session:
            entity = await session.get(cls.entity, data['id'])
            for key, value in data.items():
                setattr(entity, key, value)
            query = select(cls.entity).filter(cls.entity.id == data['id'])
            result = await session.execute(query)

            await session.commit()
            return result.scalars().first()
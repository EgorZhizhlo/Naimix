from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import or_
from .base_model import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find(cls, all: bool = False, or_method: bool = False, **kwargs):
        async with async_session() as session:
            if or_method:
                query = select(cls.model)
                filters = [getattr(cls.model, key) == value for key, value in kwargs.items()]
                query = query.where(or_(*filters))
            else:
                query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            if all:
                return result.scalars().all()
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):
        async with async_session() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

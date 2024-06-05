from typing import Iterable, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from tickets.models.base import BaseDBModel


class BaseRepo:

    model_class: SQLModel = BaseDBModel

    def __init__(self, session: sessionmaker):
        if self.model_class is None:
            raise NotImplementedError("Model class has to be defined")
        self._session: sessionmaker = session

    async def get_by_id(self, id: int) -> model_class:
        async with self._session() as session, session.begin():
            query = select(self.model_class).where(self.model_class.id == id)
            return (await session.exec(query)).first()

    async def save(self, obj) -> model_class:
        async with self._session() as session, session.begin():
            session.add(obj)
            await session.commit()
        return obj  # session.commit() sub-sequentially calls session.flush() , so obj.id is filled

    async def list(self, request: BaseModel | None) -> Iterable[model_class]:
        if request is not None:
            raise NotImplementedError("search by request is not implemented")
        async with self._session() as session, session.begin():
            query = select(self.model_class)
            return await session.exec(query)

    async def bulk_save(self, objs: Iterable[model_class]):
        async with self._session.begin() as session:
            session.add_all(objs)

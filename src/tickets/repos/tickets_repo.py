import datetime
from typing import Iterable

from sqlmodel import select

from base_repo import BaseRepo
from tickets.models.ticket import TicketDB
from tickets.models.requests import TicketsRequest


class TicketsRepo(BaseRepo):
    model_class = TicketDB

    def __init__(self, session_factory):
        super().__init__(session_factory)

    async def list(self, request: TicketsRequest) -> Iterable[model_class]:
        async with self._session.begin():
            query = select(TicketDB)
            query = query.where(TicketDB.departure >= datetime.datetime.now())
            query = query.where(TicketDB.from_ == request.departure_point)
            query = query.where(TicketDB.to == request.destination_point)
            return await self._session.exec(query)


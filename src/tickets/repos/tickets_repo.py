import datetime
from typing import Iterable

from sqlmodel import select, update

from base_repo import BaseRepo
from tickets.errors.ran_out_of_tickets import RanOutOfTicketsError
from tickets.errors.ticket_already_reserved import TicketAlreadyReservedError
from tickets.models.ticket import TicketDB
from tickets.models.requests import TicketsRequest


class TicketsRepo(BaseRepo):
    model_class = TicketDB

    def __init__(self, session_factory):
        super().__init__(session_factory)


    async def list(self, request: TicketsRequest) -> Iterable[model_class]:
        async with self._session() as session, session.begin():
            query = select(self.model_class)
            query = query.where(self.model_class.departure_time >= datetime.datetime.now())
            query = query.where(self.model_class.departure_point == request.departure_point)
            query = query.where(self.model_class.destination_point == request.destination_point)
            return (await session.exec(query)).all()

    async def reserve_by_id(self, ticket_id: int) -> model_class:
        async with self._session.begin() as session:
            query = update(self.model_class).values(is_reserved=True)
            query = query.where(self.model_class.id == ticket_id)
            query = query.where(self.model_class.is_reserved == False)
            query = query.returning(self.model_class)
            result = (await session.exec(query)).first()
        if not result:
            raise TicketAlreadyReservedError(f"Ticket {ticket_id} already reserved", ticket_id=ticket_id)
        return result[0]

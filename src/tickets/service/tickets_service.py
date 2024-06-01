from pydantic import TypeAdapter

from tickets.models.ticket import TicketDB
from tickets.models.requests import TicketsRequest
from tickets.repos.tickets_repo import TicketsRepo


class TicketsService:

    def __init__(self, repo: TicketsRepo):
        self._repo = repo
        self._response_adapter = TypeAdapter(TicketDB)

    async def reserve_ticket(self, ticket_id: int) -> TicketDB:
        ticket = self._repo.get_by_id(ticket_id)
        ticket.reserved = True
        return await self._repo.save(ticket)

    async def search(self, request: TicketsRequest) -> list[TicketDB]:
        return list(await self._repo.list(request))

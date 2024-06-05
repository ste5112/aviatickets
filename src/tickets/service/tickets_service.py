from pydantic import TypeAdapter

from tickets.models.ticket import TicketDB
from tickets.models.requests import TicketsRequest
from tickets.repos.tickets_repo import TicketsRepo


class TicketsService:

    def __init__(self, repo: TicketsRepo):
        self._repo = repo
        self._response_adapter = TypeAdapter(TicketDB)

    async def reserve_ticket_by_id(self, ticket_id: int) -> TicketDB:
        return await self._repo.reserve_by_id(ticket_id)

    async def reserve_ticket_by_race_id(self, race_id: str) -> TicketDB:
        ticket = await self._repo.reserve_by_race_id(race_id)
        return ticket

    async def search(self, request: TicketsRequest) -> list[TicketDB]:
        return list(await self._repo.list(request))

    async def get_by_id(self, ticket_id: int) -> TicketDB:
        return await self._repo.get_by_id(ticket_id)

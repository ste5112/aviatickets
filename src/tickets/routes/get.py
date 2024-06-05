from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Path

from container import AppContainer
from tickets.models.ticket import TicketDB
from tickets.models.requests import TicketsRequest
from tickets.routes.router import api_router as router
from tickets.service.tickets_service import TicketsService


@router.get("/", summary="Get tickets")
@inject
async def get_tickets(
        request: TicketsRequest = Depends(),
        tickets_service: TicketsService = Depends(Provide[AppContainer.tickets_service]),
) -> list[TicketDB]:
    return await tickets_service.search(request)


@router.get("/{ticket_id}/", summary="Get ticket by id")
@inject
async def get_ticket(
        ticket_id: Annotated[int, Path(title="Ticket id")],
        tickets_service: TicketsService = Depends(Provide[AppContainer.tickets_service]),
) -> TicketDB:
    return await tickets_service.get_by_id(ticket_id)

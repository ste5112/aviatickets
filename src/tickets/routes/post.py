from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Path, Depends, HTTPException

from container import AppContainer
from tickets.errors.ticket_already_reserved import TicketAlreadyReservedError
from tickets.models.ticket import TicketDB
from tickets.routes.router import api_router as router
from tickets.service.tickets_service import TicketsService


@router.post("/reserve/{ticket_id}/", summary="Reserve ticket by id")
@inject
async def reserve_ticket_by_id(
        ticket_id: Annotated[int, Path(title="Ticket id")],
        tickets_service: TicketsService = Depends(Provide[AppContainer.tickets_service]),
):
    try:
        return await tickets_service.reserve_ticket_by_id(ticket_id)
    except TicketAlreadyReservedError:
        raise HTTPException(409, "Ticket already reserved")
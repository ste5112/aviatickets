import pytest
import pytest_asyncio
from sqlmodel import select

from tests.functional.races_generator import races_gen
from tickets.models.ticket import TicketDB


@pytest_asyncio.fixture(scope='module')
async def tickets(client):
    repo = client.app.container.tickets_repo()
    tickets = list(races_gen(races_number=100))
    await repo.bulk_save(tickets)
    return tickets


@pytest_asyncio.fixture(scope='module')
async def repo_tickets(client, tickets):
    async with client.app.container._session_factory().begin() as session:
        return (await session.exec(select(TicketDB))).all()


@pytest.mark.asyncio
async def test_db_is_not_empty(repo_tickets):
    assert len(repo_tickets) >= 0


def test_get_tickets(client, tickets):
    data = client.get(
        '/tickets/', params={
            'departure_point': tickets[0].departure_point,
            'destination_point': tickets[0].destination_point,
            'departure_time': tickets[0].departure_time}
    ).json()

    assert len(data) >= 0
    assert isinstance(data[0]['id'], int)

    for i, ticket in enumerate(data):
        assert ticket['departure_point'] == tickets[0].departure_point, ticket.id
        assert ticket['destination_point'] == tickets[0].destination_point, ticket.id


def test_reserve_ticket(client, repo_tickets):

    ticket_id = None
    for ticket in repo_tickets:
        if not ticket.is_reserved:
            ticket_id = ticket.id
            break

    assert ticket_id is not None
    reserved_ticket_response = client.post(f'/tickets/reserve/{ticket_id}')
    reserved_ticket = reserved_ticket_response.json()
    assert reserved_ticket_response.is_success
    assert reserved_ticket['id'] == ticket_id
    assert reserved_ticket['is_reserved'] is True


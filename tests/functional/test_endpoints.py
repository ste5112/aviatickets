import threading
from collections import Counter

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


@pytest_asyncio.fixture
async def unreserved_ticket(client):
    async with client.app.container._session_factory().begin() as session:
        return (await session.exec(select(TicketDB).where(TicketDB.is_reserved == False))).first()


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


def test_reserve_ticket(client, unreserved_ticket):
    ticket_id = unreserved_ticket.id
    reserved_ticket_response = client.post(f'/tickets/reserve/{ticket_id}')
    reserved_ticket = reserved_ticket_response.json()
    assert reserved_ticket_response.is_success
    assert reserved_ticket['id'] == ticket_id
    assert reserved_ticket['is_reserved'] is True


def test_reserve_ticket_concurrently(client, unreserved_ticket):
    ticket_id = unreserved_ticket.id
    threads_count = 10
    results = [None] * threads_count

    def func(path, results_list, thread_number):
        results_list[thread_number] = client.post(path).status_code

    threads = []

    for i in range(threads_count):
        thread = threading.Thread(target=func, args=(f'/tickets/reserve/{ticket_id}/', results, i))
        thread.start()
        threads.append(thread)

    for thr in threads:
        thr.join()

    counted_results = Counter(results)
    assert counted_results[200] == 1
    assert counted_results[409] == 9



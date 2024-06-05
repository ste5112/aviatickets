import datetime
import os

from faker import Faker

from tickets.models.ticket import TicketDB


def _tickets_gen(from_, to_, time, race_id, airline, count, gen_price):
    for _ in range(count):
        yield TicketDB(
            departure_point=from_,
            destination_point=to_,
            departure_time=time,
            race_id=race_id,
            airline=airline,
            price=gen_price(),  # in cents
            is_reserved=False
        )


def races_gen(
        *,
        points_count=20,
        max_departure_time=datetime.datetime.now() + datetime.timedelta(days=7),
        min_departure_time=datetime.datetime.now() - datetime.timedelta(days=1),
        min_tickets_per_race=25,
        max_tickets_per_race=125,
        races_number=None
):
    points = set()
    fake = Faker()
    try:
        seed = int(os.getenv("TEST_DATA_RANDOM_SEED"))
        Faker.seed(seed)
    except TypeError:
        pass

    counter = 0
    while True:
        points.add(fake.city())
        if len(points) >= points_count:
            break
    airlines = [fake.company() for _ in range(points_count // 10 + 1)]
    used_race_ids = set()
    while True:
        if races_number and counter > races_number:
            return
        addr1 = fake.random_choices(list(points), 1)[0]
        addr2 = fake.random_choices(list(points), 1)[0]

        if addr1 == addr2:
            continue
        race_id = f"{''.join(fake.random_letters(2)).upper()} {fake.random_int(1000, 9999)}"
        if race_id in used_race_ids:
            continue
        used_race_ids.add(race_id)
        try:
            yield from _tickets_gen(
                addr1,
                addr2,
                fake.date_time_between(min_departure_time, max_departure_time),
                race_id,
                fake.random_choices(airlines, 1)[0],
                fake.random_int(min_tickets_per_race, max_tickets_per_race),
                lambda: fake.random_int(10000, 5000000)
            )
            counter += 1
        except StopIteration:
            continue

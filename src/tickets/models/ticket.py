from datetime import datetime

from sqlmodel import Field
from tickets.models.base import BaseDBModel


class TicketDB(BaseDBModel, table=True):
    __tablename__ = "tickets"

    id: int | None = Field(default=None, primary_key=True)
    departure_point: str
    destination_point: str
    departure_time: datetime
    race_id: str
    airline: str
    price: int
    is_reserved: bool = False

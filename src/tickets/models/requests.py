from datetime import datetime

from pydantic import BaseModel


class TicketsRequest(BaseModel):
    departure_point: str
    destination_point: str
    departure_datetime: datetime
    window_size_seconds: int

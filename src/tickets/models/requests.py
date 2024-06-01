from datetime import datetime

from pydantic import BaseModel, Field


class TicketsRequest(BaseModel):
    departure_point: str
    destination_point: str
    departure_time: datetime

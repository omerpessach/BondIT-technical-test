from pydantic import BaseModel
from datetime import datetime


class Flight(BaseModel):
    flight_id: str
    arrival: datetime
    departure: datetime

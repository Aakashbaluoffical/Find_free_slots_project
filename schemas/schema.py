from pydantic import BaseModel
from sqlalchemy.orm import relationship
from datetime import datetime


class AvailabilityRequest(BaseModel):
    user_ids: list[int]
    date_range: dict
    timezone: str
    
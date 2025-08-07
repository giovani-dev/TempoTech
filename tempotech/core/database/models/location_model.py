from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class LocationModel(SQLModel, table=True):
    id: None
    city_name: str = Field(alias="cityName")
    state_name: str = Field(alias="stateName", max_length=50)
    state: str
    country: str
    latitude: float
    longitude: float
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)

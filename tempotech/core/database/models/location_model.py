from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class LocationModel(SQLModel, table=True):
    __tablename__ = "Location"

    id: int = Field(default=None, primary_key=True)
    city_name: Optional[str] = Field(alias="cityName")
    state_name: str = Field(alias="stateName", max_length=50)
    state: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)

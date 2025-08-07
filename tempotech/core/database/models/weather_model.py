from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class WeatherModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    current_temperature: float = Field(alias="currentTemperature")
    feels_like_temperature: float = Field(alias="feelsLikeTemperature")
    min_temperature: int = Field(alias="minTemperature")
    max_temperature: int = Field(alias="maxTemperature")
    humidity: float = Field(alias="humidity")
    wind_speed: float = Field(alias="windSpeed")
    timestamp_utc: datetime = Field(alias="timestampUtc")
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)

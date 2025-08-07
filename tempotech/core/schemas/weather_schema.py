from datetime import datetime
from typing import Annotated, Literal, TypeAlias

from pydantic import AfterValidator, BaseModel, Field


def ensure_future_datetime(d: datetime) -> datetime:
    now = datetime.now()
    assert d > now
    return d


FutureDatetime: TypeAlias = Annotated[datetime, AfterValidator(ensure_future_datetime)]


class Temperature(BaseModel):
    current: float = Field(description="The current temperature in degrees Celsius.")
    feels_like: float = Field(
        description="The 'feels like' temperature in degrees Celsius.",
        alias="feelsLike",
    )
    min: float = Field(description="The minimum temperature in degrees Celsius.")
    max: float = Field(description="The maximum temperature in degrees Celsius.")
    unit: Literal["celsius"] = Field(description="The unit of temperature measurement.")


class Weather(BaseModel):
    city_name: str = Field(
        min_length=1,
        max_length=100,
        description="The name of the city.",
        alias="cityName",
    )
    country: Literal["BR"] = Field(description="The country code of the city.")
    temperature: Temperature = Field(description="The temperature data for the city.")
    humidity: int = Field(ge=0, le=100, description="The percentage of humidity.")
    wind_speed: float = Field(
        ge=0, description="The wind speed in meters per second.", alias="windSpeed"
    )
    timestamp_utc: FutureDatetime = Field(
        description="The UTC timestamp of when the weather data was retrieved.",
        alias="timestampUtc",
    )

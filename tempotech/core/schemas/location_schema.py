from typing import Literal, Optional

from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    latitude: float = Field(description="The geographical latitude of the city.")
    longitude: float = Field(description="The geographical longitude of the city.")


class Location(BaseModel):
    country: Literal["BR"]
    state: str
    state_name: str = Field(alias="stateName")
    city_name: Optional[str] = Field(alias="cityName")
    coordinates: Optional[Coordinates] = Field(
        description="The geographical coordinates of the city."
    )

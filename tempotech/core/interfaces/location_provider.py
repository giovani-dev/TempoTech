from abc import ABC, abstractmethod
from typing import AsyncGenerator

from tempotech.core.schemas.location_schema import Location


class ILocationProvider(ABC):
    country: str

    @abstractmethod
    async def list_states(self) -> AsyncGenerator[Location, None]:
        pass

    @abstractmethod
    async def list_cities_by_state(self, state: str) -> AsyncGenerator[Location, None]:
        pass

    @abstractmethod
    async def get_coordinates(self, location: Location) -> Location:
        pass

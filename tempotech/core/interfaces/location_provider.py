from abc import ABC, abstractmethod
from typing import AsyncGenerator, Literal, Optional

from tempotech.core.schemas.location_schema import Coordinates, Location
from tempotech.core.schemas.pagination_schema import Pagination


# TODO: QUal é o jeito correto de tipar um metodo asyncrono?
class ILocationProvider(ABC):

    @abstractmethod
    async def list_states(self) -> AsyncGenerator[Location]:
        pass

    @abstractmethod
    async def list_cities_by_state(self, state: str) -> Pagination[Location]:
        pass

    @abstractmethod
    async def get_coordinates(self, location: Location) -> Location:
        pass

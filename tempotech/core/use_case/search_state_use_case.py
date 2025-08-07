from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.interfaces.weather_provider import IWeatherProvider
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination


class SearchState(IUseCase[Pagination[Location]]):
    def __init__(self, location: ILocationProvider):
        self._location = location
        # self._database = 

    async def execute(self) -> Pagination[Location]:
        # TODO: validar se os estados de um pais estão cadastrados no banco
        self._location.country
        states = await self._location.list_states()
        async for state in states:
            pass

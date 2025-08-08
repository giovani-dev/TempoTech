from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location


class SearchState(IUseCase[list[Location]]):
    def __init__(
        self,
        location_provider: ILocationProvider,
    ):
        self._location_provider = location_provider

    async def execute(self) -> list[Location]:
        return [item async for item in self._location_provider.list_states()]

from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location


class CreateLocationUseCase(IUseCase[None]):

    def __init__(
        self,
        location_db: IDefaultRepository[Location],
        location_provider: ILocationProvider,
    ):
        self._location_db = location_db
        self._location_provider = location_provider

    async def execute(self) -> None:
        provider_data = self._location_provider.list_states()
        async for state in provider_data:
            local_data = await self._location_db.search(
                filters={
                    "country": self._location_provider.country,
                    "state": state.state,
                    "state_name": state.state_name,
                },
                limit=1,
            )
            if len(list(local_data)) == 0:
                async for city in self._location_provider.list_cities_by_state(
                    state.state
                ):
                    await self._location_db.create(city)

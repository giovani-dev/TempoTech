from typing import AsyncGenerator, Literal, Optional

import aiohttp

from tempotech.core import config
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.schemas.location_schema import Coordinates, Location
from tempotech.core.schemas.pagination_schema import Pagination


class IBGEProvider(ILocationProvider):
    IBGE_ESTATE_LOCATION = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    IBGE_CITY_LOCATION = (
        "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios"
    )

    def __init__(self):
        self.country = "BR"

    async def list_states(self) -> AsyncGenerator[Location]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.IBGE_ESTATE_LOCATION) as response:
                response.raise_for_status()
                data = await response.json()
        for item in data:
            yield Location(
                country="BR",
                state_name=item["nome"],
                state=item["sigla"],
                city_name=None,
                coordinates=None,
            )

    async def list_cities_by_state(self, state: str) -> AsyncGenerator[Location]:
        url = self.IBGE_ESTATE_LOCATION.replace("{UF}", state)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

        for item in data:
            yield Location(
                country="BR",
                state_name=item["microrregiao"]["mesorregiao"]["UF"]["nome"],
                state=item["microrregiao"]["mesorregiao"]["UF"]["sigla"],
                city_name=item["nome"],
                coordinates=None,
            )

    async def get_coordinates(self, location: Location) -> Location:
        raise NotImplementedError

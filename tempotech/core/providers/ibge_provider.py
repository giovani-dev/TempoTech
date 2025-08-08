from typing import AsyncGenerator

import aiohttp

from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.schemas.location_schema import Location


class IBGEProvider(ILocationProvider):
    IBGE_ESTATE_LOCATION = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    IBGE_CITY_LOCATION = (
        "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios"
    )

    def __init__(self):
        self.country = "BR"

    async def list_states(self) -> AsyncGenerator[Location, None]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.IBGE_ESTATE_LOCATION) as response:
                response.raise_for_status()
                data = await response.json()
        for item in data:
            yield Location(
                **{
                    "country": "BR",
                    "stateName": item["nome"],
                    "state": item["sigla"],
                    "cityName": None,
                    "coordinates": None,
                }
            )

    async def list_cities_by_state(self, state: str) -> AsyncGenerator[Location, None]:
        url = self.IBGE_CITY_LOCATION.replace("{UF}", state)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()

        for item in data:
            state = (
                item.get("microrregiao", {})
                .get("mesorregiao", {})
                .get("UF", {})
                .get("sigla")
            )
            state_name = (
                item.get("microrregiao", {})
                .get("mesorregiao", {})
                .get("UF", {})
                .get("nome")
            )
            if state and state_name:
                yield Location(
                    **{
                        "country": "BR",
                        "stateName": item["microrregiao"]["mesorregiao"]["UF"]["nome"],
                        "state": item["microrregiao"]["mesorregiao"]["UF"]["sigla"],
                        "cityName": item["nome"],
                        "coordinates": None,
                    }
                )

    async def get_coordinates(self, location: Location) -> Location:
        raise NotImplementedError

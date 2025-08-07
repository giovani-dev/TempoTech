from typing import AsyncGenerator

import aiohttp

from tempotech.core import config
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.schemas.location_schema import Coordinates, Location
from tempotech.core.schemas.pagination_schema import Pagination


class OpenWeatherProvider(ILocationProvider):
    GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={API_key}"

    async def list_states(self) -> AsyncGenerator[Location]:
        raise NotImplementedError

    async def list_cities_by_state(self, state: str) -> Pagination[Location]:
        raise NotImplementedError

    async def get_coordinates(self, location: Location) -> Location:
        url = (
            self.GEOCODING_URL.replace("{city_name}", location.city_name)
            .replace("{state_code}", location.state)
            .replace("{country_code}", location.country)
            .replace("{limit}", 1)
            .replace("{API_key}", config.OPEN_WEATHER_API_KEY)
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
        location.coordinates = Coordinates(
            latitude=data["lat"],
            longitude=data["lon"],
        )

"""
Módulo do provedor de clima e geocodificação OpenWeather.

Este provedor implementa a interface `ILocationProvider` para buscar
coordenadas geográficas a partir da API de geocodificação do OpenWeatherMap.
Ele é o provedor de coordenadas do projeto.
"""

from typing import AsyncGenerator

import aiohttp

from tempotech.core import config
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.schemas.location_schema import Coordinates, Location
from tempotech.core.schemas.pagination_schema import Pagination


class OpenWeatherProvider(ILocationProvider):
    """
    Provedor de localização que utiliza a API de geocodificação do OpenWeather.

    Fornece a funcionalidade de buscar coordenadas geográficas para uma
    localização específica.
    """

    GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&limit={limit}&appid={API_key}"

    def __init__(self):
        """
        Inicializa o provedor do OpenWeather e define o país padrão.
        """
        self.country = "BR"

    async def list_states(self) -> AsyncGenerator[Location, None]:
        """
        Lista de estados não implementada.

        Este provedor não fornece uma lista de estados, pois sua função
        principal é a geocodificação.
        """
        raise NotImplementedError

    async def list_cities_by_state(self, state: str) -> AsyncGenerator[Location, None]:
        """
        Lista de cidades por estado não implementada.

        Este provedor não lista cidades por estado, pois sua função principal
        é a geocodificação.
        """
        raise NotImplementedError

    async def get_coordinates(self, location: Location) -> Location:
        """
        Obtém as coordenadas de uma cidade usando a API de geocodificação do OpenWeather.

        Args:
            location (Location): Um objeto Location com `city_name`, `state` e `country`.

        Returns:
            Location: O objeto Location atualizado com as coordenadas de latitude e longitude.
        """
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

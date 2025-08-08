"""
Módulo do provedor de localização do IBGE.

Este provedor implementa a interface `ILocationProvider` para buscar
dados de localização (estados e cidades) do Brasil a partir da API do IBGE.
Ele utiliza requisições HTTP assíncronas para buscar as informações.
"""
from typing import AsyncGenerator

import aiohttp

from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.schemas.location_schema import Location


class IBGEProvider(ILocationProvider):
    """
    Provedor de localização para o Brasil, usando a API do IBGE.

    Fornece métodos para listar estados e cidades. A propriedade `country`
    é definida como "BR" para indicar que este provedor é específico para o Brasil.
    """
    IBGE_ESTATE_LOCATION = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    IBGE_CITY_LOCATION = (
        "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios"
    )

    def __init__(self):
        """
        Inicializa o provedor do IBGE e define o país.
        """
        self.country = "BR"

    async def list_states(self) -> AsyncGenerator[Location, None]:
        """
        Lista todos os estados do Brasil a partir da API do IBGE.

        Retorna um gerador assíncrono de objetos Location, onde cada um
        representa um estado.

        Returns:
            AsyncGenerator[Location, None]: Gerador de objetos Location para cada estado.
        """
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
        """
        Lista todas as cidades de um estado específico do Brasil.

        Busca os municípios a partir da API do IBGE, usando a sigla do estado.

        Args:
            state (str): A sigla do estado (ex: "SC").

        Returns:
            AsyncGenerator[Location, None]: Gerador de objetos Location para cada cidade do estado.
        """
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
        """
        Obtém as coordenadas geográficas para uma localização.

        Esta função não é implementada no IBGE Provider, pois a API do IBGE
        não fornece coordenadas geográficas, apenas nomes e códigos.
        """
        raise NotImplementedError
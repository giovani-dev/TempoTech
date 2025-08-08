"""
Módulo de interfaces para provedores de dados de localização.

Define os contratos para provedores de dados que fornecem informações geográficas,
como listas de estados e cidades, e coordenadas. A interface permite que
a lógica de negócios seja independente de uma fonte de dados de localização
específica (ex: IBGE, OpenWeather).
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator

from tempotech.core.schemas.location_schema import Location


class ILocationProvider(ABC):
    """
    Interface para provedores de dados de localização.

    Esta classe abstrata define os métodos que qualquer provedor de localização
    deve implementar, garantindo consistência e intercambiabilidade.
    """

    country: str
    """
    O código do país para o qual o provedor de localização é configurado.
    """

    @abstractmethod
    async def list_states(self) -> AsyncGenerator[Location, None]:
        """
        Método abstrato para listar todos os estados.

        A implementação deve retornar um gerador assíncrono que itera sobre
        os estados disponíveis.

        Returns:
            AsyncGenerator[Location, None]: Um gerador assíncrono de objetos Location, um para cada estado.
        """
        pass

    @abstractmethod
    async def list_cities_by_state(self, state: str) -> AsyncGenerator[Location, None]:
        """
        Método abstrato para listar todas as cidades de um estado específico.

        Args:
            state (str): O código ou nome do estado a ser consultado.

        Returns:
            AsyncGenerator[Location, None]: Um gerador assíncrono de objetos Location, um para cada cidade.
        """
        pass

    @abstractmethod
    async def get_coordinates(self, location: Location) -> Location:
        """
        Método abstrato para obter as coordenadas geográficas de uma localização.

        Args:
            location (Location): O objeto Location contendo as informações da cidade.

        Returns:
            Location: O objeto Location atualizado com as coordenadas.
        """
        pass

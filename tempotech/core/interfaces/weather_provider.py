"""
Módulo de interfaces para provedores de dados de clima.

Este módulo define o contrato para provedores de dados que fornecem
informações meteorológicas. A interface permite que a lógica de negócios
seja independente de uma fonte de dados de clima específica (ex: OpenWeatherMap).
"""

from abc import ABC, abstractmethod

from tempotech.core.schemas.weather_schema import Weather


class IWeatherProvider(ABC):
    """
    Interface para provedores de dados de clima.

    Esta classe abstrata define os métodos que qualquer provedor de clima
    deve implementar para buscar dados meteorológicos.
    """

    @abstractmethod
    async def get_current_weather(self, location: str) -> Weather:
        """
        Método abstrato para obter o clima atual de uma localização.

        Args:
            location (str): O nome da cidade ou outra identificação de localização.

        Returns:
            Weather: Um objeto contendo os dados de clima atuais.
        """
        pass

"""
Módulo de inicialização dos provedores de dados.

Este módulo configura e inicializa as instâncias dos provedores de dados
externos (como IBGE e OpenWeather) com base nas configurações da aplicação.
Isso permite que a aplicação utilize o provedor de país e de coordenadas
apropriado de forma centralizada.
"""

from tempotech.core import config
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.providers.ibge_provider import IBGEProvider
from tempotech.core.providers.open_weather_provider import OpenWeatherProvider

coutry_provider: ILocationProvider
coordinate_provider = OpenWeatherProvider()

if config.COUNTRY == "BR":
    coutry_provider = IBGEProvider()

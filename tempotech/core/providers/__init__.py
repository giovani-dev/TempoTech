from tempotech.core import config
from tempotech.core.interfaces.location_provider import ILocationProvider
from tempotech.core.providers.ibge_provider import IBGEProvider
from tempotech.core.providers.open_weather_provider import OpenWeatherProvider

coutry_provider: ILocationProvider
coordinate_provider = OpenWeatherProvider()

if config.COUNTRY == "BR":
    coutry_provider = IBGEProvider()

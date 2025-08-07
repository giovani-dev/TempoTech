from abc import ABC, abstractmethod

from tempotech.core.schemas.weather_schema import Weather


class IWeatherProvider(ABC):
    @abstractmethod
    async def get_current_weather(self, location: str) -> Weather:
        pass

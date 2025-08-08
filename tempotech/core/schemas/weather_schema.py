"""
Módulo de esquemas de dados para clima.

Define os modelos de dados Pydantic para representar informações de clima,
como temperatura e dados meteorológicos completos. Esses esquemas são
usados para validação de dados e para tipagem das respostas da API.
"""

from datetime import datetime
from typing import Annotated, Literal, TypeAlias

from pydantic import AfterValidator, BaseModel, Field


def ensure_future_datetime(d: datetime) -> datetime:
    """
    Função de validação para garantir que um datetime está no futuro.

    Esta função é usada como um `AfterValidator` para assegurar que o
    timestamp de recuperação dos dados de clima seja sempre posterior ao
    momento da validação.

    Args:
        d (datetime): O objeto datetime a ser validado.

    Returns:
        datetime: O mesmo objeto datetime se a validação for bem-sucedida.

    Raises:
        AssertionError: Se o datetime não for futuro.
    """
    now = datetime.now()
    assert d > now
    return d


FutureDatetime: TypeAlias = Annotated[datetime, AfterValidator(ensure_future_datetime)]
"""
Type alias para um campo de datetime que deve ser no futuro.

Utiliza `Annotated` e `AfterValidator` para aplicar a validação
`ensure_future_datetime` automaticamente.
"""


class Temperature(BaseModel):
    """
    Esquema de dados para informações de temperatura.

    Representa as temperaturas atual, "sensação térmica", mínima e máxima,
    juntamente com a unidade de medida (Celsius).
    """

    current: float = Field(description="The current temperature in degrees Celsius.")
    feels_like: float = Field(
        description="The 'feels like' temperature in degrees Celsius.",
        alias="feelsLike",
    )
    min: float = Field(description="The minimum temperature in degrees Celsius.")
    max: float = Field(description="The maximum temperature in degrees Celsius.")
    unit: Literal["celsius"] = Field(description="The unit of temperature measurement.")


class Weather(BaseModel):
    """
    Esquema de dados para informações completas de clima.

    Representa um conjunto de dados meteorológicos para uma cidade específica,
    incluindo nome da cidade, país, dados de temperatura, umidade, velocidade
    do vento e um timestamp de recuperação.
    """

    city_name: str = Field(
        min_length=1,
        max_length=100,
        description="The name of the city.",
        alias="cityName",
    )
    country: Literal["BR"] = Field(description="The country code of the city.")
    temperature: Temperature = Field(description="The temperature data for the city.")
    humidity: int = Field(ge=0, le=100, description="The percentage of humidity.")
    wind_speed: float = Field(
        ge=0, description="The wind speed in meters per second.", alias="windSpeed"
    )
    timestamp_utc: FutureDatetime = Field(
        description="The UTC timestamp of when the weather data was retrieved.",
        alias="timestampUtc",
    )

"""
Módulo de modelo de dados para o clima.

Define a estrutura da tabela `Weather` no banco de dados usando o SQLModel.
Este modelo é projetado para armazenar informações de clima, como
temperatura, umidade e velocidade do vento, para futuras consultas.
"""
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class WeatherModel(SQLModel, table=True):
    """
    Modelo de dados para a tabela "Weather".

    Esta classe mapeia as informações de clima para a tabela correspondente
    no banco de dados, incluindo detalhes como a temperatura atual,
    data de criação e atualização.
    """
    __tablename__ = "Weather"

    id: int = Field(default=None, primary_key=True)
    current_temperature: float = Field(alias="currentTemperature")
    feels_like_temperature: float = Field(alias="feelsLikeTemperature")
    min_temperature: int = Field(alias="minTemperature")
    max_temperature: int = Field(alias="maxTemperature")
    humidity: float = Field(alias="humidity")
    wind_speed: float = Field(alias="windSpeed")
    timestamp_utc: datetime = Field(alias="timestampUtc")
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)
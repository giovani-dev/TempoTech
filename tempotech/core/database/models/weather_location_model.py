"""
Módulo de modelo de dados para a tabela de relacionamento entre clima e localização.

Define a estrutura da tabela `WeatherLocation`, que é uma tabela de associação
muitos-para-muitos entre as tabelas `Weather` e `Location`.
"""

from sqlmodel import Field, SQLModel


class WeatherLocationModel(SQLModel, table=True):
    """
    Modelo de dados para a tabela de associação "WeatherLocation".

    Esta classe mapeia a tabela de relacionamento que liga um registro de
    clima a um registro de localização.
    """

    __tablename__ = "WeatherLocation"

    weather_id: int = Field(alias="id_Weather")
    location_id: int = Field(alias="id_Location")

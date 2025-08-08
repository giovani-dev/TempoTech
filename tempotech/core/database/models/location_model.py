"""
Módulo de modelo de dados para localização.

Define a estrutura da tabela `Location` no banco de dados usando o SQLModel.
Este modelo representa cidades e estados, incluindo seus nomes, códigos e
coordenadas geográficas.
"""

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class LocationModel(SQLModel, table=True):
    """
    Modelo de dados para a tabela "Location".

    Esta classe mapeia os dados de localização para a tabela correspondente
    no banco de dados, facilitando a interação com o ORM.
    """

    __tablename__ = "Location"

    id: int = Field(default=None, primary_key=True)
    city_name: Optional[str] = Field(alias="cityName")
    state_name: str = Field(alias="stateName", max_length=50)
    state: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime = Field(alias="createdAt", default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(alias="updatedAt", default=None)

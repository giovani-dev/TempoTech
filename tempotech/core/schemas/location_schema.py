"""
Módulo de esquemas de dados para localização.

Define os modelos de dados Pydantic para representar informações de localização,
como coordenadas, estados e cidades. Esses esquemas são usados para validação
de dados e para garantir a consistência das informações em toda a aplicação.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """
    Esquema de dados para coordenadas geográficas.

    Representa a latitude e a longitude de uma localização, sendo
    ambos campos opcionais, pois nem sempre estarão disponíveis
    ao buscar uma localização.
    """

    latitude: Optional[float] = Field(
        description="The geographical latitude of the city.", default=None
    )
    longitude: Optional[float] = Field(
        description="The geographical longitude of the city.", default=None
    )


class Location(BaseModel):
    """
    Esquema de dados para informações de localização.

    Representa uma localização, que pode ser uma cidade ou um estado,
    incluindo o país, o estado, o nome do estado, o nome da cidade e
    as coordenadas.
    """

    country: Literal["BR"]
    state: str
    state_name: str = Field(alias="stateName")
    city_name: Optional[str] = Field(alias="cityName", default=None)
    coordinates: Optional[Coordinates] = Field(
        description="The geographical coordinates of the city.", default=None
    )

"""
Módulo de injeção de dependência para os casos de uso.

Este módulo lida com a injeção de dependências dos casos de uso, que encapsulam
a lógica de negócios da aplicação. As funções aqui definidas criam e retornam
instâncias de casos de uso, injetando as dependências necessárias, como
repositórios de banco de dados e provedores de dados externos.
"""

from typing import Annotated, Literal, Optional

from fastapi import Depends

from tempotech.api.deps.database import LocationDbRepository
from tempotech.api.deps.provider import CountryProvider
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination
from tempotech.core.use_case.search_city_use_case import SearchCity
from tempotech.core.use_case.search_state_use_case import SearchState


def get_search_state(location_provider: CountryProvider):
    """
    Função de injeção de dependência para o caso de uso `SearchState`.

    Esta função cria e retorna uma instância de `SearchState`, injetando o
    provedor de localização do país.

    Args:
        location_provider (CountryProvider): O provedor de localização injetado.

    Returns:
        SearchState: Uma instância do caso de uso `SearchState`.
    """
    return SearchState(location_provider=location_provider)


def get_search_city(
    location_db: LocationDbRepository,
    state: str,
    order_by: Optional[Literal["state_name", "city_name"]] = None,
    search_by: Optional[Literal["country", "state", "state_name", "city_name"]] = None,
    search_value: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    """
    Função de injeção de dependência para o caso de uso `SearchCity`.

    Esta função constrói e retorna uma instância de `SearchCity`,
    passando o repositório de banco de dados e os parâmetros da requisição
    para o caso de uso.

    Args:
        location_db (LocationDbRepository): O repositório de localização injetado.
        state (str): A abreviação do estado a ser buscado.
        order_by (Optional[Literal["state_name", "city_name"]]): Coluna para ordenação.
        search_by (Optional[Literal["country", "state", "state_name", "city_name"]]): Coluna para busca.
        search_value (Optional[str]): Valor a ser buscado.
        page (int): O número da página.
        page_size (int): O número de itens por página.

    Returns:
        SearchCity: Uma instância do caso de uso `SearchCity`.
    """
    return SearchCity(
        location_db=location_db,
        state=state,
        order_by=order_by,
        search_by=search_by,
        search_value=search_value,
        page=page,
        page_size=page_size,
    )


SearchStateUseCase = Annotated[IUseCase[list[Location]], Depends(get_search_state)]
"""
Type alias para injeção do caso de uso de busca de estados.

Quando injetado em um endpoint, o FastAPI resolve a dependência
chamando `get_search_state`.
"""


SearchCityUseCase = Annotated[IUseCase[Pagination[Location]], Depends(get_search_city)]
"""
Type alias para injeção do caso de uso de busca de cidades.

Quando injetado em um endpoint, o FastAPI resolve a dependência
chamando `get_search_city`.
"""

"""
Módulo de roteamento para os endpoints de localização.

Este módulo define as rotas da API para buscar informações de localização, como
estados e cidades. As funcionalidades aqui implementadas se comunicam com o
provedor de localização do IBGE e com o banco de dados interno para
recuperar e gerenciar dados geográficos.
"""

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi_limiter.depends import RateLimiter

from tempotech.api.deps.use_case import SearchCityUseCase, SearchStateUseCase
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination

router = APIRouter(tags=["Location"])


@router.get("/state", dependencies=[Depends(RateLimiter(times=1, seconds=10))])
@cache(expire=600)
async def get_states(use_case: SearchStateUseCase) -> list[Location]:
    """
    Retorna uma lista de todos os estados brasileiros.

    Este endpoint busca os estados a partir da IBGE Provider. Para evitar sobrecarga no sistema,
    ele é limitado a 1 requisição a cada 10 segundos por cliente.
    O resultado da busca é armazenado em cache por 10 minutos para consultas subsequentes.

    Returns:
        list[Location]: Uma lista de objetos Location, onde cada um representa um estado do Brasil.
    """
    return await use_case.execute()


@router.get("/{state}/cities", dependencies=[Depends(RateLimiter(times=1, seconds=10))])
@cache(expire=600)
async def get_cities_from_state(use_case: SearchCityUseCase) -> Pagination[Location]:
    """
    Retorna uma lista paginada de todas as cidades de um estado específico.

    Este endpoint recupera as cidades de um estado usando a IBGE Provider. A
    resposta é paginada para facilitar o manuseio de grandes volumes de dados. A
    rota também possui um limite de 1 requisição a cada 10 segundos e cache de 10 minutos.

    Args:
        state (str): A abreviação do nome do estado (ex: "SC").

    Returns:
        Pagination[Location]: Um objeto paginado com a lista de cidades do estado.
    """
    return await use_case.execute()

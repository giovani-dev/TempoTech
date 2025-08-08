"""
Módulo do caso de uso para buscar cidades.

Este módulo define a lógica de negócio para buscar cidades em um estado
específico, com suporte a ordenação e paginação. Ele encapsula a orquestração
entre o repositório de banco de dados e a resposta da aplicação.
"""

from typing import Literal, Optional

from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination


class SearchCity(IUseCase[Pagination[Location]]):
    """
    Caso de uso para buscar e retornar uma lista paginada de cidades.

    Lida com a lógica de busca no banco de dados, aplicando filtros,
    ordenação e paginação com base nos parâmetros fornecidos.
    """

    def __init__(
        self,
        location_db: IDefaultRepository[Location],
        state: str,
        order_by: Optional[Literal["state_name", "city_name"]] = None,
        search_by: Optional[Literal["city_name"]] = None,
        search_value: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
    ):
        """
        Inicializa o caso de uso com o repositório e os parâmetros de busca.

        Args:
            location_db (IDefaultRepository[Location]): O repositório de banco de dados para a busca.
            state (str): A abreviação do estado a ser pesquisado.
            order_by (Optional[Literal["state_name", "city_name"]]): Critério de ordenação.
            search_by (Optional[Literal["city_name"]]): Campo para a busca.
            search_value (Optional[str]): Valor a ser buscado no campo especificado.
            page (int): O número da página atual.
            page_size (int): O número de itens por página.
        """
        self._location_db = location_db
        self._state = state
        self._order_by = order_by
        self._search_by = search_by
        self._search_value = search_value
        self._page = page
        self._page_size = page_size

    async def execute(self) -> Pagination[Location]:
        """
        Executa a busca de cidades no banco de dados e retorna os resultados paginados.

        Monta os parâmetros para a consulta ao banco de dados e formata o resultado
        em um objeto `Pagination`.

        Returns:
            Pagination[Location]: Um objeto de paginação contendo a lista de cidades e os metadados.
        """
        params = {"filters": {"state": self._state}}
        if self._search_by and self._search_value:
            params["filters"][self._search_by] = self._search_value
        if self._order_by:
            params["order_by"] = self._order_by
        if self._page:
            params["offset"] = (self._page - 1) * self._page_size
            params["limit"] = self._page_size
        query = await self._location_db.search(**params)
        return Pagination(
            **{
                "actualPage": self._page,
                "nextPage": (
                    self._page + 1 if len(query) == self._page_size else self._page
                ),
                "previusPage": self._page - 1 if self._page >= 1 else 0,
                "itemsCount": len(query),
                "items": query,
            }
        )

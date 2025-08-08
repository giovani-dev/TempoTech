from typing import Literal, Optional

from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination


class SearchState(IUseCase[Pagination[Location]]):
    # TODO: Adicionar um validador para os parametros!!!
    # TODO: Criar um filtro por coordenadas
    def __init__(
        self,
        location_db: IDefaultRepository,
        order_by: Optional[Literal["state_name", "city_name"]],
        search_by: Optional[Literal["country", "state", "state_name", "city_name"]],
        search_value: Optional[str],
        page: int,
        page_size: int,
    ):
        self._location_db = location_db
        self._order_by = order_by
        self._search_by = search_by
        self._search_value = search_value
        self._page = page
        self._page_size = page_size

    async def execute(self) -> Pagination[Location]:
        params = {}
        if self._search_by and self._search_value:
            params[self._search_by] = self._search_value
        if self._order_by:
            params["order_by"] = self._order_by
        if self._page:
            params["page"] = self._page
        self._location_db.search(**params)
        return Pagination(
            total=0,
            actual_page=1,
            next_page=2,
            previus_page=1,
            items_count=10,
            items=[],
        )

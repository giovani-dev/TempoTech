from typing import Literal, Optional

from tempotech.core.interfaces.database_repository import IDefaultRepository
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination


class SearchCity(IUseCase[Pagination[Location]]):

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
        self._location_db = location_db
        self._state = state
        self._order_by = order_by
        self._search_by = search_by
        self._search_value = search_value
        self._page = page
        self._page_size = page_size

    async def execute(self) -> Pagination[Location]:
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

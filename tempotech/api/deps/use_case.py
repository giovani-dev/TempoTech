from typing import Annotated, Literal, Optional

from fastapi import Depends

from tempotech.api.deps.database import LocationDbRepository
from tempotech.api.deps.provider import CountryProvider
from tempotech.core.interfaces.use_case import IUseCase
from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination
from tempotech.core.use_case.search_state_use_case import SearchState


def get_search_state(location_provider: CountryProvider):
    return SearchState(location_provider=location_provider)


def get_search_city(
    location_provider: CountryProvider,
    order_by: Optional[Literal["state_name", "city_name"]] = None,
    search_by: Optional[Literal["country", "state", "state_name", "city_name"]] = None,
    search_value: Optional[str] = None,
    page: int = 1,
    page_size: int = 10,
):
    return dict(
        location_db=location_db,
        location_provider=location_provider,
        order_by=order_by,
        search_by=search_by,
        search_value=search_value,
        page=page,
        page_size=page_size,
    )


SearchStateUseCase = Annotated[IUseCase[list[Location]], Depends(get_search_state)]

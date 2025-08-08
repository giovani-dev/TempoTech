from typing import Literal, Optional

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from tempotech.core.schemas.location_schema import Location
from tempotech.core.schemas.pagination_schema import Pagination

router = APIRouter(tags=["Location"])


@router.get("/state")
@cache(expire=600)
async def get_states(
    order_by: Optional[Literal["state_name", "city_name"]],
    search_by: Optional[Literal["country", "state", "state_name", "city_name"]],
    search_value: Optional[str],
    page: int = 1,
    page_size: int = 10,
) -> Pagination[Location]:
    """
    Returns a list of all states.

    This route doesn't require any input parameters.
    """
    pass


@router.get("/{state_name}/cities")
@cache(expire=600)
async def get_cities_from_state(
    state: str,
    order_by: Optional[Literal["city_name"]],
    search_by: Optional[Literal["city_name"]],
    search_value: Optional[str],
    page: int = 1,
    page_size: int = 10,
) -> Pagination[Location]:
    """
    Returns a list of all cities in a specific state.

    - **state_name**: The name of the state (e.g., "santa-catarina").
    """
    pass

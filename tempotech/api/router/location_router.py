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
    Returns a list of all states.

    This route doesn't require any input parameters.
    """
    return await use_case.execute()


@router.get("/{state}/cities", dependencies=[Depends(RateLimiter(times=1, seconds=10))])
@cache(expire=600)
async def get_cities_from_state(use_case: SearchCityUseCase) -> Pagination[Location]:
    """
    Returns a list of all cities in a specific state.

    - **state**: The abreviation name of the state (e.g., "SC").
    """
    return await use_case.execute()

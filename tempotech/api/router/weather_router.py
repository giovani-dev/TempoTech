from typing import Optional

from fastapi import APIRouter, Request
from fastapi_cache.decorator import cache

from tempotech.core.schemas.pagination_schema import Pagination
from tempotech.core.schemas.weather_schema import Weather

router = APIRouter(tags=["Weather"])


@router.get("/current/{city_name}")
@cache(expire=600)
async def get_current_weather(city_name: str, request: Request) -> Weather:
    """
    Retrieves the current weather for a specified city.

    This endpoint provides up-to-date weather information. To ensure high performance,
    it uses a caching mechanism to quickly serve data that has been recently
    requested. Queries are also stored to provide a history of searches.
    """
    pass


@router.get("/history")
@cache(expire=600)
async def get_history(
    city_name: Optional[str] = None, state: Optional[str] = None
) -> list[Weather]:
    """
    Retrieves a paginated list of the most recent weather queries.

    This endpoint fetches the 10 most recent weather queries that were made,
    providing a chronological record of the API usage.
    """
    pass

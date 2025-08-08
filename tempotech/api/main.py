import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from redis import asyncio as aioredis

from tempotech.api.router import location_router, weather_router
from tempotech.core import config
from tempotech.core.database.repository.postgres.connection_repository import (
    ConnectionRepositoryV2,
)
from tempotech.core.database.repository.postgres.location_repository import (
    LocationRepository,
)
from tempotech.core.providers import coutry_provider
from tempotech.core.use_case.create_location_use_case import CreateLocationUseCase

API_VERSION = "v1"


async def setup_db():
    async with ConnectionRepositoryV2.connect() as session:
        await CreateLocationUseCase(
            location_db=LocationRepository(session), location_provider=coutry_provider
        ).execute()


@asynccontextmanager
async def lifesplan(app: FastAPI) -> AsyncIterator[None]:
    task = asyncio.create_task(setup_db())
    app.state.background_task = task

    redis = await aioredis.from_url(
        f"redis://{config.REDIS_HOST}:{config.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield
    await FastAPILimiter.close()


app = FastAPI(lifespan=lifesplan)
app.include_router(weather_router.router, prefix=f"/api/{API_VERSION}/weather")
app.include_router(location_router.router, prefix=f"/api/{API_VERSION}/location")


if __name__ == "__main__":
    uvicorn.run(app=app, port=8080)

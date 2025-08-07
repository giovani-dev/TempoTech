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

API_VERSION = "v1"


@asynccontextmanager
async def lifesplan(app: FastAPI) -> AsyncIterator[None]:
    # TODO: validar se os estados de um pais estão cadastrados no banco -> fazer no startup da aplicação
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

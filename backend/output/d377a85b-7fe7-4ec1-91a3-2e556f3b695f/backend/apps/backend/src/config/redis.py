"""Redis client singleton using aioredis."""
from functools import lru_cache

import redis.asyncio as aioredis
from redis.asyncio import Redis

from .env import settings


@lru_cache
def get_redis_client() -> Redis:
    """Cached Redis client singleton."""
    return aioredis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=20,
    )


redis_client: Redis = get_redis_client()

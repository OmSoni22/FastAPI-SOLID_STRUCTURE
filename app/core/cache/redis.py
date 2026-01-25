import redis.asyncio as redis
from app.core.config.settings import settings

redis_client = None

async def init_redis():
    global redis_client
    if settings.redis_enabled:
        redis_client = redis.from_url(settings.redis_url)

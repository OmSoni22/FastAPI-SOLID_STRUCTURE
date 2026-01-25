from app.core.cache.redis import redis_client

def cached(key_builder, ttl=60):
    def wrapper(func):
        async def inner(*args, **kwargs):
            if not redis_client:
                return await func(*args, **kwargs)

            key = key_builder(*args, **kwargs)
            cached_val = await redis_client.get(key)
            if cached_val:
                return cached_val

            result = await func(*args, **kwargs)
            await redis_client.set(key, result, ex=ttl)
            return result
        return inner
    return wrapper

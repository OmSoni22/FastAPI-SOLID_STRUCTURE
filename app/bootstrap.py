from app.core.cache.redis import init_redis

async def bootstrap():
    """
    Initialize application services on startup.
    
    Note: Database migrations are handled by Alembic.
    Run 'alembic upgrade head' to apply migrations.
    """
    await init_redis()

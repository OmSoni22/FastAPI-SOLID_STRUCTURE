from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.router import api_router
from app.api.health import router as health_router
from app.bootstrap import bootstrap
from app.core.logging.middleware import logging_middleware
from app.core.config.settings import settings
from app.core.config.env import validate_config
from app.core.exceptions.base import AppException
from app.core.exceptions.handlers import (
    app_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Production-grade FastAPI application with SOLID principles, MVC, and enterprise features",
    version="1.0.0",
    debug=settings.debug,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"]
)


# Register logging middleware
app.middleware("http")(logging_middleware)


# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# Startup event
@app.on_event("startup")
async def startup():
    """
    Application startup tasks:
    - Validate configuration
    - Initialize services (Redis, etc.)
    """
    # Validate environment configuration
    validate_config()
    
    # Bootstrap services
    await bootstrap()


# Shutdown event
@app.on_event("shutdown")
async def shutdown():
    """
    Application shutdown tasks:
    - Close connections
    - Cleanup resources
    """
    from app.core.cache.redis import redis_client
    if redis_client:
        await redis_client.close()


# Include routers
app.include_router(health_router, prefix="/api", tags=["Health"])
app.include_router(api_router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": "1.0.0",
        "docs": "/api/docs",
        "health": "/api/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )

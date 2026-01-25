from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.service_factory import ServiceFactory
from app.core.dependencies import get_service_factory
from .entity_schema import EntityCreate, EntityRead

router = APIRouter()


@router.post("/", response_model=EntityRead, status_code=201)
async def create_entity(
    payload: EntityCreate,
    factory: ServiceFactory = Depends(get_service_factory)
):
    """
    Create a new entity.
    
    - **name**: Entity name (required)
    - **description**: Entity description (optional)
    """
    return await factory.entity.create_entity(payload)


@router.get("/", response_model=List[EntityRead])
async def list_entities(factory: ServiceFactory = Depends(get_service_factory)):
    """
    List all entities.
    
    Returns a list of all entities in the database.
    """
    return await factory.entity.get_entities()

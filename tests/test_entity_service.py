"""
Unit tests for Entity service.

These tests verify the business logic in isolation.
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.entity.entity_model import Entity
from app.modules.entity.entity_schema import EntityCreate
from app.modules.entity.services.entity_service import EntityService


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_entity(test_db: AsyncSession, sample_entity_data: dict):
    """Test creating an entity."""
    # Arrange
    service = EntityService(test_db)
    payload = EntityCreate(**sample_entity_data)
    
    # Act
    result = await service.create_entity(payload)
    await test_db.commit()
    
    # Assert
    assert result is not None
    assert isinstance(result, Entity)
    assert result.name == sample_entity_data["name"]
    assert result.description == sample_entity_data["description"]
    assert result.id is not None


@pytest.mark.unit
@pytest.mark.asyncio
async def test_get_entities(test_db: AsyncSession, sample_entity_data: dict):
    """Test retrieving all entities."""
    # Arrange
    service = EntityService(test_db)
    
    # Create test entities
    entity1 = EntityCreate(**sample_entity_data)
    entity2 = EntityCreate(name="Another Entity", description="Another test entity")
    
    await service.create_entity(entity1)
    await service.create_entity(entity2)
    await test_db.commit()
    
    # Act
    results = await service.get_entities()
    
    # Assert
    assert len(results) == 2
    assert all(isinstance(e, Entity) for e in results)


@pytest.mark.unit
@pytest.mark.asyncio
async def test_create_entity_minimal(test_db: AsyncSession):
    """Test creating an entity with minimal data."""
    # Arrange
    service = EntityService(test_db)
    payload = EntityCreate(name="Minimal Entity")
    
    # Act
    result = await service.create_entity(payload)
    await test_db.commit()
    
    # Assert
    assert result.name == "Minimal Entity"
    assert result.description is None

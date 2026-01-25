from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class EntityBase(BaseModel):
    """Base entity schema with common fields."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the entity",
        examples=["My Entity"]
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional description of the entity",
        examples=["A detailed description of my entity"]
    )


class EntityCreate(EntityBase):
    """Schema for creating a new entity."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Sample Entity",
                    "description": "This is a sample entity for demonstration"
                }
            ]
        }
    )


class EntityRead(EntityBase):
    """Schema for reading an entity (includes ID)."""
    
    id: int = Field(..., description="Unique identifier")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Sample Entity",
                    "description": "This is a sample entity for demonstration"
                }
            ]
        }
    )

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    """Base user schema with common fields."""
    
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the user",
        examples=["My User"]
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional description of the user",
        examples=["A detailed description of my user"]
    )


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Sample User",
                    "description": "This is a sample user for demonstration"
                }
            ]
        }
    )


class UserRead(UserBase):
    """Schema for reading a user (includes ID)."""
    
    id: int = Field(..., description="Unique identifier")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "Sample User",
                    "description": "This is a sample user for demonstration"

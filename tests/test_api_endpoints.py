"""
Integration tests for Entity API endpoints.

These tests verify the full request/response cycle.
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration
def test_create_entity_endpoint(client: TestClient, sample_entity_data: dict):
    """Test POST /api/v1/entities endpoint."""
    # Act
    response = client.post("/api/v1/entities/", json=sample_entity_data)
    
    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_entity_data["name"]
    assert data["description"] == sample_entity_data["description"]
    assert "id" in data


@pytest.mark.integration
def test_list_entities_endpoint(client: TestClient, sample_entity_data: dict):
    """Test GET /api/v1/entities endpoint."""
    # Arrange - Create some entities first
    client.post("/api/v1/entities/", json=sample_entity_data)
    client.post("/api/v1/entities/", json={"name": "Another Entity"})
    
    # Act
    response = client.get("/api/v1/entities/")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.integration
def test_create_entity_validation_error(client: TestClient):
    """Test validation error for invalid entity data."""
    # Act - Missing required 'name' field
    response = client.post("/api/v1/entities/", json={"description": "No name"})
    
    # Assert
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"] is True


@pytest.mark.integration
def test_health_check(client: TestClient):
    """Test health check endpoint."""
    # Act
    response = client.get("/api/health")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


@pytest.mark.integration
def test_request_id_in_response(client: TestClient):
    """Test that request ID is included in response headers."""
    # Act
    response = client.get("/api/health")
    
    # Assert
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) > 0

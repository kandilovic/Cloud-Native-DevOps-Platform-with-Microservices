import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add path to this service's app folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from app.main import app  # noqa: E402

@pytest.fixture
def client():
    """Create a FastAPI test client."""
    return TestClient(app)

def test_healthcheck(client):
    """Check that the service root or /health endpoint works."""
    response = client.get("/")
    assert response.status_code in (200, 404)

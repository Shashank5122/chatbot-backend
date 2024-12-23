
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client

def test_chat(client):
    response = client.post("/chat", json={"message": "Tell me about GEM"})
    assert response.status_code == 200
    assert "response" in response.json

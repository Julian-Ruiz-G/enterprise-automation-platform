from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_tickets_sin_token():
    response = client.get("/tickets")
    assert response.status_code == 401


def test_ai_analyze_sin_token():
    response = client.post(
        "/ai/analyze",
        json={
            "title": "x",
            "description": "y",
            "status": "OPEN",
            "channel": "WEB",
            "client_id": 1,
        },
    )
    assert response.status_code == 401


def test_workflows_sin_token():
    response = client.get("/workflows")
    assert response.status_code == 401
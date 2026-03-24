from fastapi.testclient import TestClient

from app.main import app


def test_preflight_endpoint_returns_parsed_blocks():
    client = TestClient(app)
    response = client.post(
        "/api/pdf/preflight",
        json={"content": "# Title\n- item", "layout_id": "default", "title": "Doc"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["valid"] is True
    assert isinstance(payload["blocks"], list)

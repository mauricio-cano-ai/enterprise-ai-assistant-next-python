from fastapi.testclient import TestClient

from app.main import create_app
from app.models.chat import ChatRequest


def test_health_and_chat_request_contract() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    request = ChatRequest(
        message="How should we evaluate an agent?",
        conversation_id=None,
        tenant_id="tenant-demo",
        user_id="user-demo",
    )
    assert request.tenant_id == "tenant-demo"

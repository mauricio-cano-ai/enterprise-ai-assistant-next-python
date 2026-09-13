import json

from fastapi.testclient import TestClient

from app.main import create_app


def _events(response_text: str) -> list[dict]:
    return [json.loads(line) for line in response_text.splitlines() if line.strip()]


def test_chat_stream_emits_tokens_citations_and_done() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/chat/stream",
        json={
            "message": "How should agent changes be evaluated?",
            "conversation_id": None,
            "tenant_id": "tenant-demo",
            "user_id": "user-demo",
        },
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/x-ndjson")
    events = _events(response.text)
    assert any(event["type"] == "token" for event in events)
    assert any(event["type"] == "citation" for event in events)
    assert events[-1] == {"type": "done"}


def test_chat_stream_rejects_unknown_identity_scope() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/chat/stream",
        json={
            "message": "Show me the evaluation guide",
            "conversation_id": None,
            "tenant_id": "tenant-other",
            "user_id": "user-demo",
        },
    )

    assert response.status_code == 403


def test_chat_stream_rejects_blank_message_before_streaming() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/v1/chat/stream",
        json={
            "message": "",
            "conversation_id": None,
            "tenant_id": "tenant-demo",
            "user_id": "user-demo",
        },
    )

    assert response.status_code == 422

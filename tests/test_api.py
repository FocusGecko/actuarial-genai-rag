"""Tests for the chat API endpoint."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from actuarial_genai_rag.api.app import app

client = TestClient(app)


def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("actuarial_genai_rag.api.app.generate_answer")
def test_chat(mock_generate):
    mock_generate.return_value = "Solvabilité 2 est un cadre réglementaire européen."
    response = client.post("/api/chat", json={"question": "Qu'est-ce que Solvabilité 2 ?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Solvabilité 2 est un cadre réglementaire européen."
    assert data["sources"] == []
    mock_generate.assert_called_once_with(question="Qu'est-ce que Solvabilité 2 ?")


def test_chat_missing_question():
    response = client.post("/api/chat", json={})
    assert response.status_code == 422

from fastapi.testclient import TestClient


def test_api_source_financial_and_question_contracts(session, encoder, monkeypatch):
    from apps.api import main

    monkeypatch.setitem(main.state, "encoder", encoder)
    with TestClient(main.app) as client:
        assert client.get("/api/health").json()["live_ai_available"] is False
        source = next(s for s in client.get("/api/sources").json() if s["company"] == "NVDA")
        assert source["checksum"] and source["publication_date"] == "2025-02-26"
        assert "storage_key" not in source
        metric = client.get("/api/financials/NVDA?metric=free_cash_flow").json()
        assert metric["value"] == "60724.0000" and len(metric["inputs"]) == 3
        assert client.get("/api/financials/TSM").status_code == 404
        assert client.get("/api/financials/NVDA?as_of=2025-02-25").status_code == 404
        assert (
            client.post(
                "/api/questions", json={"question": "What was NVIDIA gross margin in FY2025?"}
            ).json()["mode"]
            == "financial_tool"
        )
        assert client.post("/api/questions", json={"question": "x" * 1201}).status_code == 422


def test_unconfigured_live_model_does_not_become_a_fake_generation(session, encoder, monkeypatch):
    from apps.api import main

    monkeypatch.setitem(main.state, "encoder", encoder)
    with TestClient(main.app) as client:
        response = client.post(
            "/api/questions",
            json={
                "question": "What was reported research and development expense?",
                "mode": "live",
            },
        )
        assert response.status_code == 503
        assert "paragraphs" not in response.json()


def test_cors_rejects_arbitrary_browser_origins(session):
    from apps.api.main import app

    with TestClient(app) as client:
        response = client.options(
            "/api/questions",
            headers={
                "Origin": "https://untrusted.example",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert "access-control-allow-origin" not in response.headers

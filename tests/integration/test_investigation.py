from datetime import date

from sqlalchemy import func, select

from semiconductor_research.database.models import Fact, Source
from semiconductor_research.financials.investigation import cash_investigation
from semiconductor_research.ingestion.tsmc import ingest_tsmc
from semiconductor_research.retrieval.answer import Question, answer_question
from semiconductor_research.retrieval.hybrid import RetrievalFilters


def test_tsmc_reingestion_is_idempotent(session, encoder):
    before = session.scalar(select(func.count()).select_from(Fact))
    assert all(not r["created"] for r in ingest_tsmc(session, encoder, recorded=True))
    assert session.scalar(select(func.count()).select_from(Fact)) == before


def test_investigation_respects_report_availability_and_resolves_inputs(session):
    hidden = cash_investigation(session, date(2025, 3, 11))
    assert not next(
        p for p in hidden["periods"] if p["window"] == "latest" and p["company"] == "TSM"
    )["metrics"]
    available = cash_investigation(session, date(2025, 3, 13))
    assert all(p["metrics"] for p in available["periods"])
    assert not available["human_reviewed"] and not available["historical_archive_certified"]
    for period in available["periods"]:
        for metric in period["metrics"]:
            for item in metric["inputs"]:
                assert session.get(Fact, item["fact_id"]).company == period["company"]
                assert session.get(Source, item["source_id"]).checksum == item["document_checksum"]


def test_tsmc_answer_keeps_calendar_currency_and_residual_definition(session, encoder):
    response = answer_question(
        session,
        encoder,
        Question(
            question="What was TSMC free cash flow in CY2024?",
            filters=RetrievalFilters(company="TSM", as_of=date(2025, 3, 13)),
        ),
    )
    assert not response["abstained"]
    assert response["calculation"]["value"] == "870170532.0000"
    assert "TWD thousand" in response["paragraphs"][0]["text"]
    assert "Not a harmonized FCF" in response["paragraphs"][0]["text"]
    assert all(e["title"].startswith("TSMC") for e in response["evidence"])
    assert len(response["evidence"]) == 2
    earlier = answer_question(
        session,
        encoder,
        Question(
            question="What was TSMC free cash flow in CY2024?",
            filters=RetrievalFilters(company="TSM", as_of=date(2025, 3, 11)),
        ),
    )
    assert earlier["abstained"]


def test_question_company_mismatch_cannot_return_other_company_cash(session, encoder):
    response = answer_question(
        session,
        encoder,
        Question(
            question="What was NVIDIA free cash flow in FY2025?",
            filters=RetrievalFilters(company="TSM", as_of=date(2025, 3, 13)),
        ),
    )
    assert response["abstained"] and not response["paragraphs"]


def test_investigation_api_and_company_coverage(session):
    from fastapi.testclient import TestClient

    from apps.api.main import app

    with TestClient(app) as client:
        result = client.get("/api/investigation?as_of=2025-03-13")
        assert result.status_code == 200 and len(result.json()["periods"]) == 4
        companies = client.get("/api/companies").json()
        assert {c["ticker"] for c in companies if c["coverage"] == "financial_pilot"} == {
            "NVDA",
            "TSM",
            "ASML",
            "MU",
            "TXN",
            "AMKR",
        }
        metric = client.get(
            "/api/financials/TSM?metric=free_cash_flow&period_end=2024-12-31&as_of=2025-03-13"
        ).json()
        assert metric["value"] == "870170532.0000" and metric["unit"] == "TWD thousand"


def test_explicit_calendar_or_fx_requests_are_not_relabelled(session, encoder):
    for company, question in [
        ("NVDA", "What was NVIDIA revenue in CY2024?"),
        ("TSM", "What was TSMC free cash flow in USD in 2024?"),
    ]:
        result = answer_question(
            session,
            encoder,
            Question(
                question=question,
                filters=RetrievalFilters(company=company, as_of=date(2025, 3, 13)),
            ),
        )
        assert result["abstained"] and not result["paragraphs"]

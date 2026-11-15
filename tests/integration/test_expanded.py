from datetime import date

import pytest
from sqlalchemy import func, select

from semiconductor_research.database.models import Fact, Source
from semiconductor_research.financials.engine import Metric, MissingEvidence, calculate_metric
from semiconductor_research.ingestion.expanded import ingest_expanded
from semiconductor_research.retrieval.answer import Question, answer_question
from semiconductor_research.retrieval.hybrid import RetrievalFilters


def test_expanded_ingestion_idempotence_and_source_lineage(session, encoder):
    before = session.scalar(select(func.count()).select_from(Fact))
    assert all(not row["created"] for row in ingest_expanded(session, encoder, recorded=True))
    assert session.scalar(select(func.count()).select_from(Fact)) == before
    result = calculate_metric(
        session, "ASML", Metric.FREE_CASH_FLOW, date(2024, 12, 31), date(2025, 3, 13)
    )
    assert result["value"] == "9083.1000" and result["unit"] == "EUR million"
    for item in result["inputs"]:
        assert session.get(Fact, item["fact_id"]).company == "ASML"
        assert session.get(Source, item["source_id"]).checksum == item["document_checksum"]
    with pytest.raises(MissingEvidence):
        calculate_metric(session, "ASML", Metric.REVENUE, date(2024, 12, 31), date(2025, 3, 4))


@pytest.mark.parametrize(
    "company,question,value,n",
    [
        ("MU", "What was Micron free cash flow in FY2024?", "386.0000", 5),
        ("TXN", "What was Texas Instruments free cash flow in CY2024?", "1498.0000", 2),
        ("AMKR", "What was Amkor free cash flow in CY2024?", "345072.0000", 2),
    ],
)
def test_expanded_questions_keep_definitions_and_exact_fact_citations(
    session, encoder, company, question, value, n
):
    response = answer_question(
        session,
        encoder,
        Question(
            question=question, filters=RetrievalFilters(company=company, as_of=date(2025, 3, 13))
        ),
    )
    assert not response["abstained"] and response["calculation"]["value"] == value
    assert response["model_calls"] == 0 and len(response["evidence"]) == n
    assert all(session.get(Fact, e["fact_id"]).company == company for e in response["evidence"])
    if company == "AMKR":
        assert "NOT Amkor’s reported" in response["paragraphs"][0]["text"]


def test_directory_api_reports_only_actual_financial_coverage(session):
    from fastapi.testclient import TestClient

    from apps.api.main import app

    with TestClient(app) as client:
        directory = client.get("/api/directory").json()
        assert {
            c["financial_company_id"] for c in directory["companies"] if c["financial_loaded"]
        } == {"NVDA", "TSM", "ASML", "MU", "TXN", "AMKR"}
        result = client.get("/api/financials/MU?metric=free_cash_flow&as_of=2025-03-13").json()
        assert result["value"] == "386.0000" and result["period_end"] == "2024-08-29"


@pytest.mark.parametrize(
    "question", ["What was Intel revenue in 2024?", "What was AMD gross margin in 2024?"]
)
def test_directory_company_without_facts_cannot_receive_selected_company_numbers(
    session, encoder, question
):
    response = answer_question(session, encoder, Question(question=question))
    assert response["abstained"] and not response["paragraphs"] and not response["evidence"]

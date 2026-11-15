from datetime import UTC, date, datetime

import pytest
from sqlalchemy import func, select

from semiconductor_research.database.models import Chunk, Fact, Source
from semiconductor_research.financials.engine import Metric, MissingEvidence, calculate_metric
from semiconductor_research.ingestion.service import ingest_nvidia
from semiconductor_research.retrieval.answer import Question, answer_question
from semiconductor_research.retrieval.hybrid import RetrievalFilters, retrieve

pytestmark = pytest.mark.integration


def test_ingestion_is_idempotent(session, encoder):
    before = session.scalar(select(func.count()).select_from(Fact))
    _, created = ingest_nvidia(session, encoder, recorded=True)
    assert not created
    assert session.scalar(select(func.count()).select_from(Fact)) == before


def test_no_lookahead_and_company_filter(session, encoder):
    for filters in [RetrievalFilters(as_of=date(2025, 2, 25)), RetrievalFilters(company="TSM")]:
        assert retrieve(session, encoder, "annual revenue", filters) == []
    with pytest.raises(MissingEvidence):
        calculate_metric(session, "NVDA", Metric.GROSS_MARGIN, date(2025, 1, 26), date(2025, 2, 25))


def test_hybrid_retrieval_has_resolvable_stored_references(session, encoder):
    results = retrieve(
        session, encoder, "NVIDIA annual research and development expense", RetrievalFilters()
    )
    assert results
    assert any(r["topic"] == "research_development" for r in results)
    assert all(
        session.get(Chunk, r["chunk_id"]) and session.get(Source, r["source_id"]) for r in results
    )


def test_topic_period_document_and_publication_filters(session, encoder):
    results = retrieve(
        session,
        encoder,
        "annual revenue",
        RetrievalFilters(
            topic="revenue", period_end=date(2024, 1, 28), document_type="earnings_release"
        ),
    )
    assert results and all(
        r["period_end"] == "2024-01-28" and r["topic"] == "revenue" for r in results
    )
    assert (
        retrieve(session, encoder, "annual revenue", RetrievalFilters(document_type="10-K")) == []
    )
    assert (
        retrieve(
            session, encoder, "annual revenue", RetrievalFilters(publication_from=date(2026, 1, 1))
        )
        == []
    )


def add_revision(session, published_at, value, suffix):
    original = session.scalars(select(Source)).first()
    revision = Source(**{c.name: getattr(original, c.name) for c in Source.__table__.columns})
    revision.id = "synthetic-test-revision-" + suffix
    revision.published_at = published_at
    revision.capture_kind = "synthetic_test_only"
    session.add(revision)
    session.flush()
    original_fact = session.scalars(
        select(Fact).where(Fact.metric == "revenue", Fact.fiscal_label == "FY2025")
    ).first()
    fact = Fact(**{c.name: getattr(original_fact, c.name) for c in Fact.__table__.columns})
    fact.id = "synthetic-revenue-" + suffix
    fact.source_id = revision.id
    fact.value = value
    session.add(fact)
    session.flush()


def test_later_restatement_is_excluded_until_public(session):
    add_revision(session, datetime(2025, 6, 1, tzinfo=UTC), 140000, "later")
    original = calculate_metric(
        session, "NVDA", Metric.REVENUE, date(2025, 1, 26), date(2025, 3, 1)
    )
    revised = calculate_metric(session, "NVDA", Metric.REVENUE, date(2025, 1, 26), date(2025, 6, 2))
    assert original["value"] == "130497.0000"
    assert revised["value"] == "140000.0000"


def test_same_publication_conflict_requires_review(session):
    original = session.scalars(select(Source)).first()
    add_revision(session, original.published_at, 140000, "conflicting")
    with pytest.raises(MissingEvidence, match="Conflicting"):
        calculate_metric(session, "NVDA", Metric.REVENUE, date(2025, 1, 26), date(2025, 3, 1))


@pytest.mark.parametrize(
    "question",
    [
        "What is NVIDIA stock price today?",
        "Compare TSMC and NVIDIA gross margins.",
        "What is NVIDIA revenue in FY2028?",
    ],
)
def test_unsupported_financial_questions_do_not_get_substitute_answers(session, encoder, question):
    response = answer_question(session, encoder, Question(question=question))
    assert response["abstained"] and not response["paragraphs"] and response["model_calls"] == 0


def test_financial_citations_resolve_to_the_exact_input_facts(session, encoder):
    response = answer_question(
        session, encoder, Question(question="What was NVIDIA free cash flow in FY2025?")
    )
    assert response["calculation"]["value"] == "60724.0000"
    assert response["mode"] == "financial_tool"
    assert len(response["evidence"]) == 3
    assert all(session.get(Fact, e["fact_id"]) for e in response["evidence"])
    assert all(
        set(p["citations"]) <= {e["citation_id"] for e in response["evidence"]}
        for p in response["paragraphs"]
    )


def test_conflicting_fiscal_year_and_period_filter_abstains(session, encoder):
    body = Question(
        question="What was NVIDIA revenue in FY2025?", filters={"period_end": "2024-01-28"}
    )
    response = answer_question(session, encoder, body)
    assert response["abstained"] and "conflicts" in response["limitation"]


def test_synthetic_database_records_cannot_enter_static_research(session, monkeypatch):
    from contextlib import contextmanager

    from semiconductor_research import cli

    add_revision(session, datetime(2025, 6, 1, tzinfo=UTC), 140000, "export-guard")

    @contextmanager
    def isolated_scope():
        yield session

    monkeypatch.setattr(cli, "session_scope", isolated_scope)
    with pytest.raises(ValueError, match="synthetic"):
        cli.snapshot(date(2025, 7, 1))

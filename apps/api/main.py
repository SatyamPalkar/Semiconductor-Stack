from datetime import date
from threading import Lock

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError

from semiconductor_research.config.settings import settings
from semiconductor_research.database.models import Chunk, Source
from semiconductor_research.database.session import session_scope
from semiconductor_research.documents.embedding import MiniLM
from semiconductor_research.financials.engine import (
    Metric,
    MissingEvidence,
    calculate_metric,
    cutoff,
)
from semiconductor_research.retrieval.answer import Question, answer_question
from semiconductor_research.sources.catalog import COMPANIES

app = FastAPI(title="Semiconductor Research Platform", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().api_origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
lock = Lock()
state = {"encoder": None}


@app.get("/api/health")
def health():
    try:
        with session_scope() as session:
            session.execute(text("SELECT 1"))
            source_count = session.scalar(select(func.count()).select_from(Source))
            chunks = session.scalar(select(func.count()).select_from(Chunk))
    except SQLAlchemyError:
        raise HTTPException(
            503, "Database unavailable. Static research remains available."
        ) from None
    conf = settings()
    return {
        "status": "ok",
        "database": "postgresql+pgvector",
        "sources": source_count,
        "chunks": chunks,
        "live_ai_available": bool(conf.enable_live_llm and conf.groq_api_key and conf.llm_model),
        "default_answer_mode": "extractive; no hosted model calls",
        "financials": "deterministic database tools",
        "embedding_model": conf.embedding_model,
        "workflow_available": False,
    }


@app.get("/api/sources")
def sources(as_of: date = date(2025, 3, 1)):
    with session_scope() as session:
        rows = session.scalars(
            select(Source).where(Source.published_at <= cutoff(as_of)).order_by(Source.id)
        ).all()
        return [
            {
                "id": s.id,
                "company": s.company,
                "title": s.title,
                "publisher": s.publisher,
                "url": s.url,
                "publication_date": s.publication_date,
                "published_at": s.published_at.isoformat(),
                "retrieved_at": s.retrieved_at.isoformat(),
                "checksum": s.checksum,
                "stored_checksum": s.stored_checksum,
                "capture_kind": s.capture_kind,
                "document_type": s.document_type,
                "accounting_basis": s.accounting_basis,
                "accession": s.accession,
            }
            for s in rows
        ]


@app.get("/api/companies")
def companies():
    return COMPANIES


@app.get("/api/financials/{company}")
def financials(
    company: str,
    metric: Metric = Metric.GROSS_MARGIN,
    period_end: date = date(2025, 1, 26),
    as_of: date = date(2025, 3, 1),
):
    if company not in {c["ticker"] for c in COMPANIES}:
        raise HTTPException(404, "Company is outside the pilot coverage")
    try:
        with session_scope() as session:
            return calculate_metric(session, company, metric, period_end, as_of)
    except MissingEvidence as exc:
        raise HTTPException(404, str(exc)) from None


@app.post("/api/questions")
def questions(body: Question):
    if not lock.acquire(blocking=False):
        raise HTTPException(429, "A research question is already running. Try again shortly.")
    try:
        if state["encoder"] is None:
            state["encoder"] = MiniLM()
        with session_scope() as session:
            return answer_question(session, state["encoder"], body)
    except (ValueError, RuntimeError) as exc:
        raise HTTPException(503, str(exc)) from None
    except SQLAlchemyError:
        raise HTTPException(
            503, "Research database unavailable; no fallback answer was generated"
        ) from None
    finally:
        lock.release()

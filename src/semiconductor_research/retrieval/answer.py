import re
import time
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from semiconductor_research.config.settings import settings
from semiconductor_research.database.models import Fact, Source
from semiconductor_research.financials.engine import (
    Metric,
    MissingEvidence,
    calculate_metric,
    cutoff,
)
from semiconductor_research.financials.profiles import PROFILES
from semiconductor_research.llm.groq import Groq
from semiconductor_research.retrieval.hybrid import RetrievalFilters, retrieve
from semiconductor_research.sources.directory import load_directory

ALIASES = {
    Metric.OCF_MARGIN: ("operating cash flow margin", "operating cash flow / revenue"),
    Metric.CAPEX_OCF: ("capex / operating cash flow", "capital spending / operating cash flow"),
    Metric.FCF_MARGIN: ("free cash flow margin", "fcf margin"),
    Metric.FREE_CASH_FLOW: ("free cash flow", "fcf"),
    Metric.REVENUE_GROWTH: ("revenue growth", "revenue grow", "sales growth"),
    Metric.GROSS_MARGIN: ("gross margin",),
    Metric.OPERATING_MARGIN: ("operating margin",),
    Metric.CAPEX_REVENUE: ("capex", "capital expenditure"),
    Metric.RD_REVENUE: ("r&d", "r and d", "research and development ratio"),
    Metric.OPERATING_CASH_FLOW: ("operating cash flow", "cash from operations"),
    Metric.REVENUE: ("revenue", "sales"),
}

# Bounded financial vocabulary, versioned with the small pilot. Unrecognised
# requests abstain; this does not pretend to be a general conversational router.
FACT_TOPICS = {
    "research_development": ("research and development", "r&d", "r and d"),
    "capital_purchases": (
        "capital purchases",
        "capex",
        "capital expenditure",
        "property and equipment",
    ),
    "capital_principal": ("principal payments",),
    "gross_profit": ("gross profit",),
    "operating_income": ("operating income",),
}


@lru_cache(maxsize=1)
def uncovered_company_patterns():
    # Directory discovery never becomes permission to answer from another issuer.
    names = {
        alias.lower()
        for company in load_directory()["companies"]
        if company["financial_company_id"] is None
        for alias in (company["name"], company["id"].replace("-", " "))
    }
    return tuple(re.compile(r"\b" + re.escape(name) + r"\b") for name in names)


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=3, max_length=1200)
    filters: RetrievalFilters = Field(default_factory=RetrievalFilters)
    mode: Literal["extractive", "live"] = "extractive"
    metric: Metric | None = None

    @field_validator("question", mode="before")
    @classmethod
    def trim_question(cls, value):
        return value.strip() if isinstance(value, str) else value


def answer_question(session: Session, encoder, body: Question):
    started = time.perf_counter()
    if not body.question.strip():
        raise ValueError("Enter a question")
    response = {
        "mode": body.mode,
        "as_of": str(body.filters.as_of),
        "abstained": True,
        "paragraphs": [],
        "evidence": [],
        "calculation": None,
        "citation_support": "not assessed",
        "model_calls": 0,
        "limitation": "The evidence desk supports selected annual financial rows for NVIDIA, TSMC, ASML, Micron, Texas Instruments and Amkor. Use Company comparison for the qualified two-company investigation; forecasts and general industry research are outside this bounded question router.",
    }
    question = body.question.lower()
    # This explicit financial tool selector is intentionally bounded; it is not a conversational controller.
    metric = body.metric or next(
        (m for m, aliases in ALIASES.items() if any(a in question for a in aliases)), None
    )
    if (
        body.metric is None
        and metric in {Metric.CAPEX_REVENUE, Metric.RD_REVENUE}
        and not any(
            term in question for term in ("ratio", "percentage", "%", "/ revenue", "of revenue")
        )
    ):
        metric = None
    profile = PROFILES.get(body.filters.company)
    company_name = profile.name if profile else body.filters.company
    label_prefix = profile.prefix if profile else "FY"
    mentioned = {
        ticker
        for ticker, names in {key: p.aliases for key, p in PROFILES.items()}.items()
        if any(re.search(rf"\b{name}\b", question) for name in names)
    }
    requested_years = re.findall(r"\b(?:(?:fy|cy)\s*)?(20\d{2})\b", question)
    unsupported = (
        profile is None
        or any(pattern.search(question) for pattern in uncovered_company_patterns())
        or bool(mentioned - {body.filters.company})
        or (
            label_prefix == "FY"
            and bool(re.search(r"\b(?:cy\s*20\d{2}|calendar year)\b", question))
        )
        or (label_prefix == "CY" and bool(re.search(r"\bfy\s*20\d{2}\b", question)))
        or any(
            code != (profile.currency if profile else "")
            for code, pattern in {
                "USD": r"\b(?:usd|us dollars|u\.s\. dollars)\b",
                "TWD": r"\b(?:twd|ntd|taiwan dollars)\b",
                "EUR": r"\b(?:eur|euros?)\b",
            }.items()
            if re.search(pattern, question)
        )
        or bool(re.search(r"\b(?:quarter(?:ly)?|q[1-4]|ttm|trailing)\b", question))
        or len(set(requested_years)) > 1
        or any(
            term in question
            for term in (
                "forecast",
                "next year",
                "today",
                "current",
                "stock price",
                "share price",
                "compare",
                "valuation",
                "dcf",
                "convert",
                "exchange rate",
            )
        )
    )
    if unsupported:
        response["latency_ms"] = round((time.perf_counter() - started) * 1000, 2)
        return response
    period = body.filters.period_end
    if metric:
        candidate_rows = session.execute(
            select(Fact.period_end, Fact.fiscal_label)
            .join(Source)
            .where(
                Fact.company == body.filters.company,
                Source.published_at <= cutoff(body.filters.as_of),
                Fact.period_kind == "annual",
            )
            .distinct()
            .order_by(Fact.period_end.desc())
        ).all()
        candidates = [
            end
            for end, label in candidate_rows
            if not requested_years or label == f"{label_prefix}{requested_years[-1]}"
        ]
        if period is not None and requested_years and period not in candidates:
            response["limitation"] = (
                "The requested fiscal year conflicts with the selected reporting-period filter."
            )
            response["latency_ms"] = round((time.perf_counter() - started) * 1000, 2)
            return response
        if period is None and candidates:
            period = candidates[0]
        if period:
            try:
                calculation = calculate_metric(
                    session, body.filters.company, metric, period, body.filters.as_of
                )
            except MissingEvidence:
                calculation = None
            if calculation:
                evidence = []
                for fact in calculation["inputs"]:
                    evidence.append(
                        {
                            **fact,
                            "citation_id": len(evidence) + 1,
                            "chunk_id": fact["fact_id"],
                            "text": f"{fact['fiscal_label']} {fact['metric'].replace('_', ' ')}: {fact['value']} {fact['currency']} at original scale {fact['unit_scale']}.",
                            "title": fact["source_title"],
                        }
                    )
                response.update(
                    abstained=False,
                    calculation=calculation,
                    evidence=evidence,
                    mode="financial_tool",
                    citation_support="deterministic calculation from the referenced database facts",
                    paragraphs=[
                        {
                            "text": f"{company_name} {calculation['fiscal_label']} {calculation['label']} was {calculation['value']} {calculation['unit']} (annual period ended {period}). {calculation['definition']}",
                            "citations": list(range(1, len(evidence) + 1)),
                            "classification": calculation["classification"],
                        }
                    ],
                )
    if response["abstained"] and metric is None:
        topic = next(
            (key for key, aliases in FACT_TOPICS.items() if any(a in question for a in aliases)),
            None,
        )
        filters = body.filters.model_copy(update={"topic": topic}) if topic else body.filters
        if requested_years:
            # Resolve fiscal labels against database periods, never an invented calendar conversion.
            ends = session.scalars(
                select(Fact.period_end)
                .where(
                    Fact.company == filters.company,
                    Fact.fiscal_label == f"{label_prefix}{requested_years[-1]}",
                )
                .distinct()
            ).all()
            if len(ends) == 1:
                filters = filters.model_copy(update={"period_end": ends[0]})
            else:
                topic = None
        evidence = retrieve(session, encoder, body.question, filters) if topic else []
        if evidence and body.mode == "live":
            draft = Groq(settings()).generate(body.question, evidence)
            response.update(draft, evidence=evidence, model_calls=1)
        elif evidence:
            response.update(
                evidence=evidence,
                mode="extractive",
                abstained=False,
                citation_support="verbatim stored evidence; answerability and completeness not independently reviewed",
                paragraphs=[
                    {
                        "text": item["text"],
                        "citations": [item["citation_id"]],
                        "classification": "evidence",
                    }
                    for item in evidence[:3]
                ],
            )
    response["latency_ms"] = round((time.perf_counter() - started) * 1000, 2)
    return response

from datetime import UTC, date, datetime, time
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import select
from sqlalchemy.orm import Session

from semiconductor_research.database.models import Fact, Source


class Metric(StrEnum):
    REVENUE = "revenue"
    REVENUE_GROWTH = "revenue_growth"
    GROSS_MARGIN = "gross_margin"
    OPERATING_MARGIN = "operating_margin"
    CAPEX_REVENUE = "capex_revenue"
    RD_REVENUE = "rd_revenue"
    OPERATING_CASH_FLOW = "operating_cash_flow"
    FREE_CASH_FLOW = "free_cash_flow"
    FCF_MARGIN = "free_cash_flow_margin"


DEFINITIONS = {
    "revenue": "Reported annual revenue; no currency conversion.",
    "revenue_growth": "(Annual revenue / prior annual revenue - 1) × 100. Prior end dates must be 350–380 days apart.",
    "gross_margin": "Gross profit / revenue × 100.",
    "operating_margin": "Operating income / revenue × 100.",
    "capex_revenue": "Purchases of property, equipment and intangible assets / revenue × 100. Intangibles included; not comparable to PPE-only capex.",
    "rd_revenue": "Research and development expense / revenue × 100.",
    "operating_cash_flow": "Reported net cash provided by operating activities.",
    "free_cash_flow": "Operating cash flow less purchases AND principal payments related to property, equipment and intangible assets. NVIDIA release definition; non-GAAP measure.",
    "free_cash_flow_margin": "Free cash flow (including capital principal payments) / revenue × 100.",
}


def cutoff(as_of: date):
    return datetime.combine(as_of, time.max, tzinfo=UTC)


class MissingEvidence(ValueError):
    pass


def select_facts(session: Session, company: str, as_of: date):
    rows = session.execute(
        select(Fact, Source)
        .join(Source, Fact.source_id == Source.id)
        .where(Fact.company == company, Source.published_at <= cutoff(as_of))
        .order_by(Source.published_at.desc(), Source.retrieved_at.desc(), Source.id)
    ).all()
    selected, conflicts = {}, set()
    for fact, source in rows:
        key = (fact.period_end, fact.period_kind, fact.metric)
        if key in selected:
            old_fact, old_source = selected[key]
            if source.published_at == old_source.published_at and fact.value != old_fact.value:
                conflicts.add(key)
            continue
        selected[key] = (fact, source)
    if conflicts:
        raise MissingEvidence("Conflicting same-publication financial facts require source review")
    return selected


def calculate_metric(session: Session, company: str, metric: Metric, period_end: date, as_of: date):
    selected = select_facts(session, company, as_of)
    used = []

    def amount(name, end=period_end):
        pair = selected.get((end, "annual", name))
        if pair is None:
            raise MissingEvidence(f"Missing annual {name} evidence available as of {as_of}")
        fact, source = pair
        if fact.currency != "USD" or fact.unit_scale != 1_000_000:
            raise MissingEvidence("Unsupported currency/unit combination; no implicit conversion")
        used.append((fact, source))
        return fact.value

    def ratio(numerator, denominator):
        if denominator == 0:
            raise MissingEvidence("Cannot divide by zero revenue")
        return numerator / denominator * Decimal(100)

    if metric == Metric.REVENUE:
        value, unit = amount("revenue"), "USD million"
    elif metric == Metric.OPERATING_CASH_FLOW:
        value, unit = amount("operating_cash_flow"), "USD million"
    elif metric in {Metric.FREE_CASH_FLOW, Metric.FCF_MARGIN}:
        value = (
            amount("operating_cash_flow")
            - amount("capital_purchases")
            - amount("capital_principal")
        )
        unit = "USD million"
        if metric == Metric.FCF_MARGIN:
            value, unit = ratio(value, amount("revenue")), "%"
    elif metric == Metric.REVENUE_GROWTH:
        prior = sorted(
            {
                key[0]
                for key in selected
                if key[1:] == ("annual", "revenue") and 350 <= (period_end - key[0]).days <= 380
            },
            reverse=True,
        )
        if not prior:
            raise MissingEvidence("Missing comparable prior annual revenue")
        value, unit = ratio(amount("revenue"), amount("revenue", prior[0])) - 100, "%"
    else:
        numerator = {
            Metric.GROSS_MARGIN: "gross_profit",
            Metric.OPERATING_MARGIN: "operating_income",
            Metric.CAPEX_REVENUE: "capital_purchases",
            Metric.RD_REVENUE: "research_development",
        }[metric]
        value, unit = ratio(amount(numerator), amount("revenue")), "%"
    bases = {s.accounting_basis for _, s in used}
    if len(bases) != 1:
        raise MissingEvidence("Accounting bases differ; manual reconciliation is required")
    return {
        "company": company,
        "metric": metric.value,
        "value": str(value.quantize(Decimal("0.0001"))),
        "unit": unit,
        "period_end": str(period_end),
        "period_kind": "annual",
        "as_of": str(as_of),
        "fiscal_label": used[0][0].fiscal_label,
        "classification": "reported_fact"
        if metric in {Metric.REVENUE, Metric.OPERATING_CASH_FLOW}
        else "calculated_metric",
        "definition": DEFINITIONS[metric.value],
        "accounting_basis": next(iter(bases)),
        "inputs": [
            {
                "fact_id": f.id,
                "metric": f.metric,
                "value": str(f.value),
                "currency": f.currency,
                "unit_scale": f.unit_scale,
                "period_end": str(f.period_end),
                "fiscal_label": f.fiscal_label,
                "source_id": s.id,
                "locator": f.locator,
                "published_at": s.published_at.isoformat(),
                "document_checksum": s.checksum,
                "url": s.url,
            }
            for f, s in used
        ],
    }

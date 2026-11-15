from datetime import UTC, date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from semiconductor_research.financials.engine import Metric, MissingEvidence, calculate_metric

END = date(2025, 1, 26)
AS_OF = date(2025, 3, 1)


def inputs():
    source = SimpleNamespace(
        id="test-source",
        accounting_basis="US GAAP",
        checksum="0" * 64,
        url="https://example.test/financials",
        published_at=datetime(2025, 2, 27, tzinfo=UTC),
    )
    values = {
        "revenue": "130497",
        "gross_profit": "97858",
        "operating_income": "81453",
        "operating_cash_flow": "64089",
        "capital_purchases": "3236",
        "capital_principal": "129",
        "research_development": "12914",
    }
    selected = {}
    for metric, value in values.items():
        fact = SimpleNamespace(
            id=metric,
            metric=metric,
            value=Decimal(value),
            currency="USD",
            unit_scale=1000000,
            period_end=END,
            fiscal_label="FY2025",
            locator="recorded row",
        )
        selected[(END, "annual", metric)] = (fact, source)
    prior = SimpleNamespace(
        id="prior-revenue",
        metric="revenue",
        value=Decimal("60922"),
        currency="USD",
        unit_scale=1000000,
        period_end=date(2024, 1, 28),
        fiscal_label="FY2024",
        locator="prior annual row",
    )
    selected[(prior.period_end, "annual", "revenue")] = (prior, source)
    return selected


@pytest.mark.parametrize(
    ("metric", "expected"),
    [
        (Metric.REVENUE_GROWTH, "114.2034"),
        (Metric.GROSS_MARGIN, "74.9887"),
        (Metric.OPERATING_MARGIN, "62.4175"),
        (Metric.CAPEX_REVENUE, "2.4798"),
        (Metric.RD_REVENUE, "9.8960"),
        (Metric.FREE_CASH_FLOW, "60724.0000"),
        (Metric.OPERATING_CASH_FLOW, "64089.0000"),
        (Metric.FCF_MARGIN, "46.5329"),
    ],
)
def test_recorded_source_calculation_oracles(metric, expected):
    with patch("semiconductor_research.financials.engine.select_facts", return_value=inputs()):
        result = calculate_metric(None, "NVDA", metric, END, AS_OF)
    assert result["value"] == expected
    assert result["inputs"]
    assert all(i["source_id"] == "test-source" for i in result["inputs"])


@pytest.mark.parametrize(
    "missing", ["capital_purchases", "capital_principal", "operating_cash_flow"]
)
def test_missing_cashflow_component_is_never_zero(missing):
    values = inputs()
    del values[(END, "annual", missing)]
    with (
        patch("semiconductor_research.financials.engine.select_facts", return_value=values),
        pytest.raises(MissingEvidence),
    ):
        calculate_metric(None, "NVDA", Metric.FREE_CASH_FLOW, END, AS_OF)


def test_zero_denominator_is_not_infinity():
    values = inputs()
    values[(END, "annual", "revenue")][0].value = Decimal(0)
    with (
        patch("semiconductor_research.financials.engine.select_facts", return_value=values),
        pytest.raises(MissingEvidence),
    ):
        calculate_metric(None, "NVDA", Metric.GROSS_MARGIN, END, AS_OF)


def test_currency_scale_and_quarterly_inputs_are_not_silently_mixed():
    for attribute, value in [("currency", "TWD"), ("unit_scale", 1000)]:
        values = inputs()
        setattr(values[(END, "annual", "revenue")][0], attribute, value)
        with (
            patch("semiconductor_research.financials.engine.select_facts", return_value=values),
            pytest.raises(MissingEvidence),
        ):
            calculate_metric(None, "NVDA", Metric.GROSS_MARGIN, END, AS_OF)
    values = inputs()
    values[(END, "quarterly", "revenue")] = values.pop((END, "annual", "revenue"))
    with (
        patch("semiconductor_research.financials.engine.select_facts", return_value=values),
        pytest.raises(MissingEvidence),
    ):
        calculate_metric(None, "NVDA", Metric.GROSS_MARGIN, END, AS_OF)

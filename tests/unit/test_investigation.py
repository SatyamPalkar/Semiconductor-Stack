"""Real recorded table checks; synthetic scenarios remain in memory only."""

import json
from datetime import UTC, date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from semiconductor_research.config.settings import ROOT
from semiconductor_research.financials.engine import Metric, MissingEvidence, calculate_metric
from semiconductor_research.ingestion.tsmc import BASIS, parse_excerpt


def excerpt(year=2024):
    return json.loads((ROOT / f"data/fixtures/tsmc-{year}-annual-excerpt.json").read_text())


def tsmc_inputs():
    selected = {}
    for year in (2024, 2023):
        source = SimpleNamespace(
            id=f"recorded-tsmc-{year}",
            title=f"TSMC {year} annual report",
            accounting_basis=BASIS,
            checksum="0" * 64,
            url="https://investor.tsmc.com/",
            published_at=datetime(2025, 3, 12, 15, 59, 59, tzinfo=UTC),
        )
        for fact in parse_excerpt(excerpt(year)):
            selected[(fact["period_end"], "annual", fact["metric"])] = (
                SimpleNamespace(id=f"{year}-{fact['fiscal_label']}-{fact['metric']}", **fact),
                source,
            )
    return selected


def test_tsmc_consolidated_units_and_periods_are_preserved():
    facts = parse_excerpt(excerpt())
    current = {f["metric"]: f for f in facts if f["fiscal_label"] == "CY2024"}
    assert current["revenue"]["value"] == Decimal("2894307699")
    assert current["operating_cash_flow"]["value"] == Decimal("1826177068")
    assert current["capital_expenditures"]["value"] == Decimal("956006536")
    assert all(f["currency"] == "TWD" and f["unit_scale"] == 1000 for f in facts)
    assert all(f["period_start"] == date(int(f["fiscal_label"][2:]), 1, 1) for f in facts)
    assert "PDF p. 65" in current["operating_cash_flow"]["locator"]
    assert parse_excerpt(excerpt(2023))[0]["value"] == Decimal("1241967347")


@pytest.mark.parametrize(
    ("field", "before", "after"),
    [
        ("cash", "NT$ thousands", "NT$ millions"),
        ("income", "2024 2023 Difference", "2023 2024 Difference"),
        ("cash", "Consolidated", "Unconsolidated"),
        ("capital", "956,006,536", "956,006,537"),
    ],
)
def test_tsmc_schema_or_scope_changes_fail_closed(field, before, after):
    data = excerpt()
    data[field] = data[field].replace(before, after)
    with pytest.raises(ValueError):
        parse_excerpt(data)


@pytest.mark.parametrize(
    ("metric", "value", "unit"),
    [
        (Metric.REVENUE, "2894307699.0000", "TWD thousand"),
        (Metric.FREE_CASH_FLOW, "870170532.0000", "TWD thousand"),
        (Metric.OCF_MARGIN, "63.0955", "%"),
        (Metric.FCF_MARGIN, "30.0649", "%"),
        (Metric.CAPEX_REVENUE, "33.0306", "%"),
    ],
)
def test_real_tsmc_cash_calculations_have_company_specific_scope(metric, value, unit):
    with patch("semiconductor_research.financials.engine.select_facts", return_value=tsmc_inputs()):
        result = calculate_metric(None, "TSM", metric, date(2024, 12, 31), date(2025, 3, 13))
    assert result["value"] == value and result["unit"] == unit
    assert result["currency"] == "TWD" and result["unit_scale"] == 1000
    if metric in {Metric.FREE_CASH_FLOW, Metric.FCF_MARGIN}:
        assert "Not a harmonized FCF" in result["definition"]
        assert {i["metric"] for i in result["inputs"]} >= {
            "operating_cash_flow",
            "capital_expenditures",
        }
        assert all(i["metric"] != "capital_principal" for i in result["inputs"])


def test_missing_tsmc_capital_outlays_cannot_be_silently_zero():
    data = tsmc_inputs()
    del data[(date(2024, 12, 31), "annual", "capital_expenditures")]
    with (
        patch("semiconductor_research.financials.engine.select_facts", return_value=data),
        pytest.raises(MissingEvidence),
    ):
        calculate_metric(None, "TSM", Metric.FREE_CASH_FLOW, date(2024, 12, 31), date(2025, 3, 13))

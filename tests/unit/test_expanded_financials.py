import json
from datetime import UTC, date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from semiconductor_research.config.settings import ROOT
from semiconductor_research.financials.engine import Metric, MissingEvidence, calculate_metric
from semiconductor_research.ingestion.expanded import REPORTS, parse_excerpt


def facts(company):
    report = REPORTS[company]
    data = json.loads((ROOT / f"data/fixtures/{report['stem']}-excerpt.json").read_text())
    return parse_excerpt(data)


def selected(company):
    source = SimpleNamespace(
        id="recorded-real-tables",
        title=REPORTS[company]["title"],
        accounting_basis=REPORTS[company]["basis"],
        published_at=datetime(2025, 3, 6, tzinfo=UTC),
        checksum="0" * 64,
        url=REPORTS[company]["url"],
    )
    return {
        (f["period_end"], "annual", f["metric"]): (SimpleNamespace(id=f["metric"], **f), source)
        for f in facts(company)
    }


@pytest.mark.parametrize(
    "company,end,expected,unit",
    [
        ("ASML", date(2024, 12, 31), "9083.1000", "EUR million"),
        ("MU", date(2024, 8, 29), "386.0000", "USD million"),
        ("TXN", date(2024, 12, 31), "1498.0000", "USD million"),
        ("AMKR", date(2024, 12, 31), "345072.0000", "USD thousand"),
    ],
)
def test_native_currency_cashflow_oracles_and_exact_inputs(company, end, expected, unit):
    with patch(
        "semiconductor_research.financials.engine.select_facts", return_value=selected(company)
    ):
        result = calculate_metric(None, company, Metric.FREE_CASH_FLOW, end, date(2025, 3, 13))
    assert result["value"] == expected and result["unit"] == unit
    if company == "MU":
        assert {i["metric"] for i in result["inputs"]} == {
            "operating_cash_flow",
            "capital_purchases",
            "capital_principal",
            "capital_asset_sales",
            "capital_grants",
        }
    if company == "AMKR":
        assert "NOT Amkor’s reported free cash flow" in result["definition"]
        assert result["label"] == "analytical gross-PPE cash residual"


def test_negative_memory_cycle_is_preserved():
    data = selected("MU")
    assert data[(date(2023, 8, 31), "annual", "gross_profit")][0].value == Decimal(-1416)
    with patch("semiconductor_research.financials.engine.select_facts", return_value=data):
        result = calculate_metric(
            None, "MU", Metric.GROSS_MARGIN, date(2023, 8, 31), date(2025, 3, 13)
        )
    assert result["value"] == "-9.1120"


@pytest.mark.parametrize(
    "component", ["capital_asset_sales", "capital_grants", "capital_principal"]
)
def test_missing_micron_offset_or_payment_cannot_be_zero(component):
    data = selected("MU")
    del data[(date(2024, 8, 29), "annual", component)]
    with (
        patch("semiconductor_research.financials.engine.select_facts", return_value=data),
        pytest.raises(MissingEvidence),
    ):
        calculate_metric(None, "MU", Metric.FREE_CASH_FLOW, date(2024, 8, 29), date(2025, 3, 13))


def test_unit_and_reconciliation_changes_stop_ingestion():
    data = json.loads((ROOT / "data/fixtures/mu-fy2024-excerpt.json").read_text())
    data["tables"][0] = data["tables"][0].replace("In millions", "In thousands")
    with pytest.raises(ValueError, match="unit"):
        parse_excerpt(data)
    data = json.loads((ROOT / "data/fixtures/asml-2024-financial-excerpt.json").read_text())
    data["income"] = data["income"].replace("27,558.5", "27,558.5 100")
    with pytest.raises(ValueError, match="layout"):
        parse_excerpt(data)


def test_reordered_annual_headers_do_not_silently_swap_periods():
    data = json.loads((ROOT / "data/fixtures/asml-2024-financial-excerpt.json").read_text())
    data["cash"] = data["cash"].replace("2023 2024", "2024 2023")
    with pytest.raises(ValueError, match="column order"):
        parse_excerpt(data)

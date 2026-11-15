"""One bounded investigation over database-authoritative, company-specific metrics."""

from datetime import date

from semiconductor_research.financials.engine import Metric, MissingEvidence, calculate_metric

WINDOWS = {
    "latest": {"NVDA": date(2025, 1, 26), "TSM": date(2024, 12, 31)},
    "prior": {"NVDA": date(2024, 1, 28), "TSM": date(2023, 12, 31)},
}


def cash_investigation(session, as_of: date):
    periods = []
    for window, companies in WINDOWS.items():
        for company, end in companies.items():
            metrics, missing = [], []
            for key in Metric:
                try:
                    metrics.append(calculate_metric(session, company, key, end, as_of))
                except MissingEvidence as exc:
                    missing.append({"metric": key.value, "reason": str(exc)})
            periods.append(
                {
                    "window": window,
                    "company": company,
                    "period_end": str(end),
                    "metrics": metrics,
                    "missing": missing,
                }
            )
    return {
        "id": "nvda-tsmc-cash-v1",
        "as_of": str(as_of),
        "periods": periods,
        "human_reviewed": False,
        "historical_archive_certified": False,
        "comparability": {
            "periods": "NVIDIA FY2025 ends 26 Jan 2025; TSMC CY2024 ends 31 Dec 2024. Prior periods also differ; no calendar alignment is inferred.",
            "currency": "NVIDIA USD millions; TSMC TWD thousands. Ratios are calculated within each company. No FX conversion or addition of revenues across supply-chain layers.",
            "accounting": "NVIDIA US GAAP earnings-release data and TSMC Taiwan IFRS annual-report tables. Operating cash-flow classifications are not harmonized.",
            "capital": "NVIDIA purchases include PPE and intangibles; its residual also subtracts related principal payments. TSMC uses annual-report capital expenditures, without assuming identical asset, lease or intangible scope.",
            "interpretation": "A two-period descriptive comparison, not a causal test, full-cycle study, standardized FCF ranking, valuation or forecast.",
        },
    }

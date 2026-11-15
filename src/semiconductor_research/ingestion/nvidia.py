import re
from decimal import Decimal

from bs4 import BeautifulSoup

from semiconductor_research.sources.catalog import NVIDIA

ROWS = {
    "revenue": ("INCOME", "Revenue"),
    "gross_profit": ("INCOME", "Gross profit"),
    "operating_income": ("INCOME", "Operating income"),
    "research_development": ("INCOME", "Research and development"),
    "operating_cash_flow": ("CASH FLOWS", "Net cash provided by operating activities"),
    "capital_purchases": (
        "CASH FLOWS",
        "Purchase related to property and equipment and intangible assets",
    ),
    "capital_principal": (
        "CASH FLOWS",
        "Principal payments on property and equipment and intangible assets",
    ),
}


def parse_nvidia(content: bytes) -> list[dict]:
    """Annual columns only. Fail closed when the selected source schema changes."""
    soup = BeautifulSoup(content, "html.parser")
    found = []
    for metric, (table_suffix, label) in ROWS.items():
        title = "CONDENSED CONSOLIDATED STATEMENTS OF " + table_suffix
        tables = [t for t in soup.find_all("table") if title in t.get_text(" ", strip=True)]
        if len(tables) != 1:
            raise ValueError(f"Expected one {table_suffix} table")
        table = tables[0]
        header = table.get_text(" ", strip=True)
        if "Twelve Months Ended" not in header or "(In millions" not in header:
            raise ValueError("Annual-period/unit header missing")
        # Do not interpret a shifted year header as the original annual periods.
        if not all(x in header for x in ("2025", "2024", "January 26", "January 28")):
            raise ValueError("Fiscal-year headers changed")
        rows = [r for r in table.find_all("tr") if label in r.get_text(" ", strip=True)]
        if len(rows) != 1:
            raise ValueError(f"Missing or duplicate financial row: {metric}")
        row = rows[0]
        cells = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"], recursive=False)]
        amounts = [
            Decimal(x.replace(",", "").replace("(", "").replace(" ", ""))
            for x in cells
            if re.fullmatch(r"\(?[\d,]+", x.replace(" ", ""))
        ]
        if len(amounts) != 4:
            raise ValueError(f"Expected two quarterly then two annual values for {metric}")
        annual = amounts[-2:]
        outflow = metric in {"capital_purchases", "capital_principal"}
        if outflow and row.get_text().count("(") < 4:
            raise ValueError("Expected cash-outflow parentheses")
        for period, value in zip(NVIDIA["periods"], annual, strict=True):
            found.append(
                {
                    "metric": metric,
                    "value": value,
                    "currency": "USD",
                    "unit_scale": 1_000_000,
                    "period_start": period["start"],
                    "period_end": period["end"],
                    "period_kind": "annual",
                    "fiscal_label": period["label"],
                    "locator": f"{title} / {label} / Twelve Months Ended {period['end']}",
                    "transformations": {
                        "parser": "nvidia-results-v1",
                        "original_cashflow_sign": "negative" if outflow else "positive",
                        "normalization": "positive cash outflow magnitude"
                        if outflow
                        else "reported amount",
                        "source_row": label,
                    },
                }
            )
    return found

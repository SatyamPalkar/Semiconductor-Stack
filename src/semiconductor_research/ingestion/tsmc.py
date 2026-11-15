"""Fixed public annual reports, independent of the previously blocked IR endpoint."""

import hashlib
import io
import json
import re
from datetime import UTC, date, datetime
from decimal import Decimal

import httpx
from pypdf import PdfReader
from sqlalchemy import select

from semiconductor_research.config.settings import ROOT, settings
from semiconductor_research.database.models import Chunk, Fact, Source
from semiconductor_research.documents.chunking import fact_chunks
from semiconductor_research.storage.local import LocalStorage

REPORTS = {
    2024: {
        "url": "https://investor.tsmc.com/sites/ir/annual-report/2024/2024%20Annual%20Report-E.pdf",
        "publication_date": "2025-03-12",
        "published_at": datetime(2025, 3, 12, 15, 59, 59, tzinfo=UTC),
        "cash_page": 65,
        "cash_section": "6.1.3",
        "printed_page": 126,
    },
    2023: {
        "url": "https://investor.tsmc.com/sites/ir/annual-report/2023/2023%20Annual%20Report_E.pdf",
        "publication_date": "2024-03-12",
        "published_at": datetime(2024, 3, 12, 15, 59, 59, tzinfo=UTC),
        "cash_page": 68,
        "cash_section": "6.2.3",
        "printed_page": 132,
    },
}
BASIS = "Taiwan IFRS; consolidated annual report"
NUMBER = r"\(?\d[\d,]*\)?"


def excerpt_pdf(content: bytes, year: int) -> dict:
    report = REPORTS[year]
    reader = PdfReader(io.BytesIO(content))
    cover = reader.pages[0].extract_text()
    printed = "March 12, " + report["publication_date"][:4]
    if f"Printed on {printed}" not in cover:
        raise ValueError("Annual report print date changed")
    cash = reader.pages[report["cash_page"] - 1].extract_text()
    consolidated = cash.split("Unconsolidated")[0]
    # Preserve table headers/rows, excluding unrelated prose and the parent-only table.
    cash_table = consolidated.split("Analysis of Cash Flow")[0]
    if year == 2024:
        income = reader.pages[63].extract_text().split("Unconsolidated")[0]
        income = income.split("Analysis of Deviation")[0]
        capital = cash.split("6.1.4 Recent Years Major Capital Expenditures")[1]
        capital = capital.split("Based on capital expenditures")[0]
    else:
        income, capital = "", ""
    return {
        "year": year,
        "print_date": report["publication_date"],
        "income": income,
        "cash": cash_table,
        "capital": capital,
    }


def parse_excerpt(data: dict) -> list[dict]:
    year = data["year"]
    report = REPORTS[year]
    if data["print_date"] != report["publication_date"]:
        raise ValueError("Publication metadata mismatch")
    cash = data["cash"]
    if not all(
        x in cash
        for x in [report["cash_section"], "Consolidated", "Unit: NT$ thousands", str(year)]
    ):
        raise ValueError("Consolidated cash-flow header changed")
    if "Unconsolidated" in cash:
        raise ValueError("Parent-only statements must not enter the excerpt")
    found = []

    def add(metric, value, period_year, locator):
        found.append(
            {
                "metric": metric,
                "value": Decimal(value.replace(",", "")),
                "currency": "TWD",
                "unit_scale": 1000,
                "period_start": date(period_year, 1, 1),
                "period_end": date(period_year, 12, 31),
                "period_kind": "annual",
                "fiscal_label": f"CY{period_year}",
                "locator": locator,
                "transformations": {
                    "parser": "tsmc-annual-v1",
                    "normalization": "reported positive amount",
                    "source_scope": "consolidated",
                    "source_unit": "NT$ thousands",
                },
            }
        )

    cash_rows = re.findall(
        rf"^({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+({NUMBER})\s+None\s+None\s*$",
        cash,
        re.M,
    )
    if len(cash_rows) != 1 or "Operating" not in cash or f"12/31/{year}" not in cash:
        raise ValueError("Cash-flow column layout changed")
    add(
        "operating_cash_flow",
        cash_rows[0][1],
        year,
        f"Annual report {year} / printed p. {report['printed_page']} (PDF p. {report['cash_page']}) / {report['cash_section']} consolidated cash flow / operating activities {year}",
    )
    if year == 2024:
        income, capital = data["income"], data["capital"]
        if not all(
            x in income
            for x in ["6.1.2", "Consolidated", "Unit: NT$ thousands", "2024 2023 Difference"]
        ):
            raise ValueError("Income statement header changed")
        for label, metric in [
            ("Net Revenue", "revenue"),
            ("Gross Profit", "gross_profit"),
            ("Income from Operations", "operating_income"),
        ]:
            rows = re.findall(rf"^{label}\s+([\d,]+)\s+([\d,]+)\s+[\d,]+\s+\d+%\s*$", income, re.M)
            if len(rows) != 1:
                raise ValueError(f"Income row changed: {label}")
            for period_year, value in zip((2024, 2023), rows[0], strict=True):
                add(
                    metric,
                    value,
                    period_year,
                    f"Annual report 2024 / printed p. 124 (PDF p. 64) / 6.1.2 consolidated financial performance / {label} / {period_year}",
                )
        if not all(
            x in capital for x in ["Unit: NT$ thousands", "Actual Use of Capital", "2024 2023"]
        ):
            raise ValueError("Capital spending header changed")
        totals = re.findall(r"^Total\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s*$", capital, re.M)
        if len(totals) != 1 or Decimal(totals[0][0].replace(",", "")) != sum(
            Decimal(v.replace(",", "")) for v in totals[0][1:]
        ):
            raise ValueError("Capital spending total does not reconcile")
        for period_year, value in zip((2024, 2023), totals[0][1:], strict=True):
            add(
                "capital_expenditures",
                value,
                period_year,
                f"Annual report 2024 / printed p. 126 (PDF p. 65) / 6.1.4 actual capital expenditures / Total / {period_year}",
            )
    return found


def ingest_tsmc(session, encoder, *, recorded=False, offline=False):
    results = []
    for year, report in REPORTS.items():
        stem = f"tsmc-{year}-annual"
        if recorded:
            content = (ROOT / f"data/fixtures/{stem}-excerpt.json").read_bytes()
            metadata = json.loads((ROOT / f"data/fixtures/{stem}-metadata.json").read_text())
            if hashlib.sha256(content).hexdigest() != metadata["extract_sha256"]:
                raise ValueError("Recorded TSMC excerpt checksum mismatch")
            excerpt = json.loads(content)
            suffix = "json"
        else:
            if offline:
                metadata = json.loads(
                    (settings().storage_root / f"{stem}.metadata.json").read_text()
                )
                content = (settings().storage_root / metadata["filename"]).read_bytes()
                if hashlib.sha256(content).hexdigest() != metadata["sha256"]:
                    raise ValueError("Stored TSMC original checksum mismatch")
            else:
                # One request per fixed, separately published annual report. Never retry a 403.
                with httpx.Client(timeout=40, follow_redirects=False) as client:
                    with client.stream(
                        "GET",
                        report["url"],
                        headers={
                            "User-Agent": "SemiconductorResearchPlatform/0.1 (personal research)"
                        },
                    ) as response:
                        if response.status_code != 200:
                            raise RuntimeError(
                                "TSMC annual report unavailable; no retry or access-control bypass"
                            )
                        content = bytearray()
                        for block in response.iter_bytes():
                            content.extend(block)
                            if len(content) > 20_000_000:
                                raise ValueError("Annual report exceeds size limit")
                        content = bytes(content)
                metadata = {
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "retrieved_at": datetime.now(UTC).isoformat(),
                }
            excerpt, suffix = excerpt_pdf(content, year), "pdf"
        facts = parse_excerpt(excerpt)
        checksum = metadata["original_sha256"] if recorded else metadata["sha256"]
        source_id = f"tsm-cy{year}-{checksum[:16]}"
        if session.get(Source, source_id):
            identities = session.scalars(
                select(Chunk.embedding_id).where(Chunk.source_id == source_id)
            ).all()
            if not identities or any(x != encoder.identifier for x in identities):
                raise ValueError("Existing TSMC chunks require explicit reindexing")
            results.append({"source_id": source_id, "created": False})
            continue
        session.add(
            Source(
                id=source_id,
                company="TSM",
                title=f"TSMC {year} annual report — consolidated financial tables",
                publisher="TSMC",
                url=report["url"],
                publication_date=date.fromisoformat(report["publication_date"]),
                published_at=report["published_at"],
                retrieved_at=datetime.fromisoformat(metadata["retrieved_at"]),
                checksum=checksum,
                stored_checksum=hashlib.sha256(content).hexdigest(),
                storage_key=LocalStorage(settings().storage_root).put(content, suffix),
                document_type="annual_report",
                accession=None,
                accounting_basis=BASIS,
                capture_kind="recorded_primary_source_excerpt"
                if recorded
                else "original_primary_source",
            )
        )
        session.flush()
        chunks = fact_chunks(facts, "TSMC", BASIS)
        vectors = encoder.encode([c["text"] for c in chunks])
        for fact, chunk, vector in zip(facts, chunks, vectors, strict=True):
            fact_id = f"{source_id}:{fact['fiscal_label']}:{fact['metric']}"
            session.add(Fact(id=fact_id, source_id=source_id, company="TSM", **fact))
            session.add(
                Chunk(
                    id=fact_id,
                    source_id=source_id,
                    company="TSM",
                    embedding=vector,
                    embedding_id=encoder.identifier,
                    **chunk,
                )
            )
        session.flush()
        results.append({"source_id": source_id, "created": True})
    return results

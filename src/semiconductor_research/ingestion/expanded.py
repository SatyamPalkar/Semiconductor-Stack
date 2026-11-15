"""Fixed primary releases and an explicitly selected ASML annual-report section.

ASML's release endpoint was restricted. The separately published annual-report
PDF is a different, disclosed source; the restricted route is not retried.
"""

import hashlib
import io
import json
import re
from datetime import UTC, date, datetime, time
from decimal import Decimal
from zoneinfo import ZoneInfo

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader
from sqlalchemy import select

from semiconductor_research.config.settings import ROOT, settings
from semiconductor_research.database.models import Chunk, Fact, Source
from semiconductor_research.documents.chunking import fact_chunks
from semiconductor_research.financials.profiles import PROFILES
from semiconductor_research.storage.local import LocalStorage

REPORTS = {
    "ASML": {
        "stem": "asml-2024-financial",
        "url": "https://ourbrand.asml.com/m/ee9da90a119cc9d/original/2024-Financial-performance-section.pdf",
        "date": "2025-03-05",
        "zone": "Europe/Amsterdam",
        "suffix": "pdf",
        "basis": "US GAAP; consolidated annual report",
        "title": "ASML 2024 annual report — financial performance section",
        "tables": [],
    },
    "MU": {
        "stem": "mu-fy2024",
        "url": "https://investors.micron.com/news/press-release/2024/Micron-Technology-Inc--Reports-Results-for-the-Fourth-Quarter-and-Full-Year-of-Fiscal-2024-09-25-2024/default.aspx",
        "date": "2024-09-25",
        "zone": "America/Boise",
        "suffix": "html",
        "basis": "US GAAP; unaudited earnings release",
        "title": "Micron fourth-quarter and full-year fiscal 2024 financial results",
        "tables": [
            ("CONSOLIDATED STATEMENTS OF OPERATIONS", 4),
            ("CONSOLIDATED STATEMENTS OF CASH FLOWS", 6),
            ("RECONCILIATION OF GAAP TO NON-GAAP MEASURES, Continued", 9),
        ],
    },
    "TXN": {
        "stem": "txn-2024",
        "url": "https://www.ti.com/en-us/about-ti/newsroom/news-releases/2025/2025-01-23-ti-reports-q4-2024-and-2024-financial-results-and-shareholder-returns",
        "date": "2025-01-23",
        "zone": "America/Chicago",
        "suffix": "html",
        "basis": "US GAAP; earnings release",
        "title": "Texas Instruments fourth-quarter and 2024 financial results",
        "tables": [
            ("Consolidated Statements of Income", 3),
            ("Consolidated Statements of Cash Flows", 5),
        ],
    },
    "AMKR": {
        "stem": "amkr-2024",
        "url": "https://ir.amkor.com/news-releases/news-release-details/amkor-technology-reports-financial-results-fourth-quarter-and-10",
        "date": "2025-02-10",
        "zone": "America/Phoenix",
        "suffix": "html",
        "basis": "US GAAP; unaudited earnings release",
        "title": "Amkor fourth-quarter and full-year 2024 financial results",
        "tables": [
            ("CONSOLIDATED STATEMENTS OF INCOME", 4),
            ("CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS", 6),
        ],
    },
}
NUMBER = re.compile(r"\(?\s*\d[\d,]*(?:\.\d+)?\s*\)?")


def numbers(text):
    result = []
    for value in NUMBER.findall(text):
        clean = re.sub(r"\s+|,", "", value)
        result.append(Decimal(clean.strip("()")) * (-1 if clean.startswith("(") else 1))
    return result


def excerpt_original(content, company):
    report = REPORTS[company]
    if company == "ASML":
        reader = PdfReader(io.BytesIO(content))
        return {
            "company": company,
            "income": reader.pages[5].extract_text(),
            "cash": reader.pages[8].extract_text(),
        }
    tables = BeautifulSoup(content, "html.parser").find_all("table")
    selected = []
    for title, index in report["tables"]:
        table = tables[index]
        if title not in table.get_text(" ", strip=True):
            raise ValueError("Financial table identity changed")
        selected.append(str(table))
    return {"company": company, "tables": selected}


def parse_excerpt(data):
    company = data["company"]
    profile = PROFILES[company]
    facts = []
    years = (2024, 2023)

    def add(metric, values, locator, positive=False):
        for year, value in zip(years, values, strict=True):
            end = (
                date(year, 8, 29 if year == 2024 else 31) if company == "MU" else date(year, 12, 31)
            )
            facts.append(
                {
                    "metric": metric,
                    "value": abs(value) if positive else value,
                    "currency": profile.currency,
                    "unit_scale": profile.scale,
                    "period_start": None,
                    "period_end": end,
                    "period_kind": "annual",
                    "fiscal_label": f"{profile.prefix}{year}",
                    "locator": locator + f" / annual {year}",
                    "transformations": {
                        "parser": "expanded-financial-v1",
                        "normalization": "outflow/expense magnitude"
                        if positive
                        else "reported signed amount",
                        "source_scope": "consolidated",
                        "source_unit_scale": profile.scale,
                    },
                }
            )

    if company == "ASML":
        income, cash = data["income"], data["cash"]
        for text in (income, cash):
            if not all(
                s in text for s in ("€, in millions", "2023", "2024", "Year ended December")
            ):
                raise ValueError("ASML annual currency/unit/year header changed")
        if not re.search(
            r"Year ended December\s*31 \(€, in millions\) 2023 % 1 2024 % 1 % Change", income
        ) or not re.search(r"Year ended December\s*31 \(€, in millions\) 2023 2024", cash):
            raise ValueError("ASML annual column order changed")
        for label, metric, positive in [
            ("Total net sales", "revenue", False),
            ("Gross profit", "gross_profit", False),
            ("Research and development (R&D) costs", "research_development", True),
            ("Income from operations", "operating_income", False),
        ]:
            rows = [
                numbers(line[len(label) :])
                for line in income.splitlines()
                if line.startswith(label + " ")
            ]
            rows = [r for r in rows if len(r) == 5]
            if len(rows) != 1:
                raise ValueError(f"ASML income layout changed: {label}")
            add(
                metric,
                [rows[0][2], rows[0][0]],
                f"Annual report 2024 / printed p. 56 (PDF p. 6) / operating results / {label}",
                positive,
            )
        for label, metric, positive in [
            ("Net cash provided by (used in) operating activities", "operating_cash_flow", False),
            (
                "Purchases of property, plant and equipment and intangible assets",
                "capital_purchases",
                True,
            ),
        ]:
            rows = [
                numbers(line[len(label) :])
                for line in cash.splitlines()
                if line.startswith(label + " ")
            ]
            rows = [r for r in rows if len(r) == 2]
            if len(rows) != 1:
                raise ValueError(f"ASML cash layout changed: {label}")
            add(
                metric,
                list(reversed(rows[0])),
                f"Annual report 2024 / printed p. 59 (PDF p. 9) / cash-flow analysis / {label}",
                positive,
            )
        return facts
    tables = [BeautifulSoup(t, "html.parser").find("table") for t in data["tables"]]
    for (title, _), table in zip(REPORTS[company]["tables"], tables, strict=True):
        text = table.get_text(" ", strip=True)
        if not all(
            x in text
            for x in (
                title,
                "2024",
                "2023",
                "Year" if company != "MU" else "year" if "CASH FLOWS" in title else "Year",
            )
        ):
            raise ValueError("Annual statement heading changed")
    for table in tables:
        heading = table.get_text(" ", strip=True)
        required = ("August 29, 2024", "August 31, 2023") if company == "MU" else ("December 31",)
        if not all(text in heading for text in required):
            raise ValueError("Reporting-period header changed")
    first_rows = {
        "MU": (
            "Revenue",
            "Cash flows from operating activities",
            "GAAP net cash provided by operating activities",
        ),
        "TXN": ("Revenue", "Cash flows from operating activities"),
        "AMKR": ("Net sales", "Cash flows from operating activities"),
    }[company]
    for index, table in enumerate(tables):
        header = table.get_text(" ", strip=True).split(first_rows[index])[0]
        if company == "MU":
            periods = re.findall(r"(?:August|May) \d{1,2}, 20\d{2}", header)
            expected = (
                ["August 29, 2024", "August 31, 2023"]
                if index == 1
                else [
                    "August 29, 2024",
                    "May 30, 2024",
                    "August 31, 2023",
                    "August 29, 2024",
                    "August 31, 2023",
                ]
            )
        else:
            periods = re.findall(r"\b20\d{2}\b", header)
            expected = (
                ["2024", "2023"]
                if company == "AMKR" and index == 1
                else ["2024", "2023", "2024", "2023"]
            )
        if periods != expected:
            raise ValueError("Annual column order changed")
    unit = "In thousands" if company == "AMKR" else "In millions"
    if not all(unit in t.get_text(" ", strip=True) for t in tables[:2]):
        raise ValueError("Statement unit changed")

    def row(index, label, count):
        matches = []
        for tr in tables[index].find_all("tr"):
            cells = tr.find_all(["td", "th"], recursive=False)
            if cells and cells[0].get_text(" ", strip=True) == label:
                vals = numbers(" ".join(c.get_text(" ", strip=True) for c in cells[1:]))
                if len(vals) == count:
                    matches.append(vals[-2:])
        if len(matches) != 1:
            raise ValueError(f"Annual row layout changed: {label}")
        return matches[0]

    if company == "MU":
        income_rows = [
            ("Revenue", "revenue"),
            ("Gross margin", "gross_profit"),
            ("Research and development", "research_development"),
            ("Operating income (loss)", "operating_income"),
        ]
        count = 5
    elif company == "TXN":
        income_rows = [
            ("Revenue", "revenue"),
            ("Gross profit", "gross_profit"),
            ("Research and development (R&D)", "research_development"),
            ("Operating profit", "operating_income"),
        ]
        count = 4
    else:
        income_rows = [
            ("Net sales", "revenue"),
            ("Gross profit", "gross_profit"),
            ("Research and development", "research_development"),
            ("Operating income", "operating_income"),
        ]
        count = 4
    for label, metric in income_rows:
        add(metric, row(0, label, count), REPORTS[company]["tables"][0][0] + " / " + label)
    cash_count = 4 if company == "TXN" else 2
    ocf_label = (
        "Cash flows from operating activities"
        if company == "TXN"
        else "Net cash provided by operating activities"
    )
    add(
        "operating_cash_flow",
        row(1, ocf_label, cash_count),
        REPORTS[company]["tables"][1][0] + " / " + ocf_label,
    )
    purchase_label = {
        "MU": "Expenditures for property, plant, and equipment",
        "TXN": "Capital expenditures",
        "AMKR": "Payments for property, plant and equipment",
    }[company]
    add(
        "capital_purchases",
        row(1, purchase_label, cash_count),
        REPORTS[company]["tables"][1][0] + " / " + purchase_label,
        True,
    )
    if company == "MU":
        for label, metric, positive in [
            ("Payments on equipment purchase contracts", "capital_principal", True),
            ("Proceeds from sales of property, plant, and equipment", "capital_asset_sales", False),
            ("Proceeds from government incentives", "capital_grants", False),
        ]:
            add(
                metric, row(2, label, 5), REPORTS[company]["tables"][2][0] + " / " + label, positive
            )
        expected = row(2, "Adjusted free cash flow", 5)
        for year, expected_value in zip(years, expected, strict=True):
            vals = {f["metric"]: f["value"] for f in facts if f["fiscal_label"] == f"FY{year}"}
            actual = (
                vals["operating_cash_flow"]
                - vals["capital_purchases"]
                - vals["capital_principal"]
                + vals["capital_asset_sales"]
                + vals["capital_grants"]
            )
            if actual != expected_value:
                raise ValueError("Micron adjusted free cash flow does not reconcile")
    return facts


def ingest_expanded(session, encoder, *, recorded=False, offline=False):
    results = []
    for company, report in REPORTS.items():
        stem = report["stem"]
        if recorded:
            content = (ROOT / f"data/fixtures/{stem}-excerpt.json").read_bytes()
            metadata = json.loads((ROOT / f"data/fixtures/{stem}-metadata.json").read_text())
            if (
                metadata["original_url"] != report["url"]
                or metadata["publication_date"] != report["date"]
            ):
                raise ValueError("Recorded source identity/date differs from catalog")
            if hashlib.sha256(content).hexdigest() != metadata["extract_sha256"]:
                raise ValueError("Recorded excerpt checksum mismatch")
            excerpt, checksum, suffix = json.loads(content), metadata["original_sha256"], "json"
        else:
            if offline:
                metadata = json.loads(
                    (settings().storage_root / f"{stem}.metadata.json").read_text()
                )
                if metadata["url"] != report["url"]:
                    raise ValueError("Stored source URL differs from fixed catalog")
                content = (settings().storage_root / metadata["filename"]).read_bytes()
                if hashlib.sha256(content).hexdigest() != metadata["sha256"]:
                    raise ValueError("Stored original checksum mismatch")
            else:
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
                                "Source unavailable; no retry or access-control bypass"
                            )
                        payload = bytearray()
                        for block in response.iter_bytes():
                            payload.extend(block)
                            if len(payload) > 10_000_000:
                                raise ValueError("Source exceeds size limit")
                        content = bytes(payload)
                metadata = {
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "retrieved_at": datetime.now(UTC).isoformat(),
                }
            excerpt, checksum, suffix = (
                excerpt_original(content, company),
                metadata["sha256"],
                report["suffix"],
            )
        if excerpt["company"] != company:
            raise ValueError("Recorded company mismatch")
        facts = parse_excerpt(excerpt)
        source_id = f"{company.lower()}-2024-{checksum[:16]}"
        if session.get(Source, source_id):
            identities = session.scalars(
                select(Chunk.embedding_id).where(Chunk.source_id == source_id)
            ).all()
            if not identities or any(x != encoder.identifier for x in identities):
                raise ValueError("Existing chunks require explicit reindexing")
            results.append({"source_id": source_id, "created": False})
            continue
        published = datetime.combine(
            date.fromisoformat(report["date"]), time(23, 59, 59), tzinfo=ZoneInfo(report["zone"])
        ).astimezone(UTC)
        session.add(
            Source(
                id=source_id,
                company=company,
                title=report["title"],
                publisher=PROFILES[company].name,
                url=report["url"],
                publication_date=date.fromisoformat(report["date"]),
                published_at=published,
                retrieved_at=datetime.fromisoformat(metadata["retrieved_at"]),
                checksum=checksum,
                stored_checksum=hashlib.sha256(content).hexdigest(),
                storage_key=LocalStorage(settings().storage_root).put(content, suffix),
                document_type="annual_report" if company == "ASML" else "earnings_release",
                accession=None,
                accounting_basis=report["basis"],
                capture_kind="recorded_primary_source_excerpt"
                if recorded
                else "original_primary_source",
            )
        )
        session.flush()
        chunks = fact_chunks(facts, PROFILES[company].name, report["basis"])
        vectors = encoder.encode([c["text"] for c in chunks])
        for fact, chunk, vector in zip(facts, chunks, vectors, strict=True):
            fact_id = f"{source_id}:{fact['fiscal_label']}:{fact['metric']}"
            session.add(Fact(id=fact_id, source_id=source_id, company=company, **fact))
            session.add(
                Chunk(
                    id=fact_id,
                    source_id=source_id,
                    company=company,
                    embedding=vector,
                    embedding_id=encoder.identifier,
                    **chunk,
                )
            )
        session.flush()
        results.append({"source_id": source_id, "created": True})
    return results

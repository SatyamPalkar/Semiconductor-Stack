# Industry directory and financial expansion

Implemented and verified locally on 15 November 2026. No cloud provisioning, publication, paid data subscription or hosted-model evaluation was performed. Independent human financial and citation-support review remains pending.

## Delivered scope

- **139 companies and operating businesses**, across design/compute, manufacturing, memory, analog/power/embedded, equipment/metrology, EDA/IP, materials/components and packaging/test. Entries can have overlapping roles; they are not necessarily independent issuers or additive revenue pools. This is a curated directory, not an exhaustive census of the industry.
- **36 official research destinations** for market/industry data, company filings, research/learning, standards/interfaces, open design tools and policy/materials. Category, role, access and text filters are implemented. Discovery links are explicitly separate from ingested financial evidence.
- Company search, role selection through an orbital map, actual financial-dataset filtering, 12-entry pagination, profile selection with focus/scroll and a return link. Profiles link to official websites, IR, role-related resources and the correct financial explorer.
- **Six historical financial datasets**, seven original documents, 78 stored annual source observations and 124 available financial metrics. Current directory metadata (2026-11-15) is distinct from the financial evidence cutoff (2025-03-13).
- Two annual cash periods per company in the visual explorer, native-currency revenue and gross-margin charts, signed losses and optional exact calculation/source rows. The existing focused NVIDIA/TSMC investigation and editorial research note remain bounded to that pair.
- Financial tools and bounded cited questions support the six datasets. Named directory-only companies abstain rather than receiving the selected issuer’s numbers. Forecasts, prices, currency conversion and multi-company questions remain outside this router.

## Financial sources added

| Company | Source / stated publication date | Annual ends / native unit | Key source-specific treatment |
| --- | --- | --- | --- |
| ASML | 2024 annual report, financial-performance PDF section; publication announced 2025-03-05 | 2023-12-31, 2024-12-31 / EUR million | PPE **plus intangibles**; printed pp.56/59, PDF pp.6/9 |
| Micron | FY2024 earnings release, 2024-09-25 | 2023-08-31, 2024-08-29 / USD million | Net capital investment includes equipment-contract payments, PPE sales and incentives; adjusted-FCF reconciliation checked |
| Texas Instruments | Q4/full-year 2024 earnings release, 2025-01-23 | 2023-12-31, 2024-12-31 / USD million | Annual columns from income/cash-flow tables, not quarterly columns |
| Amkor | Q4/full-year 2024 earnings release, 2025-02-10 | 2023-12-31, 2024-12-31 / USD thousand | Detailed statements used for an **analytical gross-PPE residual**, not Amkor’s rounded reported-FCF reconciliation |

Fixed source URLs, originals’ SHA-256 hashes, actual retrieval timestamps, selected real tables and excerpt hashes are recorded in `data/fixtures/*-metadata.json`. Downloaded originals remain in ignored `data/raw`. Reproducible setup uses clearly labelled REAL excerpts, distinct from rollback-only synthetic test amendments.

ASML’s earnings-release canonical endpoint returned HTTP 403 and was not retried or bypassed. The explicitly selected alternative is the separately published annual-report financial section on ASML’s brand-asset host. Its March 5 publication date is supported by ASML’s annual-report publication announcement, not inferred from the PDF filename. Earlier TSMC restrictions remain documented. These later-captured sources are not certified point-in-time archives.

Date-only source publication uses conservative publisher-day cutoffs: ASML Europe/Amsterdam (2025-03-05 22:59:59 UTC), Micron America/Boise (2024-09-26 05:59:59 UTC), TI America/Chicago (2025-01-24 05:59:59 UTC), Amkor America/Phoenix (2025-02-11 06:59:59 UTC). Unknown period starts remain null.

Parsers validate statement identity, units, annual column order and reported period headers. Negative income/gross profit remains negative. Every configured capital offset is required; absence never becomes zero. All financial arithmetic uses Decimal and rejects incompatible units/bases. CY labels identify the December-31-ended annual observations and do not align NVIDIA or Micron to a different calendar.

## Numerical oracles executed

| Result | Verified value and scope |
| --- | --- |
| ASML CY2024 FCF | `11,166.2 − 2,083.1 = 9,083.1` EUR million |
| Micron FY2024 adjusted FCF | `8,507 − 8,386 − 149 + 99 + 315 = 386` USD million, five cited inputs |
| Micron FY2023 gross margin / adjusted FCF | `−9.1120%` / `−5,453` USD million; negative visual axis and cash display retained |
| TI CY2024 FCF | `6,318 − 4,820 = 1,498` USD million |
| Amkor CY2024 analytical gross-PPE residual | `1,088,868 − 743,796 = 345,072` USD thousand; explicitly not reported Amkor FCF |

Existing NVIDIA/TSMC oracles and cash-investigation behavior continue to pass. Ratios do not harmonize cash-flow scope, reporting periods or accounting frameworks and are not an investment ranking. ROIC, DCF, forecasts and full-cycle analysis are not implemented by this expansion.

## Directory link observations

The catalog’s **245 unique current URLs** have observations: 170 responded, 53 redirected, 17 restricted, three could not be confirmed and two deliberately not requested. No current URL had a recorded 404/410 after corrections. Redirect targets were not automatically followed. These are HTTP observations, not content, licensing or future-availability certification.

Each request is bounded to one fixed catalog URL, 12 seconds and 256 KiB; no login, payment, retry or access-control bypass. SEC is skipped without a declared contact identity; the previously restricted TSMC IR host is skipped. Stale URLs and an unrelated similarly named Qnity site were corrected to the official destinations before export. Checked-in observations are filtered to current approved catalog URLs; page contents and diagnostic details do not enter the browser export.

## Executed verification

- `UV_NO_SYNC=1 make lint`: Ruff checks/format and TypeScript passed.
- `UV_NO_SYNC=1 make test`: **56 passed**.
- `UV_NO_SYNC=1 make integration`: **29 passed**, including all four sources’ idempotence, exact citations, native units, publication cutoffs, missing offsets, uncovered-company abstention and actual directory coverage.
- `UV_NO_SYNC=1 make evaluate`: **21/21 passed**, no hosted-model calls. This remains the original NVIDIA development dataset; it does not score general industry reasoning or the new datasets’ research merit.
- `UV_NO_SYNC=1 make snapshot` and `make build`: database export and static production build passed.
- `UV_NO_SYNC=1 make e2e`: **19 passed**; final production-export browser results are recorded in `evaluations/results/browser-summary.json`. Coverage includes atlas/profile/pagination/coverage/empty states; resource access/role/search filters; expanded company selectors; EUR formatting; negative Micron values and prior-year cash; analytical Amkor labels; exact cited answers; offline behavior; source-date withholding; keyboard controls; and seven routes at 1440/768/393px without page overflow or browser errors.
- ASML printed pp.56/59 were rendered from the downloaded PDF and visually inspected. Desktop/mobile atlas and financial screenshots were inspected after production builds. Screenshots and original PDFs remain ignored local artifacts, not frontend exports.

## Review locally

- Atlas: http://127.0.0.1:3100/value-chain/
- Research resources / ingested evidence: http://127.0.0.1:3100/sources/
- Six-company finance explorer: http://127.0.0.1:3100/industry-economics/
- Bounded evidence desk: http://127.0.0.1:3100/assistant/
- API docs: http://127.0.0.1:8100/docs

The retained static preview serves `apps/web/out` on loopback 3100; FastAPI is on loopback 8100. Current process stop commands: `kill 54834` (preview), `kill 65736` (API), or Ctrl+C in their originating terminals. Restart with `make preview` and `make api`. Stop the project-owned native database with `make native-down`. The user’s existing database on 5432 was not changed.

Clean setup now includes `make ingest-expanded` after NVIDIA/TSMC ingestion. `uv run semi ingest-expanded --offline` verifies downloaded originals; `make ingest-expanded-live` requests only the four fixed official source URLs, once each. The optional directory checker supports `--only-new` to retain prior observations and avoid rechecking restricted links.

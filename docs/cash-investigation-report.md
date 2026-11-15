# NVIDIA–TSMC cash investigation — 15 November 2026

This local follow-on turns the research foundation into a focused investigation: how NVIDIA and TSMC turn revenue into operating cash, and what remains after their disclosed capital outlays. The finding is descriptive, with explicit counterevidence and limits. It is not a stock recommendation, harmonized FCF ranking or full-cycle study.

## Implemented

- TSMC’s separately published 2023/2024 annual-report PDFs returned HTTP 200 and were preserved with SHA-256 originals in ignored local storage. Earlier IR HTTP 403 failures remain documented; no proxy, alternate identity or access-control bypass was used. Selected REAL table excerpts and metadata support reproducible setup without redistributing the original reports.
- PostgreSQL now holds 24 source observations from three documents: NVIDIA’s FY2025 release and the two TSMC reports. Native USD millions, TWD thousands, reporting labels, date cutoffs, row locators and source versions are preserved.
- The financial engine supports company-specific cash definitions, operating-cash-flow margin and disclosed capital spending / operating cash. `/api/investigation` and the static export use the same calculation boundary. Missing inputs and incompatible units remain unavailable.
- The overview leads with the investigation. Company comparison switches between FY2025/CY2024 and FY2024/CY2023; every displayed result exposes the definition and exact source inputs. Detailed rows adapt to phone screens. Company charts and methodology definitions can be switched between NVIDIA and TSMC.
- The substantive research note includes supporting observations, counterevidence, alternative explanations and conditions that could change the interpretation. Both figures and dependent comparative prose are withheld before required source dates. The selected research date persists across page navigation within the browser tab.
- The evidence desk supports bounded annual questions for either company, with correct calendars, native units and source titles. Company mismatches, unsupported calendar alignment and explicit unsupported FX requests abstain. Offline examples remain labelled; general comparative conversation is not implemented.

## Finding and boundaries

For NVIDIA FY2025, operating cash / revenue is 49.1115% and release-defined FCF / revenue is 46.5329%. For TSMC CY2024, operating cash / revenue is 63.0955%; operating cash less annual-report capital expenditures / revenue is 30.0649%. Thus the operating-cash and cash-after-investment comparisons point in different directions. Those are calculations from the selected source rows, not independently reviewed financial conclusions.

NVIDIA deducts PPE/intangible purchases and related principal payments in its release-defined FCF. TSMC’s analytical residual deducts the annual report’s capital-expenditure total; other investing and financing flows are excluded. These scopes are not harmonized. Different fiscal ends and accounting frameworks remain visible. Ratios do not remove exchange-rate exposure or classification differences. Purchased manufacturing services can contain investment costs that do not appear in a buyer’s own capex; that is an interpretation to investigate, not a causal result established by these rows.

The 2024 TSMC report provides consolidated income figures on printed p.124 / PDF p.64 and operating cash/capital expenditure tables on printed p.126 / PDF p.65. The 2023 report supplies consolidated operating cash on printed p.132 / PDF p.68. TSMC source dates use the printed cover dates (12 March 2024/2025), conservatively at end of Taipei day. These later-captured files are not independently certified historical archives.

## Executed verification

- `UV_NO_SYNC=1 make lint test`: Ruff checks, formatting, TypeScript and **37 unit tests passed**.
- `RUN_DB_TESTS=1 .venv/bin/python -m pytest tests/integration -q`: **22 integration tests passed** against the project PostgreSQL/pgvector database, including rollback-controlled synthetic cases. New coverage checks TSMC ingestion idempotence, report-date exclusion, exact source resolution, native currency/calendar answers, company mismatches and unsupported FX/calendar requests.
- `UV_NO_SYNC=1 make evaluate snapshot`: **21/21 original NVIDIA development cases passed**, zero hosted-model calls; database export completed. This remains a draft NVIDIA regression dataset, not an evaluation score for the new research interpretation or TSMC financial review.
- `UV_NO_SYNC=1 make build`: production static export passed. The sandbox initially prevented Turbopack’s local compiler port; moving the failed generated cache into ignored `.cache/` and building with the required process permissions resolved it. No development server ran in the build directory.
- `UV_NO_SYNC=1 make e2e`: **14 browser workflows passed** against the production export and real local API. All seven routes were checked at 1440, 768 and 393 pixels without page overflow or browser page errors. Expanded source rows, company definitions, offline examples and earlier-date withholding were checked. See `evaluations/results/browser-summary.json`.
- TSMC report tables and final comparison screenshots were visually inspected by the coding agent. This is not independent human review. Images remain in ignored `data/interim/`.
- The static export was checked to exclude original PDFs, model weights, databases, secret files and local storage keys. Synthetic source records are rejected by the existing snapshot guard. `git diff --check` passed.

## Run and review

Use `make ingest-tsmc` for the hash-verified recorded REAL excerpts. `make ingest-tsmc-live` requests only the two fixed public annual-report URLs; a 403 fails closed without retries. For this workspace’s already downloaded originals, `uv run semi ingest-tsmc --offline` verifies and parses them.

After local setup, run `make api` and `make preview`. The production preview is `http://127.0.0.1:3100`, comparison at `/companies/`, note at `/briefs/`, and API docs at `http://127.0.0.1:8100/docs`. Stop foreground servers with Ctrl+C. Stop only this project’s database using `make native-down` or `make db-stop` for the selected profile. This work leaves the useful local preview running; it does not deploy or provision anything.

## Remaining review and research

Independent human financial mapping, citation-support and interpretation review remain pending. The history is two annual observations per company, not a complete cycle. Full cash-flow classification, lease/intangible scope and supplier commitment reconciliation are still needed before a standardized comparison. No general conversational research router, LangGraph workflow, live hosted-model evaluation, cloud deployment, valuation, backtest or trading capability is claimed.

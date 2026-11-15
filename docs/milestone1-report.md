# Milestone 1 verification — 15 November 2026

## Working

A real NVIDIA FY2025 results document was ingested with original bytes/checksums and row-level provenance. PostgreSQL 17/pgvector holds 14 annual reported observations and 14 normalized financial-row vectors. Decimal financial tools expose traceable inputs, units, definitions, fiscal labels and as-of dates. The seven-page Next.js/Plotly interface builds as a static export and remains useful offline. The FastAPI sources, company, metric, question and health endpoints run locally. No hosted model is required for financial-tool or extractive answers.

## Executed verification

- 41 pytest tests passed, including real isolated PostgreSQL/pgvector integration and API contracts.
- 8 Playwright workflows passed against the production static export with an isolated Chrome profile; mobile and API-offline behavior included. See `evaluations/results/browser-summary.json`.
- 20/20 versioned development cases passed. See `evaluations/results/milestone1.json` for dataset/pipeline checksums, model identity, latency and actual usage. Human review is pending.
- Ruff lint/format checks, TypeScript checks, uv lock consistency and Next static production build passed.
- Final local HTTP smoke checks: healthy API, cited FCF calculation, conflicting fiscal-year/filter abstention, whitespace rejection (422) and reachable static preview.
- Native startup is idempotent. It uses this project's separate database on 55432 and leaves the existing service on 5432 alone.

## Limits and unexecuted work

TSMC source access returned HTTP 403, so peer financial comparisons are unavailable. Financial period starts not independently reported by the selected release remain null. The source page was captured later than its stated publication date; this is not a certified point-in-time archive. Human financial/citation review, real hosted-model evaluation, Docker execution on this Mac and GitHub Actions execution have not occurred. The optional Groq adapter has mocked schema/citation tests only. The API is a local prototype, not ready for public exposure. No LangGraph agent, DCF, backtest, trade execution or AWS infrastructure was implemented/provisioned.

## Run

The current local interface is `http://127.0.0.1:3100`; API docs are `http://127.0.0.1:8100/docs`. Start with `make api` and `make preview` after the README setup commands. `make web` is the alternative development UI; stop it before rebuilding. Use `make native-down` (or `make db-stop` for Docker) to stop the project database. Stop foreground web/API processes with Ctrl+C.

## Next milestone

Obtain a permitted TSMC source, validate cross-company calendars/units/definitions and human-review the important financial answers. Broaden retrieval and evaluation before implementing a bounded LangGraph workflow with PostgreSQL checkpoints, idempotent jobs, cancellation/retry/timeout policies and token/cost/demo budgets. Costed AWS stacks and deployment require a later explicit request.

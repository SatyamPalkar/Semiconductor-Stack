# Semiconductor Research Platform

**Milestone 1: a working local research foundation.** The interface is branded **semiscope**. It connects official NVIDIA financial tables to PostgreSQL facts, Decimal calculations, hybrid keyword/vector retrieval, cited answers and a statically exportable research site.

The historical pilot covers **NVIDIA FY2024 and FY2025**, not today's market. Six companies are in scope; TSMC financial ingestion is pending after its public source returned HTTP 403. No substitute estimates are shown. LangGraph research agents, AWS, DCF and trading are outside this first milestone.

## What works

- One actual official NVIDIA FY2025 earnings-release HTML ingested with original bytes preserved locally, hashes and row-level provenance.
- 14 annual reported observations; nine metric definitions, including missing prior-growth handling and NVIDIA's release-defined FCF.
- PostgreSQL 17 with pgvector, SQLAlchemy and three Alembic migrations (with a guarded downgrade where source metadata is unknown).
- Pinned 384-dimensional MiniLM CPU embeddings plus PostgreSQL full-text search and reciprocal rank fusion. Company, publication/as-of, period, document type and topic filters.
- Deterministic financial tools; extractive source answers without API credentials. An optional Groq JSON adapter is implemented but no real hosted-model evaluation was run.
- Seven Next.js pages, Plotly charts, source inspection, as-of filtering, calculation citations, offline examples and honest unavailable states.
- A static PostgreSQL export remains useful with the API offline. Recorded examples are calculations from real reported data, not fabricated model outputs.

## Prerequisites and clean setup

Python 3.12 (uv can install it), uv, Node >=20.9, npm, Docker with Compose. The browser tests use installed Google Chrome; alternatively install Playwright's Chrome channel in your development environment.

```bash
cp .env.example .env
make setup
make db-up
make migrate
make model
make ingest             # recorded REAL primary-source excerpt, no data API key
make evaluate
make snapshot
make build
```

Then use two terminals:

```bash
make api                # http://127.0.0.1:8100/docs
make preview            # http://127.0.0.1:3100 — actual static production export
```

`make web` replaces the static preview with a development server on the same port. Stop that server before `make build`. There is no cloud resource, public tunnel or AWS deployment in this milestone.

### This Mac's verified native alternative

Docker is not installed. Verification used the existing Homebrew PostgreSQL 17.10 binaries and the official pgvector v0.8.1 extension in a **separate project-owned cluster on 55432**. The existing service on 5432 was left alone. pgvector was compiled from the official tagged source; it must be available for your PostgreSQL version before native startup.

```bash
make native-up
# Set this DATABASE_URL in the ignored .env (instead of the Docker URL):
# postgresql+psycopg://semi_local@/semiconductor?host=/tmp&port=55432
make migrate
make model
make ingest
```

The native socket uses local trust for this isolated public-data development cluster. TCP is loopback-only and uses SCRAM authentication; no public database endpoint is created. Use the Docker credentials from the example only for local Docker development. Stop native PostgreSQL with `make native-down`; stop Docker with `make db-stop`. Neither command destroys data. The Docker path is supplied and checked against the same schema, but Docker execution was not verified on this Mac.

## Verify

```bash
make lint
make test
make integration
make evaluate
make snapshot
make build
# With API and preview running:
make e2e
```

See [the milestone verification report](docs/milestone1-report.md) and [the executed development results](evaluations/results/milestone1.json). These checks verify calculations, source resolution, scope/as-of handling and abstention. Important finance answers still need independent human review; no LLM judge or investment-performance result is reported. Pytest also verifies amendments, conflicts, units, missing values and injected instructions. See [evaluation methodology](docs/evaluation-plan.md).

## Try it

- “What was NVIDIA free cash flow in FY2025?” → 60,724 USD million, with three source inputs.
- “What was NVIDIA gross margin in FY2025?” → 74.9887%, calculated from 97,858 / 130,497.
- “What was reported research and development expense?” → filtered, cited stored evidence.
- “What is NVIDIA stock price today?” → an explicit limitation.
- Change the research date to 2025-02-25 → the later results are withheld.

The release rounds gross margin to 75.0%; recomputing from rounded million-dollar source inputs yields 74.9887%. Both the scale and calculation are visible; they are not claimed to be more precise than the source.

## Live source and model configuration

`make ingest-live` makes one request to the fixed NVIDIA catalog URL, preserves immutable original bytes and records a new checksum version. It does not request SEC data. Configure a declared `SEC_USER_AGENT` before implementing SEC ingestion; the code does not send a fake identity to EDGAR.

For optional Groq generation, set `GROQ_API_KEY`, a currently supported `LLM_MODEL`, `LLM_PROVIDER=groq` and `ENABLE_LIVE_LLM=true` only in server-side `.env`. Restart the API and deliberately enable the hosted-model toggle in the assistant. Evidence and the question are sent to Groq. Financial calculations continue to use Python. Calls have a 25-second timeout, one request, at most 600 output tokens and a bounded evidence context. No automatic retries. The adapter has mocked schema/citation rejection tests; real model support/quality and pricing require a separately controlled live evaluation. It is a local prototype without authentication, durable quotas or production spending enforcement. Never expose this API publicly as-is.

The embedding model is pinned in `documents/embedding.py`, verified by artifact hashes, local-only at query time and distinct from generation. Its dimensions/identifier are stored alongside vectors. Adding another embedding provider requires explicit dimension/version validation and reindexing.

## Documents

- [Project brief](docs/project-brief.md) · [Implementation plan](docs/implementation-plan.md)
- [Architecture](docs/architecture.md) · [Methodology](docs/methodology.md)
- [Metric definitions](docs/metric-definitions.md) · [Data dictionary](docs/data-dictionary.md)
- [Evaluation plan](docs/evaluation-plan.md) · [Local deployment and teardown](docs/deployment.md)

Next milestone: obtain permitted TSMC source data, review the financial mappings with a human, broaden the retrieval set, then implement the bounded LangGraph research workflow with PostgreSQL checkpoints and run budgets. Only after local validation should AWS costed infrastructure be prepared and deployment explicitly requested.

# Semiconductor Research Platform

Implement the user's brief in `docs/project-brief.md` in complete, verified local milestones.
Do not provision cloud resources, deploy, publish or execute live paid-model evaluations without an explicit deployment/evaluation request.
The parent workspace publication guardrail also applies. Keep `.env`, model weights, original documents, local databases, caches and private artifacts out of Git and frontend exports.

## Established commands

- Python 3.12 and uv. `make setup` installs locked Python and web dependencies.
- `make db-up` starts the loopback-only Docker PostgreSQL/pgvector service on 55432. Docker is a prerequisite, not installed on the development Mac.
- Native Mac alternative: `make native-up` uses existing PostgreSQL 17 + pgvector binaries; set the documented socket URL in ignored `.env`. It owns a separate `data/native-postgres` cluster. Never change the user's database on 5432.
- `make migrate` applies Alembic migrations. `make model` prepares hash-verified MiniLM ONNX assets.
- `make ingest` ingests the clearly labelled recorded primary-source table excerpt. `make ingest-live` requests only the fixed official NVIDIA URL.
- `make api`: loopback FastAPI on 8100. `make web`: Next dev on 3100. `make preview`: built static export on 3100.
- `make lint`: Ruff and TypeScript. `make test`: unit tests. `make integration`: isolated PostgreSQL tests. `make evaluate`: versioned development evaluation. `make snapshot`: PostgreSQL export. `make build`: Next static export. `make e2e`: explicit Playwright/Chrome browser workflows; start API and preview first.
- `make verify` performs non-browser checks, evaluation, snapshot export and production build. `make e2e` is separate.
- The uv cache and managed Python installation live inside ignored project directories so commands work in this workspace's filesystem sandbox.

## Data and correctness

Financial facts are authoritative in PostgreSQL. Calculations use Decimal; absence is never zero. Preserve original scale, currency, reporting kind, fiscal label, period end, source version, publication/availability dates and row locator. NVIDIA FCF includes purchases AND principal payments related to property/equipment/intangibles. Capex includes intangibles and is not a PPE-only cross-company metric.

A date-only publication uses a conservative end-of-publisher-day availability cutoff. `publication_date` is the source's stated date; `published_at` is the conservative availability timestamp. Never describe the later-captured unversioned IR page as a certified historical archive. Do not claim point-in-time backtesting readiness.

Keep recorded REAL source excerpts distinct from synthetic test inputs. Synthetic amendment/conflict records are inserted only in rollback-controlled tests and never exported. Do not silently replace blocked sources or bypass source access controls. TSMC ingestion is pending after HTTP 403.

Model output schemas and citation IDs provide structural validation, not proof of entailment. Extractive answers and recorded examples must remain labelled. Live LLM use is opt-in, server-side only; no arbitrary SQL, shell or URLs become model tools. The pilot's bounded vocabulary can abstain on paraphrases; don't claim a general conversational router.

## Scope and quality

Milestone 1 does not implement the LangGraph thesis workflow, worker execution, AWS, valuation or trading. Don't create empty framework directories or suggest their presence means those capabilities work. Full agent budgets, checkpoints and retries belong to the next workflow milestone.

Record only executed tests/evaluations. Human review remains pending until a human actually performs it. New checks must protect meaningful behavior rather than mirror implementation.

Read `apps/web/AGENTS.md` and the installed Next docs for relevant changes. Use existing API/schema boundaries. Stop the dev server before running a build in the same `.next` directory. Preserve useful local previews for user review; document stop commands.

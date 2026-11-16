# Semiconductor Research Platform

**An application-led semiconductor atlas: nine real-world application areas, 139 companies and businesses, 36 research resources and six historical financial datasets.** The interface is branded **semiscope**. It connects official financial tables to PostgreSQL facts, Decimal calculations, hybrid retrieval, cited answers and a static research site.

The directory is a curated discovery catalog, not an exhaustive census. Financial coverage is historical: NVIDIA FY2024/FY2025, Micron FY2023/FY2024, and TSMC, ASML, Texas Instruments and Amkor CY2023/CY2024. Directory metadata is dated separately from the financial evidence cutoff. Native currencies, units, period ends and company-specific cash definitions remain visible. Independent human financial/citation review is pending.

## What works

- Thirteen detailed, AI-generated 3D-style studio renders across application and semiconductor business scenes, with local responsive WebP assets and accessible task controls. [Visual system and prompts](docs/studio-3d-report.md).

- Nine application worlds, with deeper AI, EV and smart-infrastructure stories. Click a system task to connect chip functions, categories, cited company capabilities and economic questions. A separate geography lens distinguishes selected operating sites from headquarters context.

- An application-led visual story: real-world systems → illustrated business models → the cash investigation → Micron’s changing annual picture → next research questions. Chapter navigation, studio-rendered conceptual scenes, guided controls and page-to-page continuation links keep the reading connected; motion respects reduced-motion preferences.

- An eight-role orbital atlas, searchable company profiles, official website/IR links, financial-coverage filtering and pagination.
- A resource library for industry data, filings, research, standards, open tools and policy; discovery destinations are separate from ingested evidence.
- Seven original primary-source documents preserved locally and 78 selected annual source observations. 124 available derived/reporting metrics across the selected periods, with exact inputs and source locators.
- Six-company financial exploration: two annual cash periods, per-100-revenue cash visuals, native-currency charts, negative margins and optional source calculations. ASML uses EUR millions; Amkor uses USD thousands; NVIDIA, Micron and TI use USD millions; TSMC uses TWD thousands.
- A focused NVIDIA/TSMC visual investigation with three chapters, two annual pairs, source inspection and a research note containing counterevidence and invalidation conditions.
- A bounded six-company evidence desk. Financial questions use deterministic tools; unsupported companies, forecasts and cross-company questions abstain. Extractive answers and offline examples remain labelled.
- PostgreSQL 17/pgvector, SQLAlchemy and three Alembic migrations. Pinned local MiniLM embeddings, full-text search and reciprocal rank fusion. Eight Next.js pages remain usable with the API offline.

The LangGraph workflow, AWS, DCF and trading are outside this local milestone. A Groq JSON adapter is optional; no live hosted-model evaluation has been run.

## Prerequisites and clean setup

Python 3.12 (uv can install it), uv, Node >=20.9, npm, Docker with Compose. The browser tests use installed Google Chrome; alternatively install Playwright's Chrome channel in your development environment.

```bash
cp .env.example .env
make setup
make db-up
make migrate
make model
make ingest             # recorded REAL NVIDIA table excerpt
make ingest-tsmc        # recorded REAL TSMC annual-report table excerpts
make ingest-expanded    # recorded REAL ASML, Micron, TI and Amkor excerpts
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
make ingest-tsmc
make ingest-expanded
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

See [the application-worlds report](docs/application-worlds-report.md), [the storytelling update report](docs/storytelling-report.md), [the directory and financial expansion report](docs/industry-expansion-report.md), [the visual-conclusions report](docs/visual-conclusions-report.md), [the cash-investigation report](docs/cash-investigation-report.md), [the original milestone verification report](docs/milestone1-report.md) and [the executed development results](evaluations/results/milestone1.json). These checks verify calculations, source resolution, scope/as-of handling and abstention. Important finance answers still need independent human review; no LLM judge or investment-performance result is reported. Pytest also verifies amendments, conflicts, units, missing values and injected instructions. See [evaluation methodology](docs/evaluation-plan.md).

## Try it

- Start at `/applications/`: choose AI, a vehicle, infrastructure, robotics, aviation, engineering design, energy, healthcare or connected devices. Filter by compute, sense, communicate, control or power.
- Try `/applications/?world=smart-infrastructure` for sensing, connectivity, building control and digital design. Company links are cited portfolio examples, not named supplier contracts or application revenue.

- Open `/value-chain/` for the company atlas and `/sources/` for the resource library.
- In `/industry-economics/`, select any of the six companies and switch annual cash periods. Micron FY2023 retains its negative cash residual and gross margin.
- Select Micron in the evidence desk: “What was Micron free cash flow in FY2024?” → 386 USD million, with all five inputs.
- Select ASML to see EUR amounts; Amkor cash results are explicitly analytical gross-PPE residuals, separate from its reported FCF.

- “What was NVIDIA free cash flow in FY2025?” → 60,724 USD million, with three source inputs.
- “What was NVIDIA gross margin in FY2025?” → 74.9887%, calculated from 97,858 / 130,497.
- “What was reported research and development expense?” → filtered, cited stored evidence.
- “What is NVIDIA stock price today?” → an explicit limitation.
- Switch the comparison between NVIDIA FY2025 / TSMC CY2024 and NVIDIA FY2024 / TSMC CY2023.
- Select TSMC in the evidence desk: “What was TSMC free cash flow in CY2024?” → an explicitly qualified analytical cash residual in TWD thousands.
- Change the research date to 2025-03-11 → TSMC CY2024 figures and comparative findings are withheld. Earlier source records may remain visible.

The release rounds gross margin to 75.0%; recomputing from rounded million-dollar source inputs yields 74.9887%. Both the scale and calculation are visible; they are not claimed to be more precise than the source.

## Live source and model configuration

`make ingest-expanded` uses hash-verified REAL recorded excerpts. `uv run semi ingest-expanded --offline` verifies downloaded originals; `make ingest-expanded-live` requests only the four fixed official source URLs with bounded downloads and no retries. ASML’s restricted earnings-release route is not retried: its separately published 2024 annual-report financial section is the documented selected source. See the expansion report for dates and definitions.

The directory uses validated public HTTPS destinations and checked-in link observations, not retrieval evidence. To check only newly listed URLs once: `.venv/bin/python scripts/check_directory_links.py --only-new --output data/catalog/directory-links.json`. Restricted responses are retained without retry. HTTP status does not certify content, licensing or future availability.

`make ingest-tsmc-live` requests only the two fixed, separately published annual-report PDF URLs, once each with size limits and no retries. A 403 fails closed. `uv run semi ingest-tsmc --offline` verifies and parses the downloaded originals; `make ingest-tsmc` uses hash-verified recorded REAL excerpts for reproducible setup. The PDFs stay in ignored local storage. TSMC source dates use the printed report dates with an end-of-Taipei-day cutoff; historical availability is not independently certified.

`make ingest-live` makes one request to the fixed NVIDIA catalog URL, preserves immutable original bytes and records a new checksum version. It does not request SEC data. Configure a declared `SEC_USER_AGENT` before implementing SEC ingestion; the code does not send a fake identity to EDGAR.

For optional Groq generation, set `GROQ_API_KEY`, a currently supported `LLM_MODEL`, `LLM_PROVIDER=groq` and `ENABLE_LIVE_LLM=true` only in server-side `.env`. Restart the API and deliberately enable the hosted-model toggle in the assistant. Evidence and the question are sent to Groq. Financial calculations continue to use Python. Calls have a 25-second timeout, one request, at most 600 output tokens and a bounded evidence context. No automatic retries. The adapter has mocked schema/citation rejection tests; real model support/quality and pricing require a separately controlled live evaluation. It is a local prototype without authentication, durable quotas or production spending enforcement. Never expose this API publicly as-is.

The embedding model is pinned in `documents/embedding.py`, verified by artifact hashes, local-only at query time and distinct from generation. Its dimensions/identifier are stored alongside vectors. Adding another embedding provider requires explicit dimension/version validation and reindexing.

## Documents

- [Project brief](docs/project-brief.md) · [Implementation plan](docs/implementation-plan.md)
- [Architecture](docs/architecture.md) · [Methodology](docs/methodology.md)
- [Interface concept: The Silicon Atlas](docs/design-direction.md)
- [Metric definitions](docs/metric-definitions.md) · [Data dictionary](docs/data-dictionary.md)
- [Evaluation plan](docs/evaluation-plan.md) · [Local deployment and teardown](docs/deployment.md)

Next milestone: independently review all six companies’ financial mappings and citation support, reconcile cash-flow classifications and capital-spending scope, extend the history through a cycle, then implement the bounded LangGraph research workflow with PostgreSQL checkpoints and run budgets. Only after local validation should AWS costed infrastructure be prepared and deployment explicitly requested.

## License and source attribution

Project code uses the repository’s MIT license. Bundled fonts retain their SIL Open Font Licenses in `apps/web/app/fonts`. Recorded financial fixtures contain selected public statement tables with publisher URLs, original/excerpt checksums and row/page attribution; they do not include the complete downloaded documents. Company names and third-party materials retain their respective ownership.

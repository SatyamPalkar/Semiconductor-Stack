Build a portfolio project called “Semiconductor Research Platform”.

PROJECT PURPOSE

Create an evidence-backed semiconductor industry research platform
with:
1. An industry deep dive and financial comparisons.
2. A retrieval-backed assistant that answers questions with citations.
3. A controlled agent workflow that develops and challenges investment
   theses and scenarios.
4. Reproducible, on-demand AWS deployment.

This is a personal portfolio and AWS learning project. There are no
existing users and no expected commercial traffic.

Prioritise correctness, explainability, evaluation and reproducibility.
Keep infrastructure inexpensive and removable.

Start by inspecting the repository and reading any existing AGENTS.md.
Then create a concise implementation plan and implement the first
working milestone. Do not stop after producing a plan.

RESEARCH SCOPE

Central question:
“Where is economic value created and captured in the semiconductor
industry, and how could that change?”

Cover:
- Industry structure and value chain.
- Major players and business models.
- Demand drivers and semiconductor cycles.
- Competition and competitive advantages.
- Capital intensity, margins, cash flow and returns on capital.
- Geographic concentration and regulation.
- AI computing as a focused case study.

Initial companies:
- NVIDIA
- TSMC
- ASML
- Micron
- Texas Instruments
- Amkor

Begin financial extraction with NVIDIA and TSMC as a pilot.
Do not assume companies have comparable reporting calendars,
currencies, accounting standards or segment definitions.

Later extensions:
- Three-statement financial model and DCF for one selected company.
- Stock pitch based on the industry research and valuation.
Do not implement these extensions in the first release.

TECHNOLOGY

Local development:
- Python 3.12 and uv.
- FastAPI and Pydantic.
- PostgreSQL with pgvector in Docker Compose.
- SQLAlchemy and Alembic.
- Next.js, TypeScript and Tailwind CSS.
- Plotly for financial charts.
- LangGraph for the controlled research workflow.
- One hosted LLM provider and one embedding model, configurable
  through environment variables.
- pytest for meaningful backend tests.
- Playwright for essential browser workflows.
- Ruff and TypeScript checks.

Keep the database authoritative for financial facts.
Use notebooks for exploration, not as the production pipeline.

ARCHITECTURE

Separate:
1. Source ingestion and provenance.
2. Document extraction and indexing.
3. Financial normalisation and calculation.
4. Retrieval.
5. LLM question answering.
6. Research workflow orchestration.
7. API and presentation.
8. Deployment and operational controls.

Define replaceable interfaces for:
- Document storage: local filesystem / S3.
- Research job execution: local runner / Fargate.
- Model and embedding providers.
- Database connections.

Keep interfaces small. Do not build a general-purpose agent framework.

REPOSITORY STRUCTURE

/
├── AGENTS.md
├── README.md
├── Makefile
├── .env.example
├── .gitignore
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── apps/
│   ├── api/
│   ├── worker/
│   └── web/
├── src/
│   └── semiconductor_research/
│       ├── config/
│       ├── database/
│       ├── sources/
│       ├── ingestion/
│       ├── documents/
│       ├── financials/
│       ├── retrieval/
│       ├── llm/
│       ├── workflows/
│       ├── storage/
│       └── evaluation/
├── migrations/
├── research/
│   ├── industry/
│   ├── companies/
│   ├── hypotheses/
│   └── sources/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── fixtures/
├── notebooks/
├── evaluations/
│   ├── datasets/
│   ├── rubrics/
│   └── results/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── infra/
│   └── terraform/
│       ├── bootstrap/
│       ├── showcase/
│       └── demo/
├── scripts/
├── docs/
│   ├── project-brief.md
│   ├── architecture.md
│   ├── methodology.md
│   ├── metric-definitions.md
│   ├── data-dictionary.md
│   ├── evaluation-plan.md
│   ├── cost-model.md
│   ├── deployment.md
│   ├── teardown.md
│   └── decisions/
├── deliverables/
└── .github/
    └── workflows/

Create files and directories as needed for implemented milestones.
Do not populate the repository with empty placeholders.

DATA AND PROVENANCE

Prefer primary sources:
- SEC EDGAR submissions and Company Facts APIs.
- Company annual reports and investor-relations materials.
- Public industry releases with appropriate reuse permissions.
- Official government sources for regulatory claims.

Follow source access policies and rate limits.
Use a declared SEC User-Agent supplied through configuration.

Store source metadata:
- Source ID and URL.
- Publisher and document title.
- Publication date and retrieval timestamp.
- Filing accession where applicable.
- Reporting period and financial-year label.
- Currency, units and accounting basis.
- Document checksum.
- Page, section, table or XBRL reference.

Preserve original source files.
Record transformations and adjustments.

Distinguish:
- Reported facts.
- Calculated metrics.
- Management guidance.
- Analyst assumptions.
- Research interpretations.

Never fabricate missing data.
Label synthetic fixtures clearly and keep them out of published findings.

FINANCIAL ENGINE

Implement deterministic Python calculations.

Start with:
- Revenue growth.
- Gross margin.
- Operating margin.
- Capital expenditure / revenue.
- R&D / revenue where disclosed.
- Operating cash flow.
- Free cash flow.
- Free cash flow margin.

Add ROIC and inventory metrics only after documenting their definitions
and validating required inputs.

Handle:
- Fiscal-year differences.
- Annual versus quarterly observations.
- Currency and unit differences.
- Duplicate and amended filings.
- Restatements and source selection.
- Missing values.
- Sign conventions.

Do not silently convert missing values to zero.
Do not aggregate revenues across supply-chain layers as market size.

Preserve both the period end and when information became public.
A historical “as of” query must exclude later publications and
restatements not available on the selected date.

RAG ASSISTANT

Use hybrid keyword and vector retrieval with metadata filters.

Retrieve by:
- Company.
- Document type.
- Publication date.
- Reporting period.
- Topic.

Answers should:
- Cite retrieved sources.
- Show reporting periods and units for financial claims.
- Separate evidence from interpretation.
- State when evidence is insufficient.
- Handle conflicting sources explicitly.
- Use financial tools for calculations.

A citation must resolve to stored evidence.
Do not treat citation presence alone as evidence of claim support.

Treat retrieved documents as untrusted content.
Document instructions must not override system instructions or
authorise tool execution.

Do not expose unrestricted SQL, shell access or arbitrary URLs as
LLM tools. Validate tool arguments and use bounded, read-only queries.

RESEARCH WORKFLOW

Implement a bounded LangGraph workflow:
1. Clarify the research question.
2. Gather relevant evidence and financial data.
3. Develop a thesis and explicit scenarios.
4. Retrieve counterevidence and challenge assumptions.
5. Validate calculations and citations.
6. Produce a research brief.

Research brief schema:
- Question and as-of date.
- Thesis.
- Supporting evidence.
- Counterevidence.
- Bull, base and bear assumptions.
- Risks.
- Invalidation conditions.
- Monitoring indicators.
- Missing evidence.
- Sources.
- Run metadata.

Persist job status and workflow checkpoints.
Use unique job IDs and idempotent processing.
Support retry limits, cancellation and timeouts.

Enforce:
- Maximum workflow steps.
- Maximum model calls.
- Input and output token limits.
- Per-run estimated cost limit.
- User/demo usage limits.

These workflows produce research theses and scenarios.
Do not implement trade execution or claim investment performance.
Do not implement backtesting without point-in-time data and
explicit bias controls.

INTERFACE

Build a professional, readable research interface.

Pages:
- Overview.
- Value chain.
- Industry economics.
- Company comparison.
- Ask the research assistant.
- Research briefs.
- Sources and methodology.

Show:
- Data freshness.
- Research as-of date.
- Chart source references.
- Financial units and definitions.
- Loading, empty and failure states.
- Whether live AI features are available.

The permanent static showcase must remain useful when the backend
is offline. It should contain the research, selected charts,
evaluation results and architecture.

Do not fabricate research findings or evaluation scores for the UI.

AWS DEPLOYMENT

Two independent Terraform stacks:

1. SHOWCASE
- Private S3 bucket for static frontend exports.
- CloudFront with Origin Access Control.
- Optional custom domain configuration.
- Published research and selected precomputed charts.
- No dependency on a live API to render the core site.

Ensure the frontend can be statically exported.
Keep dynamic work in the backend.

2. ON-DEMAND DEMO
- ECR for container images.
- API Gateway HTTP API and Lambda for short API operations.
- ECS Fargate tasks for ingestion and long research jobs.
- RDS PostgreSQL with pgvector for cloud retrieval and financial data.
- S3 for documents and reports.
- SQS with a dead-letter queue.
- DynamoDB on-demand for job status where appropriate.
- EventBridge Scheduler for optional ingestion triggers.
- CloudWatch logs and alarms.
- Secrets Manager for credentials.
- IAM roles with least privilege.
- GitHub Actions OIDC for deployment.

Keep PostgreSQL authoritative for research data and LangGraph
checkpoints. If DynamoDB is used, restrict its role to job status
and idempotency records; document the ownership boundary.

Do not add:
- Kubernetes.
- Always-running worker services.
- A load balancer unless justified by an implementation requirement.
- NAT gateways by default.
- Multi-AZ database deployment for this portfolio demo.
- Paid market-data subscriptions in the initial release.

Do not publicly expose RDS.
Document a private networking design for Lambda and Fargate.
If outbound API access requires public task networking or VPC
endpoints, explicitly document security and cost trade-offs.
Do not claim that a NAT-free design has zero networking cost.

Deployment region must be configurable.
Calculate costs for the chosen region before cloud provisioning.

Use separate local, showcase and demo configuration.
Document remaining charges after teardown, including snapshots,
logs, images, S3 objects and Terraform state resources.

No cloud provisioning or paid-resource creation until I explicitly
request deployment. Preparing code, Terraform, tests and deployment
documentation is authorised.

EVALUATION

Create a small human-reviewed evaluation set covering:
- Document facts.
- Financial comparisons.
- Calculations.
- Missing evidence.
- Conflicting sources.
- Historical as-of questions.
- Prompt injection in retrieved documents.
- Research thesis quality.

Compare:
1. Simple retrieval-backed question answering.
2. The agent research workflow.

Measure:
- Retrieval relevance.
- Citation support.
- Numerical accuracy.
- Correct handling of reporting periods.
- Appropriate abstention.
- Latency.
- Token usage and estimated cost.

Use deterministic checks where possible.
Keep human-reviewed answers for important finance questions.
LLM judges may supplement these checks, not replace them.

Never report an unexecuted evaluation as passing.
Version datasets, prompts, model identifiers and results.

CI/CD AND QUALITY

On pull requests:
- Formatting and lint checks.
- Backend tests.
- TypeScript checks.
- Frontend build.
- Relevant integration tests.

Use recorded fixtures for routine CI.
Run paid live-model evaluations manually or through a separately
controlled workflow.

Before deployment:
- Validate infrastructure.
- Build and scan container images.
- Run a smoke test.
- Document rollback.

Keep credentials out of Git, browser bundles, logs and fixtures.
Configure limited log retention.
Budget alerts are notifications, not spending caps.

FIRST IMPLEMENTATION MILESTONE

Implement a complete local vertical slice:
1. Working local development setup.
2. Database schema and migrations.
3. One permitted real source document ingested with provenance.
4. Parsing, chunking and indexing.
5. One financial calculation using traceable source data.
6. API endpoints for sources, financial metrics and questions.
7. Frontend showing the source, metric and a cited answer.
8. A small initial evaluation set and essential tests.
9. Clear setup and verification commands.

If API credentials are missing:
- Complete everything that can run without them.
- Provide a clearly labelled fixture-based demonstration.
- Document the exact configuration needed for live operation.
- Do not present fixture outputs as live model results.

Write AGENTS.md with the actual commands and conventions established
during implementation.

At the end of each milestone, report:
- What works.
- What was verified.
- Known limitations.
- How to run it.
- The next milestone.

Complete and verify this local slice before expanding into cloud
infrastructure or additional agents.
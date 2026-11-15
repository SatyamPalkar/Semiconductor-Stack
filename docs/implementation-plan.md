# Milestone 1 implementation plan

1. Establish Python 3.12/uv, Next.js static export, PostgreSQL/pgvector, migrations and local commands.
2. Ingest public NVIDIA FY2025 results with checksums, immutable originals and auditable extraction. Keep TSMC CY2024 financial coverage pending after HTTP 403; do not substitute numbers.
3. Store reported facts in PostgreSQL; calculate period-aware metrics with Decimal, provenance and as-of filtering.
4. Implement bounded hybrid retrieval, extractive cited responses without credentials, and opt-in Groq generation with one pinned embedding model.
5. Build the research interface, export an offline snapshot, execute meaningful tests/evaluations, and document limitations and next milestones.

Cloud provisioning, live model calls, DCF, trading, additional research agents and live financial-data subscriptions are outside this milestone.

# Data dictionary

## sources

`id`: catalog key + original-document SHA prefix. `company`: ticker within research scope. `url/publisher/title`: primary-source identity. `publication_date`: exact stated source date, nullable if unknown. `published_at`: conservative availability cutoff, not an asserted intraday release time. `retrieved_at`: actual UTC capture time. `checksum`: original full-document SHA-256. `stored_checksum`: bytes actually stored (the original or the explicitly recorded excerpt). `capture_kind`: original primary source or recorded primary-source excerpt. `storage_key`: content-addressed local file, not exposed by the API. `document_type`: earnings release or annual report. `accession`: null for the IR source; never invent an SEC accession. `accounting_basis`: company-specific US GAAP earnings-release/annual-report or Taiwan IFRS annual-report scope. TSMC date metadata comes from the printed cover date; historical online availability is unverified.

## financial_facts

`id`: source ID + fiscal label + metric. `source_id`: foreign key. `value`: NUMERIC(30,8), original magnitude, no float arithmetic. `currency/unit_scale`: USD/1,000,000 (NVIDIA, Micron, TI), TWD/1,000 (TSMC), EUR/1,000,000 (ASML), USD/1,000 (Amkor). `period_start`: null when not verified from the selected source. `period_end`: reported annual-column end. `period_kind`: annual. `fiscal_label`: FY2024/FY2025 for NVIDIA; FY2023/FY2024 for Micron; CY2023/CY2024 for TSMC, ASML, TI and Amkor. `locator`: statement / exact row label / annual end. `classification`: reported_fact. `transformations`: parser version, source row, original cashflow sign and normalization. Unique source/metric/end/kind prevents duplicate period observations even when start is null.

## chunks

`id`: deterministic financial-row reference. `source_id/company`: source/coverage filters. `text`: normalized, labelled reported fact with period, units and basis (not a free-form management summary). `locator/topic/period_end`: citation and retrieval filters. `embedding`: 384-dimensional pgvector. `embedding_id`: model repository/revision + quantization/pooling/normalization/length identity. HNSW cosine index plus a PostgreSQL full-text GIN index support rank fusion.

## derived metrics and static exports

Metrics are calculated at request/export time from authoritative database facts; they are not untraceable stored LLM outputs. Every result includes the definition, classification, as-of, unit, annual end, fiscal label and the complete input fact/source records. The static snapshot is a timestamped database export, useful offline but not a live market feed.

Synthetic amendment/conflict records exist only inside rollback-controlled integration tests. They are never allowed into research snapshots or published findings. The real source excerpt used for offline CI is explicitly marked `synthetic: false` and preserves both original and extract checksums.

## investigation export / API

`GET /api/investigation?as_of=YYYY-MM-DD` and `snapshot.investigation` expose the same bounded `nvda-tsmc-cash-v1` contract. Four company/period records identify latest/prior windows, exact ends, successful metrics and missing-input reasons. Each metric contains original currency/scale, its company-specific definition and complete financial source references. `comparability` states the calendar, currency, accounting, capital-spending and interpretation limits. `human_reviewed` and `historical_archive_certified` remain false. The frontend additionally withholds metrics and comparative prose when source dates exceed the selected date.

## Discovery directory

`GET /api/directory` and `snapshot.directory` expose the validated `data/catalog/semiconductor-directory.json` plus allowlisted link observations. Catalog date, scope, eight role categories, company/business metadata and research resources are distinct from financial facts. Optional `financial_company_id` maps a directory record to a supported financial issuer; `financial_loaded` is derived from actual database coverage, not inferred from a website URL. It describes dataset presence, not availability at every selected date.

Only the current catalog’s public URLs and observation fields `url/state/status/checked_at` enter the browser export. HTTP status does not prove content or availability. Directory text is not embedded, retrieved, or cited as financial evidence. The server’s financial router rejects named directory-only companies rather than substituting the selected issuer’s figures.

## Application context API / export

`GET /api/applications` and `snapshot.applications` contain nine educational application worlds, five function definitions, source references and selected geographic examples. World steps carry `task/functions/chips/company_ids/source_ids/economic_question`. Each company ID must resolve to the discovery directory and a company-specific supporting reference. The data does not assert a bill of materials, supplier contract or application revenue.

Reference records preserve publisher, URL, scope of support, curation/review date, known publication date and the latest bounded HTTP observation (`link_status/link_checked_on/access_note`). HTTP 401/403/429 observations require a note. The catalog’s `human_reviewed` remains false. `footprints` distinguish region/location/role and source-supported company context; they are not shipment edges. No application records enter the financial fact or embedding tables.

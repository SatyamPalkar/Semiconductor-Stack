# Data dictionary

## sources

`id`: catalog key + original-document SHA prefix. `company`: ticker within research scope. `url/publisher/title`: primary-source identity. `publication_date`: exact stated source date, nullable if unknown. `published_at`: conservative availability cutoff, not an asserted intraday release time. `retrieved_at`: actual UTC capture time. `checksum`: original full-document SHA-256. `stored_checksum`: bytes actually stored (the original or the explicitly recorded excerpt). `capture_kind`: original primary source or recorded primary-source excerpt. `storage_key`: content-addressed local file, not exposed by the API. `document_type`: earnings release. `accession`: null for the IR source; never invent an SEC accession. `accounting_basis`: unaudited US GAAP for the selected source.

## financial_facts

`id`: source ID + fiscal label + metric. `source_id`: foreign key. `value`: NUMERIC(30,8), original magnitude, no float arithmetic. `currency`: USD in the pilot. `unit_scale`: 1,000,000. `period_start`: null when not verified from the selected source. `period_end`: reported annual-column end. `period_kind`: annual. `fiscal_label`: FY2024/FY2025. `locator`: statement / exact row label / annual end. `classification`: reported_fact. `transformations`: parser version, source row, original cashflow sign and normalization. Unique source/metric/end/kind prevents duplicate period observations even when start is null.

## chunks

`id`: deterministic financial-row reference. `source_id/company`: source/coverage filters. `text`: normalized, labelled reported fact with period, units and basis (not a free-form management summary). `locator/topic/period_end`: citation and retrieval filters. `embedding`: 384-dimensional pgvector. `embedding_id`: model repository/revision + quantization/pooling/normalization/length identity. HNSW cosine index plus a PostgreSQL full-text GIN index support rank fusion.

## derived metrics and static exports

Metrics are calculated at request/export time from authoritative database facts; they are not untraceable stored LLM outputs. Every result includes the definition, classification, as-of, unit, annual end, fiscal label and the complete input fact/source records. The static snapshot is a timestamped database export, useful offline but not a live market feed.

Synthetic amendment/conflict records exist only inside rollback-controlled integration tests. They are never allowed into research snapshots or published findings. The real source excerpt used for offline CI is explicitly marked `synthetic: false` and preserves both original and extract checksums.

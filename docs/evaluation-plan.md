# Evaluation plan

`evaluations/datasets/milestone1.json` is versioned, with synthetic questions and expected values sourced from real NVIDIA financial rows. It is **draft and not independently human-reviewed**. Do not remove that label until an actual reviewer confirms the important finance answers and citation support.

## Executed milestone-1 checks

The CLI records a real execution timestamp, dataset checksum, embedding identity, case results, latency and hosted usage in `evaluations/results/milestone1.json`. It checks numerical oracles, annual reporting-period handling, expected retrieval topics, source-ID resolution, as-of exclusion and appropriate abstention. It makes zero hosted model calls. A score does not measure generated-answer entailment or investment performance.

Pytest additionally covers source schema drift, quarterly/annual extraction, cashflow sign conventions, missing inputs, zero denominator, currency/scale mismatches, idempotence, later restatements, conflicting publications, metadata filters, source citations, instruction injection and model-output schema/reference rejection. The synthetic database revisions roll back after every test. API tests verify real database contracts and reject unconfigured live generation.

Playwright checks the production static export: real metrics/charts, provenance, earlier as-of dates, database-backed calculation answers, unsupported market prices, an API-offline labelled example, honest empty states and mobile navigation. It uses an isolated Chrome profile, not personal browsing sessions.

## Not yet measured

Independent human citation support, historical-source archival integrity, financial comparability across companies, a live hosted model and the LangGraph workflow are not evaluated. No fabricated score or unexecuted agent comparison is shown. Add financial comparisons, conflicting prose, multi-company evidence, harder retrieval paraphrases and thesis quality before comparing simple QA against an agent.

Future live runs must be opt-in, use fixed prompts/models/datasets, record token usage and estimated cost and enforce run limits. An LLM judge may supplement human review; it cannot replace it.

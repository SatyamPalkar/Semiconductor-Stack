# Evaluation plan

`evaluations/datasets/milestone1.json` is versioned, with synthetic questions and expected values sourced from real NVIDIA financial rows. It is **draft and not independently human-reviewed**. Do not remove that label until an actual reviewer confirms the important finance answers and citation support.

## Executed milestone-1 checks

The CLI records a real execution timestamp, dataset checksum, embedding identity, case results, latency and hosted usage in `evaluations/results/milestone1.json`. It checks numerical oracles, annual reporting-period handling, expected retrieval topics, source-ID resolution, as-of exclusion and appropriate abstention. It makes zero hosted model calls. A score does not measure generated-answer entailment or investment performance.

Pytest additionally covers source schema drift, quarterly/annual extraction, cashflow sign conventions, missing inputs, zero denominator, currency/scale mismatches, idempotence, later restatements, conflicting publications, metadata filters, source citations, instruction injection and model-output schema/reference rejection. The synthetic database revisions roll back after every test. API tests verify real database contracts and reject unconfigured live generation.

Playwright checks the production static export: real metrics/charts, provenance, earlier as-of dates, database-backed calculation answers, unsupported market prices, an API-offline labelled example, honest empty states and mobile navigation. It uses an isolated Chrome profile, not personal browsing sessions.

## Not yet measured

Independent human citation support, historical-source archival integrity, financial comparability across companies, a live hosted model and the LangGraph workflow are not evaluated. No fabricated score or unexecuted agent comparison is shown. Add financial comparisons, conflicting prose, multi-company evidence, harder retrieval paraphrases and thesis quality before comparing simple QA against an agent.

Future live runs must be opt-in, use fixed prompts/models/datasets, record token usage and estimated cost and enforce run limits. An LLM judge may supplement human review; it cannot replace it.

## CI portability follow-up (15 November 2026)

The original v1.1 dataset scored 21/21 on the local ARM development environment and 20/21 on the Linux CI runner. Its generic “reported research and development expense” question did not reliably meet the bounded semantic retrieval threshold. This is a supported-vocabulary limitation, not a financial calculation failure; no threshold was lowered and no expected topic or numerical check was removed.

Dataset v1.2 makes that one document-fact query explicit: “NVIDIA annual research and development expense”. It retains the expected `research_development` topic, citation/date checks and all other cases. Results now derive their version label from the dataset and continue to include dataset/pipeline hashes. A passing v1.2 score must not be described as proof that the original vague paraphrase works across platforms. The unconfigured-model API test separately uses real stored evidence to test the provider boundary independently of retrieval scores.

The combined CI pytest run uses importlib collection so unit/integration test files may share a basename. It runs all 85 current tests together; the usual local Make targets still allow the suites to run separately.

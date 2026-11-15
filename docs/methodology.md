# Research methodology

The central question is where semiconductor economic value is created and captured, and how this could change. Begin with a small traceable financial pilot instead of publishing unsupported industry rankings.

## Evidence classes

1. **Reported facts:** seven selected NVIDIA annual financial rows for each of FY2024 and FY2025. Original scale is USD millions; the release is unaudited US GAAP.
2. **Calculated metrics:** Decimal transformations defined in `financials/engine.py`, with exact input IDs/locators. Display rounding does not create additional source precision.
3. **Management guidance:** not ingested in milestone 1. The release contains outlook text, which the financial parser deliberately does not index as a reported fact.
4. **Analyst assumptions:** absent financial fields remain null; scenarios are not invented. Reporting-period starts are null because the selected release reports ends and annual-column labels, not independently verified starts.
5. **Research interpretations:** the initial UI note states a hypothesis to investigate and missing evidence. It makes no valuation or investment-performance claim.

## Source access

The NVIDIA URL is a fixed public publisher page. One request, no retries, no arbitrary URL input or access-control bypass. Its original bytes are preserved with SHA-256. A small recorded primary-source table excerpt is committed for deterministic CI; it contains real reported values, clearly distinguished from synthetic tests. The original full article is ignored and not redistributed in the static website.

TSMC's historical PDF and annual-report page returned HTTP 403 during setup. That is recorded as an access limitation. No third-party estimate or changed User-Agent was used to bypass it. SEC integration is deferred until a declared contact User-Agent is configured; source policies/rate limits must be implemented with that connector.

## Historical availability

The release states 26 February 2025 without a verified publication timestamp. `publication_date` records that date. `published_at` is a conservative availability cutoff at 23:59:59 America/Los_Angeles (27 February 07:59:59 UTC). Day-level as-of filters compare against UTC end of the selected date; they may exclude a source for part of its actual publication day. This avoids claiming an unverified earlier intraday release time.

Later publications/restatements are excluded until their availability cutoff. Selection is per company, annual period and metric, newest available publication then retrieval. Conflicting same-publication values require review. Identical duplicates do not double count. The historical IR page was captured later than publication and is unversioned: this is **not a certified point-in-time data archive** and is unsuitable for backtesting claims.

## Comparison limits

NVIDIA annual fiscal periods end on 28 January 2024 and 26 January 2025. They must not be labelled calendar-year revenue. TSMC and other companies have no financial data loaded. Currency and unit changes fail explicitly; there is no implicit USD conversion. Do not add company revenues across supply-chain layers to estimate market size. Capex/FCF definitions require company-specific reconciliation before comparison.

## Answering

Calculation requests use a bounded financial vocabulary or an explicit validated metric enum. This is a small pilot selector, not a general conversational controller. Unsupported forecasts, market prices, uncovered companies and multi-period comparisons abstain. Paraphrases can also abstain and should be evaluated before broadening the selector.

Non-calculation fact questions use company/date/type/period/topic filters, PostgreSQL full-text ranking and cosine retrieval with reciprocal rank fusion. A similarity score is relevance, not support. Topic admission constrains extractive answers to stored financial concepts. The optional model sees only bounded source data as untrusted input; JSON/citation validation cannot independently prove entailment.

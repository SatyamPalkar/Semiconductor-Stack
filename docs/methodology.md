# Research methodology

The central question is where semiconductor economic value is created and captured, and how this could change. Begin with a small traceable financial pilot instead of publishing unsupported industry rankings.

## Evidence classes

1. **Reported facts:** seven selected NVIDIA annual financial rows for each of FY2024 and FY2025, plus ten selected TSMC annual-report observations across CY2023/CY2024 and 54 selected observations for ASML, Micron, TI and Amkor. Native scales are USD millions, EUR millions and TWD/USD thousands. NVIDIA uses unaudited US GAAP earnings-release data; TSMC uses consolidated Taiwan IFRS annual-report tables.
2. **Calculated metrics:** Decimal transformations defined in `financials/engine.py`, with exact input IDs/locators. Display rounding does not create additional source precision.
3. **Management guidance:** not ingested in milestone 1. The release contains outlook text, which the financial parser deliberately does not index as a reported fact.
4. **Analyst assumptions:** absent financial fields remain null; scenarios are not invented. NVIDIA and expanded-source period starts remain null because the selected excerpts do not independently establish them. TSMC observations use calendar-year boundaries. Neither missing figures nor unknown start dates are invented.
5. **Research interpretations:** the cash-investigation note separates a supported descriptive observation from its proposed explanation, counterevidence and conditions that would change it. It is labelled editorial interpretation with human review pending, not analyst-reviewed or agent-produced research. It makes no valuation or investment-performance claim.

## Source access

The NVIDIA URL is a fixed public publisher page. One request, no retries, no arbitrary URL input or access-control bypass. Its original bytes are preserved with SHA-256. A small recorded primary-source table excerpt is committed for deterministic CI; it contains real reported values, clearly distinguished from synthetic tests. The original full article is ignored and not redistributed in the static website.

Earlier TSMC IR requests returned HTTP 403 during setup. This remains an access limitation. During the explicitly requested cash investigation, separately published annual-report PDFs linked from TSMC’s public 2023/2024 report pages returned HTTP 200. Their original bytes were preserved, selected tables extracted and hash-verified REAL excerpts recorded for setup. This is a documented separate source selection, not a retry of the blocked endpoint, a proxy or a changed identity. No third-party estimate was substituted. SEC integration is deferred until a declared contact User-Agent is configured; source policies/rate limits must be implemented with that connector.

## Historical availability

The release states 26 February 2025 without a verified publication timestamp. `publication_date` records that date. `published_at` is a conservative availability cutoff at 23:59:59 America/Los_Angeles (27 February 07:59:59 UTC). Day-level as-of filters compare against UTC end of the selected date; they may exclude a source for part of its actual publication day. This avoids claiming an unverified earlier intraday release time.

TSMC’s report covers say “Printed on March 12, 2024” and “Printed on March 12, 2025”. These source dates are recorded with conservative end-of-Taipei-day cutoffs (15:59:59 UTC); the UI explicitly calls them printed dates. Actual historical online availability is unverified. This policy does not certify that the later-captured files existed unchanged on their printed dates.

Later publications/restatements are excluded until their availability cutoff. Selection is per company, annual period and metric, newest available publication then retrieval. Conflicting same-publication values require review. Identical duplicates do not double count. The historical IR page was captured later than publication and is unversioned: this is **not a certified point-in-time data archive** and is unsuitable for backtesting claims.

## Comparison limits

NVIDIA annual fiscal periods end on 28 January 2024 and 26 January 2025. They must not be labelled calendar-year revenue. TSMC, ASML, TI and Amkor CY2023/CY2024 end on 31 December. Micron FY2023/FY2024 end on 31 August 2023 and 29 August 2024. The CY label denotes a calendar-year-ended observation; reported ends are always preserved. Comparisons use each company’s native-unit ratios, with explicit differences in capital spending and accounting. Unrecognized currency/scale profiles and mismatches fail explicitly; there is no implicit USD conversion. Do not add company revenues across supply-chain layers to estimate market size. Capex/FCF definitions require company-specific reconciliation before comparison.

## Answering

Calculation requests use a bounded financial vocabulary or an explicit validated metric enum. This is a small pilot selector, not a general conversational controller. Unsupported forecasts, market prices, uncovered companies and multi-period comparisons abstain. Paraphrases can also abstain and should be evaluated before broadening the selector.

Non-calculation fact questions use company/date/type/period/topic filters, PostgreSQL full-text ranking and cosine retrieval with reciprocal rank fusion. A similarity score is relevance, not support. Topic admission constrains extractive answers to stored financial concepts. The optional model sees only bounded source data as untrusted input; JSON/citation validation cannot independently prove entailment.

## Directory and financial expansion

The company/resource catalog is current discovery metadata, dated independently from the historical research cutoff. It cannot supply financial answers, imply independent issuer status or turn supply-chain revenues into an additive market size. Link responses are bounded observations, not certification of content or source accuracy. Unavailable/restricted links remain labelled; no login, membership or licensing action is taken.

The four added sources preserve their own capital definitions in `financials/profiles.py`. Every configured capital payment and offset is mandatory; absent offsets never become zero. Micron negative income/gross profit stays negative. Amkor’s detailed statements and rounded reported-FCF reconciliation have different scales: the platform uses the detailed statements for an explicitly analytical gross-PPE residual and does not call it reported FCF. See [metric definitions](metric-definitions.md) and [executed expansion verification](industry-expansion-report.md).

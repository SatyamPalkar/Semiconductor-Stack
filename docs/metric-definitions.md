# Metric definitions — version 1

All monetary inputs are positive magnitudes in USD **millions**. Annual observations only; period end and fiscal label travel with every result. Decimal arithmetic is retained until the result is rounded to four decimal places for transport. Source inputs rounded to millions limit the implied precision.

| Metric | Definition / handling |
| --- | --- |
| Revenue | Reported annual revenue; no currency conversion |
| Revenue growth | `(revenue / prior annual revenue - 1) * 100`; prior ends must be 350–380 days apart; missing prior annual data is unavailable |
| Gross margin | `gross_profit / revenue * 100` |
| Operating margin | `operating_income / revenue * 100` |
| Capital purchases / revenue | Purchases related to property/equipment **and intangible assets** divided by revenue; not a PPE-only capex definition |
| R&D / revenue | Reported research and development expense divided by revenue |
| Operating cash flow | Reported net cash provided by operating activities |
| Free cash flow | Operating cash flow minus capital purchases **and related principal payments**, consistent with this NVIDIA release's definition; a non-GAAP measure |
| Free cash flow margin | The preceding FCF measure divided by revenue |

The parser records negative cashflow rows as positive outflow magnitudes and stores that normalization. NVIDIA FY2025 FCF is `64,089 - 3,236 - 129 = 60,724` USD million. Gross margin recomputed from source rows is 74.9887%; NVIDIA's summary rounds it to 75.0%. No missing component becomes zero. Zero denominators and missing/mismatched annual units/bases are rejected.

ROIC, inventory metrics, FX conversion and cross-company ratios are deferred. Their definitions and inputs require review before implementation. These are historical financial calculations, not investment recommendations.

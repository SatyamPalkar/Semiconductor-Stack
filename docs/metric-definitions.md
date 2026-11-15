# Metric definitions — cash investigation v1

Monetary observations retain their native scale: NVIDIA, Micron and TI **USD millions**; TSMC **TWD thousands**; ASML **EUR millions**; Amkor **USD thousands**. Disclosed capital outflows are positive magnitudes. Annual observations only; period end and fiscal label travel with every result. Decimal arithmetic is retained until the result is rounded to four decimal places for transport. Source rounding limits implied precision. Currency and scale must match all inputs inside a calculation and the supported company profile; there is no implicit FX conversion.

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

## TSMC scope and the comparison

The 2024 annual report supplies consolidated CY2024/CY2023 revenue, gross profit and operating income (printed p.124 / PDF p.64), CY2024 operating cash flow and CY2024/CY2023 actual capital expenditures (printed p.126 / PDF p.65). The 2023 annual report supplies CY2023 consolidated operating cash flow (printed p.132 / PDF p.68). These are selected report tables, not a complete financial-statement reconciliation.

For TSMC, `capex_revenue` uses the annual report’s total actual capital expenditures. Do not assume it has the same intangible, lease or principal-payment scope as NVIDIA’s rows. The shared API key `free_cash_flow` returns a company-specific definition: for TSMC it is the **analytical residual** `operating cash flow - annual-report capital expenditures`, excluding other investing/financing flows. It is not described as harmonized FCF. The comparison UI calls it “Cash after disclosed capital outlays”. TSMC CY2024: `1,826,177,068 - 956,006,536 = 870,170,532` TWD thousand.

Two additional ratios are implemented: `operating_cash_flow_margin = operating_cash_flow / revenue × 100`; `capex_operating_cash_flow = disclosed capital spending / operating_cash_flow × 100`. NVIDIA’s latter ratio uses purchases and excludes principal payments; its FCF still subtracts principal payments. Each source-specific definition travels with the result. Zero denominators and missing components fail explicitly.

Ratios remove the display currency unit, not accounting differences or FX exposure. NVIDIA fiscal periods and TSMC calendar years are shown side by side, not silently calendar-aligned. The investigation is descriptive over two annual observations per company; it cannot establish full-cycle returns, a causal business-model effect or investment merit. Independent review remains pending.

## Expanded company definitions

| Company | Capital investment used in ratios | Cash calculation / 2024 example |
| --- | --- | --- |
| ASML | PPE **and intangible** purchases | OCF minus those purchases: `11,166.2 − 2,083.1 = 9,083.1` EUR million; ASML annual-report non-GAAP FCF |
| Micron | PPE expenditures + equipment-contract payments − PPE sale proceeds − government incentives | `8,507 − 8,386 − 149 + 99 + 315 = 386` USD million; Micron adjusted FCF. FY2023 remains `−5,453` USD million |
| Texas Instruments | Release-disclosed capital expenditures | `6,318 − 4,820 = 1,498` USD million; TI non-GAAP FCF |
| Amkor | Gross PPE payments, no offset | `1,088,868 − 743,796 = 345,072` USD thousand; **analytical gross-PPE residual**, not Amkor reported FCF. Excludes sale/insurance/grant proceeds and finance-lease payments |

`financials/profiles.py` supplies the company-specific cash label and definition to every metric and financial-tool answer. API keys remain stable; `free_cash_flow` is not a promise of harmonized scope. Capital/operating-cash and capital/revenue use the profile’s same investment scope. NVIDIA additionally subtracts principal payments only in its FCF. Micron’s configured offsets must all exist; none is silently set to zero. Losses remain signed, including FY2023 gross margin −9.1120%.

ASML, TI and Amkor labels CY2023/CY2024 refer to years ended December 31; Micron FY2023/FY2024 ends are August 31, 2023 and August 29, 2024. These observations do not calendar-align NVIDIA or Micron to other companies.

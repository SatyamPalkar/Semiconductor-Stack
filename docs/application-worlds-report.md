# Application-led global semiconductor view

Implemented locally on 15 November 2026 after approval to expand from the production lifecycle into real-world applications. No deployment, GitHub push, live financial ingestion or hosted-model evaluation was performed in this milestone. Independent content/financial review remains pending.

## Delivered experience

The homepage now starts with AI systems, electric mobility and the built environment. An original SVG collage replaces the chip-only opening, and **Start the story** leads to applications before manufacturing. The story continues through business models, cash economics, the changing year and research questions.

`/applications/` adds nine worlds:

- AI, software and cloud
- Automotive and electric mobility
- Civil infrastructure and construction
- Automation and robotics
- Aviation and aerospace
- Design and digital engineering
- Energy and utilities
- Healthcare and medical equipment
- Communications and everyday devices

AI, electric mobility and smart infrastructure each have four guided tasks. The other six worlds have two-task overviews. All 24 tasks have conceptual diagrams, selectable hotspots, chip categories, an economic research question and primary references. The five recurring functions are compute, sense, communicate, control and manage power. Function and text filters, clear/empty states, safe world/task deep links, next/back controls and mobile return paths are implemented.

The illustrations depict systems, not literal bills of materials or verified vendor-to-customer flows. Company examples are linked only when a matching company reference is present. Company profiles and available historical financial datasets are reachable from those examples. Unassigned supplier cases remain unassigned rather than borrowing another company’s evidence.

A second view shows four selected geographic examples: NVIDIA headquarters context in the United States; a documented TSMC wafer-fabrication site in Taiwan; ASML equipment R&D/manufacturing in the Netherlands; and Amkor packaging/test capabilities in Vietnam. Region filters and conceptual map markers distinguish a headquarters from an operating site. These examples are independent of the selected application and do not establish its supplier chain, current capacity, shipping route or regional market share.

## Data and source boundaries

`data/catalog/application-worlds.json` contains educational context, 19 primary references, portfolio links and selected operating examples. `sources/applications.py` validates public HTTPS destinations, unique IDs, known functions, company mappings and source references. Restricted links require visible access notes. This structural validation does not establish entailment or independent human review.

`GET /api/applications` and `snapshot.applications` expose the same validated catalog through existing API/static-export boundaries. Application text is not inserted into PostgreSQL financial facts or the assistant’s financial retrieval store. The bounded assistant remains limited to its supported annual financial questions.

Application curation is dated separately from historical financial availability. Changing the financial date does not erase current educational guides; following a company financial link still applies that selected date to its figures. No application market-size, financial revenue contribution, customer contract, clinical outcome, aviation certification or investment ranking is inferred from a product/application guide.

The primary references include SIA’s end-use overview and company application documentation from NVIDIA, Micron, TI, Infineon, Analog Devices, ASML, TSMC and Amkor. A fixed-URL check was executed once per listed URL, with bounded reads and no retries or access-control bypass. The current references produced **18 HTTP 200 responses and one HTTP 403**. A stale ASML careers link returned 404 and was explicitly replaced by its separately published Veldhoven location page, whose R&D/manufacturing statement was inspected. The ADI structural-monitoring demonstration remains linked and visibly labelled as restricted to the automated request; its official indexed description was reviewed. No alternate identity, proxy or access bypass was used. HTTP responses do not certify content or future availability. The detailed audit stays in ignored `data/interim/application-reference-links.json`.

## Executed verification

- `RUN_DB_TESTS=1 UV_NO_SYNC=1 uv run pytest -q`: **91 passed**, including reference resolution, company-specific citation requirements, unsafe URLs, duplicate IDs, restricted-reference disclosure, geographic evidence and API/snapshot agreement.
- `UV_NO_SYNC=1 make lint`: Ruff, format checks and TypeScript passed.
- `UV_NO_SYNC=1 make evaluate`: **21/21** deterministic NVIDIA development cases passed with zero hosted-model calls. This does not evaluate application-guide truth or general industry QA.
- `UV_NO_SYNC=1 make snapshot build`: database export and eight-route static production build passed.
- `UV_NO_SYNC=1 make e2e`: the expansion browser run recorded **30 passing workflows**, including application-first entry, all nine scenes/tasks, AI memory/network/power transitions, filters/empty states/invalid deep links, portfolio/financial links, geography, offline use, historical financial filtering, mobile hotspots and reduced motion. Previous financial/directory/source workflows remain covered. Eight routes were checked at 1440/768/393px without page overflow or browser errors.
- Desktop and phone captures of the opening, AI explorer, infrastructure story and geography view were visually inspected. Original SVGs are code-native; no third-party photos were copied. QA screenshots remain ignored local artifacts.

## Review locally

- Applications: http://127.0.0.1:3100/applications/
- AI: http://127.0.0.1:3100/applications/?world=ai-cloud
- Electric mobility: http://127.0.0.1:3100/applications/?world=electric-mobility
- Smart infrastructure: http://127.0.0.1:3100/applications/?world=smart-infrastructure
- Application-led opening: http://127.0.0.1:3100/

The retained static preview is PID **54834** on loopback 3100; the refreshed API is PID **77927** on loopback 8100. Stop with `kill 54834` and `kill 77927`, or Ctrl+C in their originating terminals. Restart with `make preview` and `make api`. These current process IDs supersede the earlier preview reports’ API IDs. The user’s database on 5432 remains untouched; the project-owned native database remains on 55432.

The subsequent homepage composition refinement and its current browser checks are recorded in [homepage-refinement-report.md](homepage-refinement-report.md).

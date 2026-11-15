# Guided storytelling update

Implemented locally on 15 November 2026, following the request for more storytelling, smoother flow and stronger graphics. No deployment, source ingestion, financial-model change or hosted-model evaluation was performed. Independent financial/citation review remains pending.

## Reading experience

The overview now follows four connected chapters:

1. **The system:** an illustrated opening introduces the industrial context. Design, fabrication, equipment and packaging/test lenses change the scene, company example and question together. NVIDIA, TSMC, ASML and Amkor link to their existing financial explorers.
2. **The cash:** a short narrative bridge leads into the existing NVIDIA/TSMC source-backed investigation. Next/back controls guide the three financial views, with direct tabs retained. The final view continues to the next story chapter.
3. **The changing year:** a Micron example switches between gross margin and adjusted free cash flow margin across FY2023/FY2024. Signed bars, a zero reference, dates and textual values retain the negative year. Source calculations remain expandable. Two annual observations are explicitly insufficient to establish a cycle or durable trend.
4. **Your next question:** four editorial paths connect to the atlas, financial datasets, research note and resources.

A sticky chapter rail tracks the current reading position. Native anchors and header-aware spacing support direct navigation without scroll hijacking. On narrow screens the rail scrolls horizontally to reveal the active chapter. Each supporting research page now recommends one continuation, including a direct route from the research note to ingested evidence.

## Graphics and motion

`story-graphics.tsx` creates original SVG chip layers, circuit traces, a wafer/die array, a conceptual equipment/light-beam scene and a connected layer stack. The illustrations are explicitly conceptual; no process dimensions, supplier relationships or literal production sequence are asserted. They are code-native assets, not downloaded photographs or company logos.

Near-black surfaces, mint/blue/violet accents, larger editorial headings and short passages connect the existing visual language across routes. Gentle chip motion, signal travel and scene transitions provide continuity. No timed carousel or automatic chapter advance was added. Reduced-motion preferences disable animation and smooth scrolling; content remains visible without motion.

## Evidence behavior preserved

All financial ratios come from the existing database-derived snapshot. Browser arithmetic only positions graphics and rounds displayed values. The Micron graphic uses the same source-availability filter as the existing financial pages. When its inputs were not available by the selected date, the graphic, dependent interpretation and source-value disclosures are withheld. Conceptual industry copy is separate from historical financial findings.

Existing native currencies, fiscal labels/ends, company cash definitions, original source rows, source checksums, offline examples, unsupported-company abstention and bounded question routes remain in place. This update adds presentation and navigation, not a financial conclusion or an executed research workflow.

## Verification executed

- `UV_NO_SYNC=1 make lint`: Ruff, format checks and TypeScript passed.
- `UV_NO_SYNC=1 make build`: static production export passed.
- `UV_NO_SYNC=1 make e2e`: **23 workflows passed** against the local production export and actual local API. The latest result is recorded in `evaluations/results/browser-summary.json`.
- New browser coverage checks the single opening heading, business-lens next/back and arrow/Home/End keyboard behavior, matching illustrations, chapter anchors and active state, sequential cash controls, the continuation into Micron, signed gross/cash margins, exact source inputs and as-of withholding, the research-note-to-ingested-evidence route, mobile touch targets and reduced motion.
- Existing workflows still cover chart values/units, source lineage, financial API answers, directory/profile/resource filtering, native EUR/TWD/USD views, unsupported questions, offline behavior and seven routes at 1440/768/393px with no page overflow or browser errors.
- Desktop and phone captures were visually inspected, including the opening, business-model chapter and signed Micron graphic. Captures remain in ignored `data/interim/web-review`.

No backend tests or model evaluations were newly claimed for this presentation-only update; their earlier executed results are documented in the expansion report.

## Local review

Open http://127.0.0.1:3100/ and choose **Start the story**. The existing atlas, all six financial datasets and the 36-resource library remain available through the main navigation and story paths.

The retained static preview runs on loopback 3100 (PID 54834); the API runs on loopback 8100 (PID 65736). Stop with `kill 54834` and `kill 65736`, or Ctrl+C in the originating terminals. Restart using `make preview` and `make api`. No cloud hosting or public publication occurred.

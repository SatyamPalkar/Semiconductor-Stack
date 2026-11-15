# Visual conclusions — 15 November 2026

The user requested an appealing visual reading of the NVIDIA–TSMC conclusions, inspired by a supplied dark orbital semiconductor visualization. This local UI milestone uses the existing investigation API/export and changes how the reader explores the findings.

## Experience

The overview now opens with an interactive conclusion map: near-black canvas, dotted orbit guides, violet revenue-denominator node, mint NVIDIA node and blue TSMC node. Equal-size nodes and fixed positions are conceptual; numerical labels and 0–100 arcs encode the existing company-specific ratios. Decorative connections do not assert cash transfers, supplier relationships, market size or investment rankings.

Three chapters expose the reasoning: operating cash / revenue, disclosed capital spending / revenue, then cash after disclosed capital outlays / revenue. A short headline communicates each reading; the capital chapter emphasizes different spending paths rather than a harmonized ranking. Select either company to inspect its period, definition and original source inputs. The year-pair selector remains available. Detailed financial tables, comparability notes and broader business-model exploration are optional disclosures.

The company comparison shares this visual. Missing evidence removes percentage arcs and withholds comparative conclusions in every chapter. Available company figures remain inspectable. Source definitions stay adjacent to each reading. Keyboard selection, visible focus and reduced-motion support are implemented. Native touch targets are checked to be at least 44 pixels wide and contained within the diagram at the tested widths.

No financial ratio, source data, ingestion behavior or model workflow was added or recalculated by the visualization. Existing Decimal-derived percentages are formatted and drawn; comparison headlines use those available values. NVIDIA and TSMC currencies, fiscal labels and different capital-outlay definitions remain explicit. Human review remains pending.

## Implementation

- `apps/web/app/conclusion-map.tsx` and `.css`: chapter controls, orbit diagram, accessible company selection, conclusion and evidence inspector.
- `apps/web/app/metric-evidence.tsx`: shared metric labels, display formatting and source disclosure, extracted from the existing investigation component.
- `apps/web/app/investigation.tsx`: shared visual entry point, existing date/period filtering and optional detailed table.
- `apps/web/app/story.tsx`: conclusion-first overview and optional business-model exploration.
- `tests/e2e/research.spec.ts`: updated meaningful browser workflows for the visual representation and preserved financial/source behavior.

## Executed verification

- `UV_NO_SYNC=1 make lint`: Ruff, formatting and TypeScript passed.
- `UV_NO_SYNC=1 make build`: production static export passed with no development server running in `.next`.
- `UV_NO_SYNC=1 make e2e`: **15 workflows passed**, including chapter switching, native-unit source inspection, earlier-date withholding in every chapter, optional tables, keyboard activation, reduced motion, API/offline behavior and all seven routes at 1440/768/393 pixels. No browser page errors or horizontal page overflow were observed. The final machine-readable summary is `evaluations/results/browser-summary.json`.
- Desktop and mobile screenshots were visually inspected by the coding agent. They remain in ignored `data/interim/web-review/`. This is not independent human review.
- `git diff --check` passed. Backend-only tests and the financial evaluation were not rerun for this presentation-only change; the preceding financial milestone’s executed checks remain documented separately.

The initial browser run exposed ambiguous accessible names on chapter controls and a missing stylesheet after an earlier permission-review timeout. Both were corrected before the final successful build/browser run. The final result contains the actual compiled stylesheet and working native controls.

## Local review

The updated production preview remains at `http://127.0.0.1:3100/`, with the detailed comparison at `/companies/`. Use `make preview` and `make api` after normal local setup. Stop foreground servers with Ctrl+C in their terminals. This milestone preserves the useful running local preview and does not publish, provision cloud resources or execute hosted-model evaluations.

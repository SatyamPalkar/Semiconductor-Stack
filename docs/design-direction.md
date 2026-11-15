# The Silicon Atlas

Semiscope presents semiconductor research as an investigation. The reader moves from a physical object to the industrial system around it, then to a sourced financial observation and the questions it cannot yet answer.

## Reading sequence

1. **The question:** “Who turns growth into cash?” introduces NVIDIA and TSMC, the historical periods and the review status. Existing original wafer artwork preserves the visual identity.
2. **The finding:** adjacent cash profiles distinguish operating cash generation from the cash remaining after each company’s own capital outlays. Latest/prior annual-pair selection changes the evidence; expandable calculations expose original units and row/page locators.
3. **The limits:** company-specific definitions and a comparability note explain calendars, currencies, accounting and investment scopes before any value-capture inference.
4. **The argument:** the research note develops the descriptive finding, counterevidence and conditions that could overturn the explanation. It is an editorial interpretation awaiting independent review.
5. **The instruments:** company financial charts, a bounded evidence desk and the source/methodology library support the investigation. Other companies remain a collapsible coverage register, not a fabricated comparison.

## Visual language

The current direction follows the user's selected **18 / Texturized and Dynamic** example from [Visme's colour-scheme collection](https://visme.co/blog/website-color-schemes/): slate blue `#2F4454`, burgundy `#2E151B`, dusty pink `#DA7B93`, teal `#376E6F` and deep teal `#1C3334`. Lighter text and accent variants preserve legibility against the dark surfaces.

Use locally bundled Barlow Condensed ExtraBold for emphatic headlines and Barlow for reading text. This is a similar typographic direction, not a claim to reproduce HAUS's original font. The fonts and their SIL Open Font Licenses are in `apps/web/app/fonts`. Original SVG grain, pink/teal wafer lighting and brief entrance motion add texture. All motion is disabled when reduced motion is requested.

Thin rules, asymmetric spreads and typographic rows preserve the analytical publication structure. The shared masthead acts as an index, with a compact menu on mobile.

The supporting pages are working documents: charts beside definitions, company registers, an evidence desk with margin notes, a research note and a source record. The assistant is one instrument in the investigation rather than the entire product identity.

## Financial graphics

Revenue has directly labelled columns and an optional two-point slope view, with hover details and a persistent period/value key. The slope explicitly connects only the two annual observations; no interim series is invented. Gross margin uses horizontal share bars on a full 0–100% scale, endpoint markers and numeric labels. Previous periods use teal hatching, while the latest period uses dusty pink, so the comparison does not depend on colour alone. Revenue charts retain a zero baseline. Values, definitions, source access and publication-date filtering use the existing snapshot/API contracts.

Keep small labels at least 10 CSS pixels, normal explanatory text around 14–15 pixels, visible keyboard focus and reduced-motion support. Do not use decorative company figures or imply an unexecuted workflow has run.

## Implementation and verification

- `apps/web/app/story.tsx`: narrative chapters, wafer artwork and interactive research lenses.
- `apps/web/app/platform.tsx`: masthead, supporting research pages and existing API interactions.
- `apps/web/app/globals.css`: shared publication layout and responsive styles.
- `apps/web/app/research-types.ts`: the existing snapshot/answer contracts shared by the views.

The redesign passed TypeScript checking, the Next production build and ten Playwright workflows, including chart-view switching without changing displayed observations, the layer-to-provenance path, financial API answers, source inspection, as-of filtering, offline handling and mobile navigation. All seven routes were also inspected at 1440, 768 and 393 pixels: no horizontal page overflow or browser page errors were observed. Reduced-motion emulation confirmed a visible cover with no entrance animation. This verifies interface behaviour; it is not new financial, model or human-review evaluation.

## Cash investigation update

`app/investigation.tsx` holds the shared comparison, source-row disclosure and substantive research note. Percentage bars use consistent 0–100 tracks, numerical labels and pattern/color differences. On small screens the detailed comparison becomes labelled company rows instead of requiring sideways scrolling. `platform.tsx` exposes company selection for financial charts, evidence questions and financial definitions. The historical date filters both figures and dependent comparative prose. Verification for this update is recorded separately in `cash-investigation-report.md`; the earlier redesign checks above refer to that earlier implementation.


## Visual conclusions — orbital reading experience

The user supplied a dark orbital semiconductor visualization as inspiration. The new cover replaces the illustrative wafer and long initial reading sequence with a source-backed conclusion map. A near-black canvas, dotted orbital guides, a violet denominator node, mint NVIDIA node and blue TSMC node establish the visual language. The nodes have equal size and fixed positions; only their numerical labels and 0–100 percentage arcs encode financial data. Decorative connections do not assert supply-chain cash transfers or company relationships.

Three explicit chapters switch between operating cash / revenue, disclosed capital spending / revenue and cash after disclosed capital outlays / revenue. The conclusion changes with the selected chapter and actual available values. The capital chapter emphasizes different spending scopes instead of claiming a harmonized ranking. Each node selects a company-specific evidence inspector. Full financial tables, comparability details and broader business-model exploration are disclosures the reader can choose to open.

The overview puts this experience first. Company comparison uses the same component and source-date filtering. Missing evidence suppresses both the percentage arc and comparative conclusion. Controls use native buttons, descriptive accessible names, keyboard focus and reduced-motion support. The inspector closes when its metric/company/period changes, preventing stale evidence from appearing under a different observation.

Verification for this visual update is recorded in `visual-conclusions-report.md`. Earlier reading-sequence and wafer descriptions in this document describe the previous iteration.

## Current direction — guided visual story (15 November 2026)

The current overview opens with “A tiny chip. An entire economy.” and an original isometric chip illustration. Four chapters then move through the industry’s business lenses, the existing cash investigation, a two-observation Micron example and four next research questions. Earlier cover/wafer and first-screen descriptions above record previous iterations.

Near-black, mint, blue and violet now connect all seven routes. The chapter rail tracks the reading position without taking over scrolling; native anchor links allow direct navigation. Design, fabricate, equip and connect each change the illustration, company lens and research question. Tab arrows/Home/End and explicit next/back buttons support keyboard and pointer use. The illustrations depict roles conceptually, not supplier relationships, process dimensions or a literal sequence.

The existing cash visualization has sequential controls and a continuation into the Micron chapter. The new signed bar graphic shows database-exported gross margin or adjusted cash margin, with a zero reference, fiscal labels, annual ends, textual values and source details. It never interpolates a cycle or computes new financial ratios in the browser. Missing source availability suppresses both the graphic and its interpretation.

Short transition passages carry a question from one chapter into the next. Supporting pages each recommend one next step. Details and sources remain available without dominating the initial reading. There is no timed carousel or automatic chapter change; gentle chip float/signal motion and illustration transitions stop when reduced motion is requested.

[Executed verification and local review](storytelling-report.md).

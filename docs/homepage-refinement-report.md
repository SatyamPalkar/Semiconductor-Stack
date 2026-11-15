# Homepage composition refinement — 15 November 2026

The homepage now has a single visual focus: an original layered silicon die, surrounded by six linked application worlds. It replaces the competing server, car, building and aircraft collage. The existing nine-world application explorer and financial research remain intact.

The new `homepage-cover.tsx` and scoped CSS module use a balanced headline/diagram layout, a mint call to action, restrained orbital guides, and separate company/application/financial coverage counts. Pointer hover and keyboard focus reveal a short application caption on wide screens. Native links open the corresponding application story; the secondary link opens all nine worlds. Connections are conceptual shared-function illustrations, never supplier or shipment claims.

Phone layouts stack the content, retain 44px minimum application targets and omit the desktop caption to prevent crowding. The shared masthead now fits 320px screens. Reduced motion disables chip movement, signal animation and transitions. No new dependencies, external images, financial data or API contracts were introduced.

## Executed checks

- TypeScript and Next static production build passed.
- The complete Playwright run passed **31/31 workflows**, including the existing research flows and a new check of all six application links using keyboard activation. The map is checked at 1440, 1024, 768, 393 and 320px for overlapping links, minimum target sizes and page overflow.
- Desktop, tablet and phone screenshots were captured in ignored `data/interim/web-review/refined-cover-*.png`; desktop/tablet/393px captures were visually inspected. A small caption omission on tablet followed this review and was rechecked in the final build/browser run.
- Backend tests were not rerun for this presentation-only change. The previous expansion's 91-test backend run remains documented separately. No paid model calls or publishing occurred.

## Local review

Open http://127.0.0.1:3100/ . The retained static preview (PID 54834) serves the rebuilt export; stop with `kill 54834` and restart with `make preview`. The existing API (PID 77927) remains available; stop with `kill 77927` and restart with `make api`.

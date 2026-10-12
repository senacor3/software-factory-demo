---
title: 'Frontend: Ford-inspired UX redesign'
type: 'feature'
ticket: 11
created: '2026-10-12'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
baseline_revision: '609cde5a53b33a300a637df9cc626d56e1d32890'
context:
  - '{project-root}/_bmad-output/initiative-demo-app/ux-freight-tenders-ui/DESIGN.md'
  - '{project-root}/_bmad-output/initiative-demo-app/ux-freight-tenders-ui/EXPERIENCE.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The three Angular pages (overview, create-tender, detail) are unstyled browser-default HTML with plain `<ul>` lists -- nothing a dispatcher can scan or sort, and nothing presentable in the closing demo.

**Approach:** Restyle all three pages per `DESIGN.md` (Ford-blue palette, Inter type scale, flat bordered surfaces, status pills) and replace the overview's two lists and the detail page's remarks/offers lists with single-column click-to-sort tables per `EXPERIENCE.md`. No functional change to creating a tender, adding a remark/offer, or the closed-tender disabled state.

## Boundaries & Constraints

**Always:** German UI copy stays exactly as it is today; status shown as "Offen"/"Geschlossen" pill text, never the raw enum or colour alone; every sortable header is a real `<button>` inside a `<th>` carrying `aria-sort`; the sort indicator shows only on the active column; table header rows still render when a table is empty; DOM assertions keep going through `data-testid`; components keep reaching the backend only through `TenderApiService`.

**Decisions (2026-10-12):** Default sort is newest-first (id descending) on all four tables until the user sorts, so a newly created tender/remark/offer appears at the top. Sort state is page-local and resets on every visit (Component Patterns wins over Flow 2's "still sorted" line). Inter is self-hosted via the `@fontsource/inter` npm dependency. Offer amounts display in German format with a euro sign (`1.234,56 €`) -- UI only, the domain stays currency-free.

**Never:** No backend/API change. No persisted or cross-page sort state. No component or CSS library, no shadows/gradients/imagery. No multi-column sort, pagination, or filtering. No new routes or pages. No edit/delete.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Default order | Table loaded, nothing selected | Rows id descending; every header `aria-sort="none"`, no indicator | No error expected |
| Sort ascending | Select an unsorted column header | Rows ordered ascending by that column; its `aria-sort="ascending"`, ▲ shown; other headers `aria-sort="none"`, no indicator | No error expected |
| Reverse | Select the active header again | Descending; `aria-sort="descending"`, ▼ shown | No error expected |
| Switch column | Select a different header | That column ascending; previous header back to `none` | No error expected |
| Keyboard sort | Tab to a header, Enter/Space | Same as selecting it | No error expected |
| Numeric column | Sort offers by "Betrag" (980, 1234.56, 99) | Numeric order (99, 980, 1234.56), not string order; column right-aligned | No error expected |
| Empty table | No rows for a table | Header row plus one centred caption cell with the existing German empty message | No error expected |
| Row added | Add remark/offer | New row appears without reload: at the top by default, at its sorted position when a column is active | On failure: inline error below the form's fields, above its submit; values kept |
| Overview row select | Select anywhere on a tender row | Navigates to `/tenders/:id` | No error expected |

</frozen-after-approval>

## Code Map

All paths under `freight-tenders/frontend/`.

- `src/styles.scss` -- empty today; `angular.json` already lists it as the one global stylesheet. All three component `.scss` files are empty too.
- `src/index.html` -- `lang="en"`, `<title>Frontend</title>`.
- `src/app/tender-overview/tender-overview.{ts,html}` -- `openTenders`/`closedTenders` signals feed two `<ul data-testid="open-tenders|closed-tenders">` of `routerLink` anchors; empty states are `<p data-testid="*-tenders-empty">` *replacing* the list. No status shown.
- `src/app/tender-detail/tender-detail.{ts,html}` -- `tender` signal; `<ul data-testid="remarks|offers">`; `STATUS_LABELS` map and `statusLabel` computed (reuse; move the map to `tender-api.ts` so the overview shares it); status is plain text `<p data-testid="status">`; add-forms append to `tender` via `update` and have no in-flight guard.
- `src/app/tender-create/tender-create.{ts,html}` -- already has `submitting` signal and error-above-submit; markup/classes only.
- `src/app/*/*.spec.ts` -- assert via the testids above; `tender-overview.spec.ts:96` queries `[data-testid="open-tenders"] a`. Keep every existing testid on the equivalent new element.
- `_bmad-output/initiative-demo-app/ux-freight-tenders-ui/mockups/*.html` -- composition reference; its `:root` variables and table/pill/form CSS are a near-direct starting point. Spine wins on conflict.
- Backend `findAll()` is unordered (in practice id ascending); `amount` is a bare `BigDecimal`, no currency.

## Tasks & Acceptance

**Execution:**
- [x] `src/styles.scss` -- define DESIGN.md tokens as CSS custom properties and the shared element/class styles: page container (max-width, desktop/mobile margins), type scale, `.data-table` (header, row border/hover, sort button + indicator, `.numeric`, `.empty-cell`), `.btn-primary`/`.btn-secondary` incl. disabled, `.pill-open`/`.pill-closed`, form label/input/focus ring, `.form-error`, `.state-message`, `.notice` -- one global sheet since all three pages share every component
- [x] `package.json`/`package-lock.json` -- `npm install @fontsource/inter`; import the 400/600/700 weights from `src/styles.scss`
- [x] `src/index.html` -- `lang="de"`, title "Frachtausschreibungen"
- [x] `src/app/table-sort.ts` (+ `table-sort.spec.ts`) -- small generic helper: sort-state type (`column`, `direction`), `toggleSort(state, column)`, `sortRows(rows, state)` (no active column: id descending) comparing numbers numerically and strings with `localeCompare(…, 'de')`, `ariaSort(state, column)` -- one implementation for all four tables
- [x] `src/app/tender-api.ts` -- export `STATUS_LABELS`
- [x] `src/app/tender-overview/tender-overview.{ts,html}` -- page `<h1>` "Ausschreibungen", create link as `.btn-secondary`; each list becomes a `.data-table` (Von, Nach sortable; Status pill column, not sortable) with independent sort state via `computed`; whole row selectable (row click navigates; the Von cell keeps the `routerLink` anchor for keyboard/AT); empty message as a `colspan` cell
- [x] `src/app/tender-detail/tender-detail.{ts,html}` -- route as `<h1>`, status pill, closed explanation as `.notice` before both forms; remarks table (Bemerkung) and offers table (Anbieter, Betrag right-aligned and rendered via `Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' })`), both sortable; forms restyled, error above submit; add `remarkSubmitting`/`offerSubmitting` signals disabling submit while in flight (EXPERIENCE.md State Patterns)
- [x] `src/app/tender-create/tender-create.html` -- `<h1>`, styled fields, `.btn-primary` submit, `.btn-secondary` "Abbrechen"
- [x] `src/app/*/*.spec.ts` -- adapt to table markup; add tests for every matrix row (overview and detail), incl. `aria-sort` values and the empty-table header

**Acceptance Criteria:**
- Given any of the three pages, when rendered, then colours, type scale, radii, and spacing come from the DESIGN.md tokens and exactly one Ford-blue filled button exists per view.
- Given a closed tender's detail page, when it loads, then both forms are `disabled` and one explanation precedes them in DOM order (unchanged behaviour, new styling).
- Given the existing suite, when run after the change, then every pre-existing behaviour assertion still holds.

## Implementation Notes

Implemented by a subagent from this plan; nothing in the frozen block changed.

- `table-sort.ts` also exports `sortIndicator` (▲/▼/null) so the four templates share the indicator logic; equal values fall back to newest-first in both directions.
- The overview builds its two tables from one `tenderTable(...)` factory (own `signal<SortState>` + `computed` rows each) and renders them with a single `@for`, instead of two copied table blocks.
- Row selection: `(click)` on the `<tr>` navigates via `Router`; the Von cell keeps a `routerLink` anchor for keyboard/AT. Clicks on that anchor, modified or non-primary clicks, and the click ending a text selection are left alone.
- Detail status is now only the pill text ("Offen"/"Geschlossen"); the former "Status:" prefix is gone.
- Primary buttons: overview "Neue Ausschreibung erstellen", create "Erstellen", detail "Angebot hinzufügen" ("Bemerkung hinzufügen" is secondary). The task line above said the overview link is secondary; review changed it to primary to satisfy the one-primary-per-view criterion and DESIGN.md.
- New testids for reading order and sort state: `page-title`, `*-row`, `*-link`, `*-header-<col>`, `*-sort-<col>`, `offer-amount`. The old `[data-testid="open-tenders"] a` query became `open-tenders-link`.
- `.data-table` uses `table-layout: fixed` so the stacked overview tables line up; long remarks wrap.
- Keyboard sorting is covered in unit tests only as "header is a real, enabled, focusable `<button>` in a `<th aria-sort>`" (jsdom does not synthesise click from Enter/Space); the key press itself was checked once manually in Chrome on the overview.

Verified after review patches: `npm run build` succeeds; `npm test -- --watch=false` 6 files, 58 tests pass; `npm run lint` clean. The implementer viewed `/`, `/tenders/new`, and an open and a closed detail page in Chrome against a local backend (Inter loads, sorting by click and focus + Enter, closed forms disabled). Not exercised in a browser: submitting any form (add-row position, error placement, in-flight guard are unit-tested only), and the mobile breakpoint.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 0, medium: 0, low: 6, false: 0, maybe-false: 0

- `tender-overview.html` -- overview had no filled Ford-blue button, so "exactly one per view" failed there (the task line and mock said outlined, the criterion and DESIGN.md say one primary action per view). **low**, route: **patch** -- `create-link` is now `.btn-primary`.
- `tender-overview.spec.ts`, `tender-detail.spec.ts` -- new assertions used `querySelector('h1')` and `closest('th')`, against the frontend AGENTS.md `data-testid`-only rule. **low**, route: **patch** -- both `<h1>` carry `data-testid="page-title"`; the detail spec reads `aria-sort` via the `*-header-*` testid.
- `tender-detail.spec.ts` -- a test name claimed right-alignment that nothing asserts; alignment and centring live only in CSS classes, which the testid rule keeps out of assertions and jsdom cannot compute. **low**, route: **patch** for the name (renamed); the missing style assertion itself is rejected -- not assertable under the repo's test rules.
- `tender-overview.ts` `openTender` -- modified/non-primary clicks navigated in place and a drag text-selection in a row ended in navigation. **low**, route: **patch** -- early return on `button !== 0`, any modifier key, or a non-empty selection; one modified-click test added.
- `styles.scss` -- pills (12px/600) and `.form-error`/`.notice` (13px/400) sat off the DESIGN.md type scale (values copied from the mocks). **low**, route: **patch** -- pills on the label step, error/notice on the caption step. The 11px sort-indicator glyph is not text on the scale and stays.
- `styles.scss` mobile query -- `.data-table td.empty-cell` out-specified the mobile padding override. **low**, route: **patch** -- selector added to the media-query list.

Full re-verification after patching: build succeeds, 58/58 tests pass, lint clean. Nothing deferred.

## Design Notes

Sorting is a pure-function helper plus per-table `signal<SortState>` and a `computed` sorted view, not a table component: four tables with different columns and cell content would make a generic component mostly projection plumbing. Because the sorted view is a `computed` over the data signal, an added remark/offer lands at its sorted position for free.

Styles are global rather than per-component: Angular's view encapsulation would force the same table/button/pill rules to be copied into three `.scss` files.

## Verification

**Commands** (in `freight-tenders/frontend`):
- `npm run build` -- expected: build succeeds
- `npm test -- --watch=false` -- expected: all specs pass, incl. the new sorting tests
- `npm run lint` -- expected: no lint errors

**Manual checks (if no CLI):**
- With backend and `npm start` running, compare `/`, `/tenders/new`, and an open and a closed `/tenders/:id` against the two mockups and DESIGN.md; sort each table by mouse and by Tab + Enter/Space.

---
schema_version: 1
story_slug: print-tender-shipment-data
stage: analysis
status: ready-for-review
updated: 2026-10-14T11:28:14Z
---

## Proposal

Frontend-only change. (1) Extract the four "Sendungsdaten" cards (currently inline in tender-detail.html lines 54-142, with their computed text helpers: country labels, bid-deadline text with the heute/abgelaufen hint, weight, loading meters, pallets, equipment, dangerous goods, temperature) into a shared component, so the rows are defined once and the detail page and print view show identical content. The component takes the tender as an input and keeps all existing data-testids (shipment-data, card-*, row ids). The card row styles (.data-row etc.) move from tender-detail.scss into the new component or global styles. The detail page then uses the shared component, so existing detail tests keep passing.
(2) Add a "Drucken" `<a class="btn-secondary" target="_blank" rel="noopener" data-testid="print-tender" [routerLink]>` to the detail header, left of the close button, rendered only in the loaded-tender branch, for any status. Because the header is a flex row, a wrapper action group (or an ordered pair of elements) keeps it at the right end when the close button is absent. At 600px and below the group stacks below the title with the existing wrap rules. The existing `.page-header .btn-secondary` rule already covers the link's no-wrap and shrink behaviour. Add `display: inline-block` / link styling so the anchor looks like the button.
(3) Add a new flat feature folder `src/app/tender-print/` (ts/html/scss/spec) and the route `tenders/:id/print` in app.routes.ts. It parses the id as the detail page does (NaN gives the existing German load-error text), loads via `TenderApiService.detail` with `catchError(() => of(null))`, and holds loading/loadError/tender signals. Template: a screen-only `btn-primary` "Drucken" button (`print-button`, calls `window.print()`, only rendered when a tender is loaded), the `<h1 data-testid="page-title">` route title, `print-meta` line "Ausschreibung {id} · {German status label}" as plain text, the "Sendungsdaten" section via the shared cards component. Loading and error states use the same `loading` and `load-error` testids. The tab title is set with Angular's `Title` service to "Ausschreibung Origin → Destination" after load (the app currently sets no titles, so this is new; the load-error and loading states can keep the default title).
(4) Print styles in the print feature's scss, using global `@page { size: A4 portrait; margin: 15mm; }` (it must be global because @page rules are not scoped by view encapsulation; put it in styles.scss or use ViewEncapsulation.None on the print view, and note that it then applies app-wide, which is acceptable since the story says printing the detail page itself is unchanged apart from paper size, or scope it by enabling it only via the print view). Inside `@media print`: hide the button, force black on white, force `.data-card-grid` to two columns regardless of the 600px breakpoint (the print rule must come after and override the mobile media query), `.data-card { break-inside: avoid; }`, and compact font/spacing so the longest commodity (200 chars wraps within the card) plus dangerous goods and temperature fits one A4 page.
(5) Docs: update freight-tenders/README.md (the /tenders/:id row and a new /tenders/:id/print route row), and EXPERIENCE.md and DESIGN.md, which live under _bmad-output/initiative-demo-app/ux-freight-tenders-ui/ (not under freight-tenders/), with the rows and notes the story lists.

## Subtasks

- Create a shared shipment-data cards component (e.g. src/app/shipment-data/) taking the tender as input, moving the four cards, their text computeds, and the .data-row styles out of tender-detail; keep all existing data-testids; make the detail page use it.
- Run the existing tender-detail spec to confirm the refactor changes nothing.
- Add the 'Drucken' link (data-testid print-tender, target=_blank, rel=noopener, btn-secondary, routerLink to /tenders/:id/print) in the detail header inside an action group left of the close button, only in the loaded-tender branch; adjust styles so it right-aligns when the close button is absent and stacks at <=600px.
- Create src/app/tender-print/ (ts, html, scss, spec) with loading/load-error/tender signals, NaN-id handling, TenderApiService.detail with catchError, the screen-only print-button calling window.print(), page-title, print-meta, and the shared cards component.
- Set the browser tab title to 'Ausschreibung <origin> → <destination>' via Title service once the tender has loaded.
- Register the route tenders/:id/print in app.routes.ts.
- Add print CSS: global @page A4 portrait 15mm margin, hide the button in print, black on white, two-column grid forced in print, break-inside: avoid on cards, compact sizing so worst-case content fits one page.
- Update freight-tenders/README.md, and EXPERIENCE.md and DESIGN.md in _bmad-output/initiative-demo-app/ux-freight-tenders-ui/.
- Run npm run lint, npm run build and npm test -- --watch=false in freight-tenders/frontend.

## Tests

- tender-detail.spec: for open, awarded and closed tenders the print-tender link renders with href ending /tenders/:id/print, target=_blank and rel=noopener.
- tender-detail.spec: print-tender is absent while loading and in the load-error state.
- tender-detail.spec: the existing close-tender tests still pass, and print-tender remains present after closing the tender (close button gone).
- tender-print.spec: shows the German loading message before the response arrives and no print-button or cards.
- tender-print.spec: a 404/error response shows the load-error message and no print-button or cards.
- tender-print.spec: a non-numeric id shows load-error without issuing an HTTP request, and no print-button.
- tender-print.spec: a loaded tender shows page-title with 'Origin → Destination', print-meta 'Ausschreibung 42 · Offen' (id and German status for open/awarded/closed), shipment-data with the four cards and the same row values as the detail page (including the bid-deadline '(heute)'/'(abgelaufen)' suffix).
- tender-print.spec: none of the offers, remarks, back-link, close-tender, award, summary, or form test ids exist in the print view.
- tender-print.spec: clicking print-button calls window.print once (spy), and window.print is not called on load.
- tender-print.spec: document title becomes 'Ausschreibung Hamburg → Rotterdam' after load.
- Shared cards component spec (or detail-spec parity assertion): the same tender rendered in the detail page and the print view gives identical text for every card row test id.
- Manual or browser check (not assertable in jsdom/Vitest): print preview of a tender with a 200-character commodity, dangerous goods with an ADR class and a temperature range fits on one A4 page with two-column cards and no hidden-background dependence. Record this as a manual verification step.

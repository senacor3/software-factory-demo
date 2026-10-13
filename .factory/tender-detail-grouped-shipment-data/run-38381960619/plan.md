---
schema_version: 1
story_slug: tender-detail-grouped-shipment-data
stage: analysis
status: ready-for-review
updated: 2026-10-13T10:15:04Z
---

## Proposal

Frontend-only change to the tender detail page. The dependency story is already in place: TenderDetail carries all shipment fields, tender-format.ts provides formatDate, formatWeight, formatLoadingMeters, formatAmount(amount, currency), formatTemperatureRange, localToday and deadlineHint, and tender-api.ts has EQUIPMENT_LABELS and COUNTRY_LABELS. The plan reuses these so formats match the overview and create form.

In tender-detail.ts, remove the hard-coded EUR formatter and format offer amounts with formatAmount(amount, tender.currency). Add small computed values for the summary line (pickup, delivery, equipment label, weight, joined by " · "), the Angebotsfrist text (date plus "(abgelaufen)" or "(heute)" from deadlineHint and localToday), and the fallback rows (Keine Angabe, Nein / Ja, ADR-Klasse X, Keine Vorgabe / N bis M °C).

In tender-detail.html, add the summary line (data-testid="tender-summary") under the header. Add a "Sendungsdaten" section with four cards (Strecke, Termine, Ladung, Fahrzeug und Konditionen), each an h3 plus a dl with every row always rendered. Move Angebote above Bemerkungen, below the closed-explanation notice. Change the amount label to "Betrag (EUR)" style using the tender currency. Existing data-testids stay, and the new elements live only in the loaded-tender branch so they are absent while loading or on load error.

In styles.scss add a shared flat data-card class (1px outline-variant border, gutter padding, no shadow) and a two-column grid that collapses to one column at 600px and narrower. tender-detail.scss gets minimal summary-line and dl styling. Update EXPERIENCE.md, DESIGN.md, freight-tenders/README.md and mockups/tender-detail.html as the story lists.

## Subtasks

- Read tender-detail.spec.ts, tender-test-data.ts, styles.scss, tender-overview.html and the docs/mockup files to confirm existing conventions and testids
- tender-detail.ts: remove fixed EUR AMOUNT_FORMAT, use formatAmount with the tender currency; add computed summary line, deadline text, and fallback-value helpers using existing label maps and formatters
- tender-detail.html: add summary line, Sendungsdaten section with four cards and dl rows (new data-testids per row), reorder Angebote before Bemerkungen, make amount label include currency
- styles.scss: add shared data-card class and responsive grid (one column at max-width 600px); adjust tender-detail.scss
- Update EXPERIENCE.md (IA row, Component Patterns row, tab order, Flow 1 steps 3-5), DESIGN.md (data card, summary line), freight-tenders/README.md (/tenders/:id row), mockups/tender-detail.html
- Run npm run lint, npm run build and npm test -- --watch=false in freight-tenders/frontend

## Tests

- Summary line shows pickup date, delivery date, vehicle label and weight for a loaded tender
- All four cards render all rows in order, for a tender with and without pallets, dangerous goods and temperature control, showing Keine Angabe / Nein / Keine Vorgabe versus the pallet count, Ja, ADR-Klasse 3 and 2 bis 8 °C
- Open tender with past bid deadline shows (abgelaufen); one due today shows (heute); a closed tender with a past deadline shows neither
- Angebote section precedes Bemerkungen in the DOM; remark/offer add, sort and closed-tender disabled behavior still pass
- Offer amounts are formatted in the tender currency (EUR and CHF) and the amount label names the currency
- No data cards or summary line in loading and load-error states
- Existing detail, overview, create and tender-format specs keep passing; unit tests for any new format helpers

---
schema_version: 1
story_slug: tender-overview-shipment-columns
stage: analysis
status: ready-for-review
updated: 2026-10-13T09:38:13Z
---

## Proposal

Backend: add offerCount (int) and lowestOfferAmount (BigDecimal, nullable) to TenderResponse. TenderResponse.from(Tender) computes them from tender.getOffers(), which covers the create and close responses. The list endpoint must not lazy-load offers once per tender, so listTenders (including the findByStatus path) fetches offers in a single query: either a repository method with @EntityGraph(attributePaths = "offers") / join fetch distinct, or one grouped JPQL query (count and min per tender id) merged into the responses. The detail endpoint is unchanged.

Frontend: add offerCount and lowestOfferAmount to TenderSummary in tender-api.ts, and update tender-test-data.ts and the specs that build summaries. In tender-overview, replace the current layout (Von, Nach, Status) with seven columns: Von, Nach, Abholung, Ladung, Fahrzeug, Angebotsfrist, Angebote. Each cell has a first line and an optional caption second line (typography.caption, on-surface-variant). Von and Nach show the city with country code and postal code below. Abholung shows the dd.MM.yyyy date. Ladung shows weight and loading meters, with "ADR <class>" and "2 bis 8 °C" below, joined by " · ", when they apply. Fahrzeug shows the German label from EQUIPMENT_LABELS. Angebotsfrist shows the deadline, plus "heute" or "abgelaufen" for open tenders only, computed against the browser's local date. Angebote shows the count right-aligned plus "ab <amount> <currency>" when offers exist. Formatting goes through small pure helpers using Intl with the de-DE locale. The Status header and pill are removed, the empty-row colspan becomes 7, and the row link stays in the first column. Existing data-testids are kept.

Sorting: generalize sortableColumns to the six sortable keys, with Fahrzeug as a plain non-sortable th. Add SORT_ACCESSORS for pickupDate, weightKg (Ladung), bidDeadline and offerCount (Angebote), using the first line's underlying value only. ISO date strings sort correctly as strings. Keep the default newest-first order and the aria-sort behavior via table-sort.ts. The column keys must be keyof TenderSummary, so the Ladung column uses weightKg.

Layout: widen the overview page content area to 1200px, either with a page modifier class or a CSS variable override scoped to the overview, while the other pages keep 960px. Wrap each table in a container with overflow-x: auto so the table scrolls inside it and the page never does. Use white-space: nowrap on cells, with a block-level second line inside the cell. Check the existing 378+ media-query rules in styles.scss that restyle .data-table cells on narrow viewports so they do not break the scroll behavior or header alignment. Add two-line cell, caption and numeric alignment styles.

Docs: update freight-tenders/README.md (the GET /api/tenders and / rows), EXPERIENCE.md (overview IA row, the Status pill row in Component Patterns, Flow 1 steps 1-3), DESIGN.md (Components -> Tables for the two-line cell and scroll container, Layout & Spacing for the 1200px overview), and mockups/tender-overview.html (new columns).

## Subtasks

- Backend: add offerCount and lowestOfferAmount to TenderResponse and compute them in from(Tender) from the offers list
- Backend: change listTenders / findByStatus so offers are fetched without per-tender queries (entity graph or grouped aggregate query) and the list controller output includes the new fields
- Backend: update TenderFixtures and existing tests for the new record components
- Frontend: extend the TenderSummary interface and tender-test-data.ts with offerCount and lowestOfferAmount
- Frontend: add pure formatting helpers (dd.MM.yyyy date, German number/weight/ldm/amount, cargo hint line, temperature range, deadline hint relative to local today) with unit tests
- Frontend: rewrite tender-overview.html for the seven columns with two-line cells, remove the Status column and pill, set empty colspan to 7, keep the row link in column 1 and keep existing data-testids
- Frontend: update tender-overview.ts with the six sortable columns, SORT_ACCESSORS for weight, count, pickup date and deadline, and a non-sortable Fahrzeug header
- Frontend: widen the overview content area to 1200px, add a horizontally scrolling table container, nowrap cells, caption and numeric-aligned styles, and verify the existing narrow-viewport media rules
- Update tender-overview.spec.ts: remove the status column tests and add tests for the new cells, hints, sorting and per-table independence
- Docs: update README.md, EXPERIENCE.md, DESIGN.md and mockups/tender-overview.html as listed in the story
- Run mvn -B verify, mvn spotless:check, mvn spotbugs:check, and the frontend build, test, lint and static-analysis commands

## Tests

- TenderControllerTest: GET /api/tenders returns offerCount and lowestOfferAmount for a tender with several offers (correct count and min) and returns 0 / null for a tender with no offers
- TenderControllerTest: the create and close responses also carry offerCount and lowestOfferAmount
- TenderServicePersistenceTest or TenderRepositoryTest (@DataJpaTest): listing N tenders with offers issues a constant number of queries, not N+1 (for example by asserting Hibernate statement counts)
- TenderServiceTest: listTenders with and without a status filter still returns the right tenders
- Frontend formatting helper specs: 18500 -> '18.500 kg', 13.6 -> '13,6 ldm', 1450 -> '1.450,00 €', '2026-10-20' -> '20.10.2026', ADR plus temperature joined by ' · ', and an empty hint when neither applies
- tender-overview.spec.ts: both tables render the seven headers in order and no status header or pill
- tender-overview.spec.ts: a row shows the city plus country code and postal code, the pickup date, the load line, the German vehicle label, the deadline and the offer count
- tender-overview.spec.ts: a dangerous-goods tender shows 'ADR 3', a reefer shows '2 bis 8 °C', and a plain tender has no second line in the Ladung cell
- tender-overview.spec.ts: an open tender with a deadline today shows 'heute', a past deadline shows 'abgelaufen', and a closed tender with such dates shows neither (fake the date)
- tender-overview.spec.ts: a tender with offers shows the count and 'ab <lowest amount>' in the tender's currency, and a tender without offers shows 0 and no amount
- tender-overview.spec.ts: each of the six sortable columns sorts ascending and descending with the right aria-sort, Ladung orders by weight and Angebote by count, sorting one table leaves the other unchanged, and Fahrzeug has no sort button
- tender-overview.spec.ts: the default order is newest first, and the whole-row click and row link still navigate to the tender
- Existing tender-detail, tender-create and tender-api specs still pass with the updated TenderSummary test data

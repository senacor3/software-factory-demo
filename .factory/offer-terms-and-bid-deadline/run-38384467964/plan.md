---
schema_version: 1
story_slug: offer-terms-and-bid-deadline
stage: analysis
status: ready-for-review
updated: 2026-10-13T10:37:19Z
---

## Proposal

Extend the offer model end to end and add a bid-deadline rule.

Backend (flat tender/ package): add deliveryDate, validUntil (LocalDate) and note to the Offer entity, AddOfferRequest and OfferResponse. Bean Validation: supplierName @NotBlank + @Size(max=100); amount unchanged; deliveryDate @NotNull; validUntil @NotNull and today-or-later; note @Size(max=500). The today-or-later check must use the injectable java.time.Clock (as CreateTenderRequestValidator already does) rather than the system clock, and report a violation on the validUntil field in the existing 400 shape. A blank note is normalised to null.

TenderService.addOffer takes the new fields plus the Clock and checks in the story's order: tender exists (404), tender open (existing TenderClosedException, 409), bidDeadline before today (new unchecked BidDeadlinePassedException, 409, mapped in TenderExceptionHandler like TenderClosedException), then deliveryDate before the tender's pickupDate (a small domain exception mapped to the existing 400 shape with a violations entry for deliveryDate). All comparisons are inclusive. Remarks are untouched. The controller passes the request through.

Frontend: extend OfferSummary and TenderApiService.addOffer with the five fields. The offers table gets five columns (Anbieter, Betrag, Zustellung, Gültig bis, Hinweis); the first four are sortable via the existing sortRows/toggleSort (ISO date strings sort correctly). Zustellung shows a caption second line "nach Wunschtermin" when the offer's deliveryDate is strictly after the tender's deliveryDate; Gültig bis shows "abgelaufen" when validUntil is before localToday(). The add-offer form gains Zustellung am, Gültig bis and Hinweis (optional) with validators mirroring the backend and a German message under each invalid touched field. When an open tender's bidDeadline is before the browser's today, disable the offer form (fields and button) and show the German notice above it; the remark form stays enabled; a closed tender shows only the existing closed explanation. A failed addOffer (including 409) shows the existing offer error and keeps the entered values (the form is only reset on success, as now).

Docs: update freight-tenders/README.md (offers endpoint row, error paragraph) and EXPERIENCE.md (add-offer form row in Component Patterns, State Patterns row "Bid deadline passed", Flow 1).

## Subtasks

- Add deliveryDate, validUntil, note to Offer entity (blank note -> null), AddOfferRequest (with validations incl. supplierName max 100, note max 500) and OfferResponse; check how the schema is managed (ddl-auto vs SQL) and update accordingly
- Implement a Clock-based validUntil today-or-later constraint reporting on the validUntil field
- Create BidDeadlinePassedException and a deliveryDate-before-pickupDate exception; map them in TenderExceptionHandler (409 and 400 with violations entry for deliveryDate)
- Update TenderService.addOffer (inject Clock) to apply checks in order: 404, closed 409, deadline 409, delivery-before-pickup 400; update TenderController call
- Update TenderFixtures and existing backend tests to the new offer shape
- Extend frontend OfferSummary and TenderApiService.addOffer; update tender-test-data
- Add helper(s) in tender-format.ts for expired validity / late delivery / deadline passed using localToday()
- Rebuild the offers table in tender-detail.html with five columns, four sortable headers, and the caption hints
- Extend offerForm with deliveryDate, validUntil, note and validators incl. cross-field deliveryDate >= pickupDate; render German per-field messages for touched invalid fields
- Disable the offer form and show the deadline-passed notice for open tenders past their deadline (not when closed); keep the remark form enabled
- Update README.md and EXPERIENCE.md
- Run mvn -B verify, mvn spotless:check, mvn spotbugs:check, and npm ci/build/test/lint/static-analysis

## Tests

- TenderControllerTest: valid offer returns 201 with all five fields and appears in tender detail
- TenderControllerTest: missing/past validUntil, missing deliveryDate, deliveryDate before pickupDate, note of 501 chars, supplierName of 101 chars each return 400 with violations entry for that field and nothing is stored
- validUntil equal to today and deliveryDate equal to pickupDate are accepted; blank note returned as null
- Service/controller tests with fixed Clock: offer on bidDeadline day accepted; day after returns 409 and is not stored; remark the day after still accepted
- Closed tender with passed deadline returns the existing closed 409, not the deadline error
- Persistence test: new Offer columns round-trip through the repository
- tender-detail.spec: five columns rendered; 'nach Wunschtermin' and 'abgelaufen' hints shown only when applicable; sorting asc/desc on the four sortable columns, Hinweis not sortable
- tender-detail.spec: add-offer form sends all fields via HttpTestingController, adds row without reload, shows per-field German errors for invalid touched fields
- tender-detail.spec: open tender past deadline disables offer fields/button and shows notice, remark form enabled; closed tender shows only the closed explanation; 409 shows offer error and keeps entered values
- tender-api.spec: addOffer posts all fields
- tender-format.spec: tests for new helpers

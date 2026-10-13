---
schema_version: 1
story_slug: offer-terms-and-bid-deadline
stage: analysis
status: ready-for-review
updated: 2026-10-13T10:27:54Z
---

## Proposal

Extend the offer through the full stack, with the backend authoritative and the frontend mirroring its rules.

Backend (flat `tender/` package):
- Add `deliveryDate`, `validUntil` and `note` to `Offer`, `AddOfferRequest` and `OfferResponse`.
- `AddOfferRequest` uses Bean Validation: `supplierName` is `@NotBlank @Size(max=100)`, `amount` keeps `@NotNull @DecimalMin("0.01")`, `deliveryDate` is `@NotNull`, `validUntil` is `@NotNull @FutureOrPresent`, `note` is `@Size(max=500)`.
- `@FutureOrPresent` would use the system clock, but "today" must come from the injectable `Clock`. So `validUntil >= today` is either checked in `TenderService` with a `400` and a `violations` entry for `validUntil`, or done with a Clock-aware validator. The service route is simpler and keeps one place that knows about `Clock`.
- A blank `note` is normalised to `null` before it is stored.
- `TenderService.addOffer` takes the request fields and the `Clock`. It checks in this order: tender exists (`404`), open (`409`, existing `TenderClosedException`), bid deadline not passed (new `BidDeadlinePassedException`, `409`, when `bidDeadline` is before today and the deadline day itself is accepted), then `deliveryDate >= pickupDate`. A violation of that last check is thrown as a new unchecked exception that carries the field name and is mapped in `TenderExceptionHandler` to `400` with a `violations` entry for `deliveryDate`.
- Request validation (`400`) naturally runs first via `@Valid`.
- Remarks are untouched.
- `TenderExceptionHandler` maps the new deadline exception exactly like `TenderClosedException`.
- Update the controller to pass the new fields, and update test fixtures to the new offer shape.

Frontend:
- `OfferSummary` and `TenderApiService.addOffer` gain the three fields.
- The offers table gets five columns (Anbieter, Betrag, Zustellung, Gültig bis, Hinweis). Zustellung shows a "nach Wunschtermin" caption line when the offer's `deliveryDate` is strictly after the tender's `deliveryDate`. Gültig bis shows an "abgelaufen" caption line when `validUntil` is before the browser's local today.
- The four date and text columns are sortable through the existing `table-sort` helpers, and ISO date strings sort correctly as strings. Hinweis is not sortable.
- The offer form gets "Zustellung am", "Gültig bis" and "Hinweis (optional)" controls with Validators mirroring the backend and German per-field messages for touched invalid fields.
- A `computed` signal `bidDeadlinePassed` is true when the tender is open and `bidDeadline` is before the browser's local today. When true, the offer form is disabled and the notice "Die Angebotsfrist ist am dd.MM.yyyy abgelaufen, daher können keine weiteren Angebote hinzugefügt werden." is shown. The remark form stays enabled. A closed tender keeps its existing single explanation, without this notice.
- A `409` or other failure reuses the existing offer error message and keeps the entered values. The form is only reset on success, which the current code already does.

Docs: update the `freight-tenders/README.md` offers endpoint row and error paragraph, plus the add-offer form row in `EXPERIENCE.md` Component Patterns, a new "Bid deadline passed" State Patterns row, and Flow 1.

## Subtasks

- Backend: add deliveryDate, validUntil and note to Offer entity, AddOfferRequest (with Bean Validation annotations incl. @Size(max=100) on supplierName and @Size(max=500) on note) and OfferResponse
- Backend: create BidDeadlinePassedException (unchecked, message via super) and map it to 409 in TenderExceptionHandler; add an exception and handler mapping producing a 400 with a violations entry for deliveryDate
- Backend: update TenderService.addOffer to take the Clock and the new fields, enforce the order 404 -> closed 409 -> deadline 409 -> deliveryDate >= pickupDate 400, enforce validUntil >= today via the Clock (400 with a validUntil violation), and normalise a blank note to null
- Backend: update TenderController, TenderFixtures and existing tests to the new offer shape
- Frontend: extend OfferSummary and TenderApiService.addOffer with deliveryDate, validUntil and note; update tender-test-data
- Frontend: add the three form controls with validators and German error messages to the offer form in tender-detail.ts/html, and send all fields on submit
- Frontend: render the five-column offers table with the 'nach Wunschtermin' and 'abgelaufen' caption hints, using the browser's local date; make Anbieter, Betrag, Zustellung and Gültig bis sortable
- Frontend: add the bidDeadlinePassed computed signal, disable the offer form and show the German notice (not for closed tenders), keep the remark form enabled
- Update freight-tenders/README.md (offers endpoint row, error paragraph) and EXPERIENCE.md (add-offer form row, 'Bid deadline passed' state row, Flow 1)
- Run mvn -B verify, mvn spotless:check and mvn spotbugs:check on the backend; run npm run build, npm test -- --watch=false, npm run lint and npm run static-analysis on the frontend

## Tests

- TenderControllerTest: valid offer returns 201 with all five fields, and it appears in the tender detail response
- TenderControllerTest: missing or past validUntil, missing deliveryDate, note longer than 500 chars, and supplierName longer than 100 chars each return 400 with a violations entry for that field and store nothing
- TenderServiceTest with a fixed Clock: validUntil equal to today is accepted; deliveryDate equal to pickupDate is accepted; deliveryDate before pickupDate returns 400 with a deliveryDate violation
- TenderServiceTest: an offer on the bidDeadline day is accepted, an offer the day after throws BidDeadlinePassedException (409) and is not stored, and a remark the day after is still accepted
- TenderServiceTest/ControllerTest: a closed tender with a passed deadline returns the existing closed 409, not the deadline error
- TenderServiceTest: a blank or missing note is stored and returned as null
- tender-detail.spec.ts: the five columns render, 'nach Wunschtermin' shows only when the offer's deliveryDate is strictly after the tender's deliveryDate, and 'abgelaufen' shows only when validUntil is before today (with the date mocked)
- tender-detail.spec.ts: sorting each of the four sortable columns works in both directions, Hinweis has no sort control, and the hints do not affect the order
- tender-detail.spec.ts: submitting the form POSTs all fields, the new row appears without a reload, and invalid touched fields show German messages
- tender-detail.spec.ts: an open tender past its deadline shows the notice, disables the offer fields and button, and leaves the remark form enabled; a closed tender shows only its existing explanation; a 409 shows the offer error and keeps the entered values
- tender-api.spec.ts: addOffer POSTs the five-field body

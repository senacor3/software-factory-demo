---
schema_version: 1
story_slug: edit-open-tender
stage: analysis
status: ready-for-review
updated: 2026-10-14T11:27:02Z
---

## Proposal

Add edit support to the freight-tenders demo app, backend and frontend together.

Backend (flat tender/ package): add PUT /api/tenders/{id} to TenderController. It takes the same CreateTenderRequest body and returns TenderResponse with 200. Check order is: tender exists (404), body valid (400), tender OPEN (409), locked fields unchanged (409).

Main design point: CreateTenderRequestValidator is a class-level constraint that always applies the "today or later" rules to pickupDate and bidDeadline. On PUT those rules apply only to a date that differs from the stored value, which bean validation cannot know. Split the validator so the relative and conditional rules (delivery vs pickup, deadline vs pickup, ADR, temperature, reefer) are shared, and the two past-date checks are a separate step. Create keeps running both. For PUT, the service loads the tender first (404), runs the shared rules plus the past-date checks only for changed dates, and reports violations under the same field names in the existing 400 violations shape through TenderExceptionHandler. It then checks OPEN (409, reusing TenderClosedException) and, if the tender has any offers (expired or not), the locked fields (409, a new exception whose message names the differing fields).

Also add Tender.update(...) as a plain mutator that replaces only the shipment fields, and TenderService.updateTender(id, request). Locked fields are compared by value: loadingMeters via compareTo, null-safe equality for optional fields, addresses field by field, text exactly. With offers, only deliveryDate and bidDeadline may differ. Extending a passed bidDeadline needs no extra code because addOffer already reads the stored deadline.

Frontend: add TenderApiService.update(id, data). Add the route /tenders/:id/edit. Show a "Bearbeiten" link (btn-secondary, data-testid edit-tender) left of the close button on the detail page, only while the tender is open, with the mobile stacking. Extract the create form's fields, groups, validators and messages into one shared form component or helper used by TenderCreate and a new TenderEdit page, so they are defined once. The edit page covers: loading, load error, not-editable and locked-fields-notice states, prefill including the conditional fields, Speichern disabled while invalid, unchanged or in flight, the 409 and generic error alerts, and navigation to /tenders/:id on success. The "today or later" checks apply only to changed dates, and locked fields are disabled but still sent at their stored values. Create page behavior and its data-testids stay unchanged.

Docs: update freight-tenders/README.md (tender description, PUT row, error paragraph, /tenders/:id and /tenders/:id/edit rows) and EXPERIENCE.md (IA row, form component pattern, "Tender with offers: locked fields" state row, correcting-a-tender flow).

## Subtasks

- Backend: refactor CreateTenderRequestValidator so the past-date rules can be applied separately from the shared cross-field rules; keep create behavior identical
- Backend: add Tender.update(...) mutator that replaces shipment fields only
- Backend: add a locked-fields exception (409) and map it, plus the update 400 violations path, in TenderExceptionHandler
- Backend: implement TenderService.updateTender with order 404, 400, OPEN 409, locked 409, value-based locked-field comparison, and past-date checks only for changed dates
- Backend: add PUT /api/tenders/{id} to TenderController returning TenderResponse
- Backend: add tests for the service, controller and validation cases
- Frontend: add TenderApiService.update(id, data) with a spec
- Frontend: extract the shared tender form (fields, groups, validators, messages) and refactor TenderCreate to use it without changing its behavior or testids
- Frontend: build the TenderEdit page with prefill, locked fields, notice, states, error alerts, change-dependent date rules and disabled-save logic; register /tenders/:id/edit
- Frontend: add the Bearbeiten link to the detail page, shown only for open tenders, with responsive stacking
- Frontend: write specs for TenderEdit and the detail-page link
- Update freight-tenders/README.md and EXPERIENCE.md as specified
- Run mvn -B verify, spotless:check, spotbugs:check, npm run lint, npm run build and npm test -- --watch=false

## Tests

- PUT on an open tender without offers returns 200; GET by id and the list show the new values; id, status and remarks are unchanged
- One rejecting PUT case per create rule returns 400 with a violation naming the field and leaves the tender unchanged
- A tender with a past bidDeadline: PUT repeating that date returns 200; PUT changing it to another past date returns 400 with a bidDeadline violation; same for pickupDate
- PUT on an unknown id returns 404; on an awarded or closed tender returns 409; an invalid body on a closed tender returns 400
- A tender with an offer: changing deliveryDate or bidDeadline returns 200; changing any other field (including currency) returns 409 naming the field and leaves the tender unchanged
- Repeating the stored values with loadingMeters 13.60 against 13.6 is not treated as a change; absent optional fields equal stored nulls
- Extending a passed bidDeadline to today or later makes POST /api/tenders/{id}/offers succeed again
- A no-op PUT returns 200
- Frontend: the detail page shows Bearbeiten linking to /tenders/:id/edit for open tenders and not for awarded or closed ones
- Frontend: the edit page prefills including the conditional ADR and temperature fields; Speichern is disabled until a valid change is made and while in flight
- Frontend: saving sends a complete PUT and navigates to /tenders/:id; Abbrechen and the back link navigate without a request
- Frontend: with offers, the locked-fields-notice is shown, only delivery and bid deadline are enabled, and the PUT still carries the full data
- Frontend: a 409 and a generic failure each show their German role=alert message and keep the entered values
- Frontend: loading, load-error, non-numeric id and not-editable states render as specified, with the back link in all of them
- Frontend: the today-or-later rule is checked only for changed dates
- The existing create page specs and backend create tests keep passing unchanged

---
schema_version: 1
story_slug: edit-open-tender
stage: analysis
status: ready-for-review
updated: 2026-11-04T08:16:51Z
---

## Proposal

Add PUT /api/tenders/{id} and an edit page that reuses the create form, with all state and ordering rules from the story (404, then 400, then 409 for non-OPEN, then 409 for locked fields).

**Backend (`freight-tenders/backend`, flat `tender/` package).**
- Reuse `CreateTenderRequest` as the PUT body. `@Valid @RequestBody` can't be used on the controller as-is, for two reasons. The class-level `@ValidCreateTenderRequest` applies the "today or later" rules unconditionally. Spring would also validate the body before the tender is looked up, which breaks the 404-before-400 order.
- Fix both by splitting the validator logic. Extract the cross-field rules (delivery not before pickup, deadline not after pickup, ADR and temperature rules) and the "today" rules into a shared helper that returns a list of `Violation`s. `CreateTenderRequestValidator` keeps calling it with "check today" on for both dates, so create is unchanged.
- The PUT path takes the body without `@Valid`. The service loads the tender (`TenderNotFoundException`, 404). It then runs field-level Bean Validation through an injected `jakarta.validation.Validator`, using the shared helper with the stored `Tender` so a "today" rule fires only for a date that differs from the stored value. Any violations are thrown as a new `TenderValidationException` carrying the `Violation`s. `TenderExceptionHandler` maps it to the existing 400 shape. Field names match create.
- Two options for the field-level step. Either make the class-level constraint skippable (for example a validation group, or by moving it off the record), or split `CreateTenderRequest` into field constraints plus an explicit validator call. Pick whichever keeps `POST` untouched.
- After validation, reject a non-OPEN tender with the existing `TenderClosedException`/`rejectIfClosed` (409). If the tender has any offers, compare the locked fields to the stored values and throw a new `TenderFieldsLockedException` (409) when any differ.
- The locked fields are everything except `deliveryDate` and `bidDeadline`. Compare by value: `BigDecimal.compareTo` for `loadingMeters`, null-equals-absent for the optional fields, exact string equality for text, and `Address` field by field. The message names the differing fields. Add the handler to `TenderExceptionHandler`.
- Add `Tender.update(...)`, a plain mutator that replaces the 16 data fields and leaves id, status, remarks, offers and `awardedOffer` alone. The service saves it and the controller returns `TenderResponse.from(tender)` with 200.
- Because the check order is fixed, an invalid body on a closed tender returns 400 and not 409.
- Extending a passed `bidDeadline` makes `addOffer` succeed again with no further change, since `addOffer` already reads the stored deadline.

**Frontend (`freight-tenders/frontend`).**
- Add `TenderApiService.update(id, data)`, a `PUT` taking the same typed object as `create`.
- Make the form shared so fields, groups and messages are defined once. Extract the form-building, `ERROR_MESSAGES`, `toRequest`, the toggle and revalidation logic and the template out of `tender-create` into a shared form component with a `mode` input (create or edit), an initial value, locked-state and submit-label inputs, and a submit output. `tender-create` becomes a thin host, so the create page and its existing `data-testid`s behave as before. Add a new `tender-edit` page for `/tenders/:id/edit`.
- Change the validators for edit so `pickupNotInPast` and `deadlineNotInPast` only fire when the value differs from the loaded value. Give them an optional "original value" source, such as a factory taking a getter or a per-control signal.
- The edit page parses the `id` param, and a non-numeric id or load error shows the detail page's load-error message. It loads via `detail(id)` and shows "Ausschreibung wird geladen…" while loading. A non-OPEN tender shows `data-testid="not-editable"` and no form. The back link "Zurück zur Ausschreibung" renders in all of these states.
- Patch the form with the stored values, including the ADR class and temperature range, whose controls are enabled when their checkbox is checked. Make "Speichern" disabled when the form is invalid, pristine or equal to the loaded values, or while submitting.
- If the tender has offers, show `data-testid="locked-fields-notice"` and disable every control except `deliveryDate` and `bidDeadline`. Disabled controls are still sent, because `toRequest` uses `getRawValue()`.
- On success navigate to `/tenders/:id`. A 409 shows the "nicht mehr in dieser Form geändert" message and any other failure shows the generic save-error message, both with `role="alert"` above the buttons and with entered values kept. "Abbrechen" and the back link are `routerLink`s to the detail page, with no request and no confirmation.
- Add the `/tenders/:id/edit` route in `app.routes.ts`.
- On the detail page add the "Bearbeiten" `<a routerLink>` (`data-testid="edit-tender"`, `btn-secondary`) directly left of the close button. Show it only when `isOpen()`, and extend the existing 600px stacking rule to cover it.

**Docs.** Update `freight-tenders/README.md` (tender description, `PUT` row, 409 cases in the error paragraph, `/tenders/:id` and `/tenders/:id/edit` rows). Update `EXPERIENCE.md` (information-architecture row, form component-pattern row, state-patterns row "Tender with offers: locked fields", and a correcting-a-tender flow).

## Subtasks

- Backend: extract the cross-field and 'today' rules from CreateTenderRequestValidator into a reusable helper producing Violations, keeping POST behaviour identical (existing TenderCreateValidationTest must stay green)
- Backend: add Tender.update(...) replacing the 16 data fields without touching id, status, remarks, offers or awardedOffer
- Backend: add TenderValidationException (400 with violations) and TenderFieldsLockedException (409 naming the differing fields); map both in TenderExceptionHandler
- Backend: add TenderService.updateTender(id, request) with the order 404 -> 400 -> 409 not-OPEN -> 409 locked fields; 'today' rules apply only to dates that differ from the stored value; relative rules always apply
- Backend: implement value-based locked-field comparison (BigDecimal compareTo for loadingMeters, null-equals-absent for optional fields, exact text compare, Address field by field), counting every offer including expired ones
- Backend: add PUT /{id} to TenderController returning TenderResponse (200)
- Frontend: add TenderApiService.update(id, data) and its spec
- Frontend: extract the shared tender form (fields, groups, ERROR_MESSAGES, toRequest, toggle/revalidate logic, template) from tender-create into a component with create/edit modes; keep the create page and all its data-testids unchanged
- Frontend: make pickupNotInPast and deadlineNotInPast depend on the loaded value so the 'today or later' check applies only to changed dates
- Frontend: add the tender-edit page and the /tenders/:id/edit route with the loading, load-error, non-numeric-id and not-editable states, prefill including conditional fields, the locked-fields notice and disabled controls, the dirty/valid/in-flight gating of Speichern, success navigation, Abbrechen/back link, and the 409/generic error alerts
- Frontend: add the 'Bearbeiten' link to the detail page header for open tenders and extend the 600px stacking styles
- Docs: update freight-tenders/README.md and EXPERIENCE.md as listed in the story
- Run mvn -B verify, mvn spotless:check, mvn spotbugs:check, npm run lint, npm run build and npm test -- --watch=false

## Tests

- TenderControllerTest/TenderServiceTest: PUT on an open tender with no offers returns 200; a following GET and the list return the new values, with id, status and remarks unchanged
- PUT with one rejecting case per create rule (each field rule and cross-field rule) returns 400 with a violation naming the field, and the tender is unchanged
- PUT on a tender whose bidDeadline (and, separately, pickupDate) is in the past: repeating the stored date returns 200; changing it to a different past date returns 400 with a bidDeadline (or pickupDate) violation; the relative rules still apply
- PUT on an awarded or closed tender returns 409 with the tender unchanged; an unknown id returns 404; an invalid body on a closed tender returns 400, not 409
- PUT on a tender with an offer: changing only deliveryDate and/or bidDeadline returns 200; changing any locked field (including currency) returns 409 naming that field and leaves the tender unchanged
- PUT on a tender with an offer, repeating the stored values with loadingMeters 13.60 vs stored 13.6, and an absent palletCount vs stored null, is not a change and returns 200
- A tender with only expired offers still counts as having offers and is locked
- PUT with unchanged data returns 200
- PUT that extends a passed bidDeadline to today or later makes POST /api/tenders/{id}/offers succeed again
- TenderCreateValidationTest remains green, proving the refactor did not change create behaviour
- tender-api.spec: update() sends PUT /api/tenders/{id} with the full body
- tender-edit.spec: shows the loading message; shows the load-error message for a failed load and for a non-numeric id; shows not-editable with no form for awarded and closed tenders; the back link is rendered in all of these states
- tender-edit.spec: the form is prefilled including ADR class and temperature range, and Speichern is disabled while unchanged, invalid or in flight
- tender-edit.spec: with offers, the locked-fields-notice is shown and only deliveryDate and bidDeadline are enabled, and the PUT body still carries the complete data with locked fields at their stored values
- tender-edit.spec: a past date equal to the loaded value is valid, while a changed past date shows the in-past message
- tender-edit.spec: a successful save navigates to /tenders/:id; 409 and other errors show the right German alert and keep the entered values; Abbrechen and the back link navigate without a request
- tender-detail.spec: the edit-tender link is present for an open tender with href /tenders/:id/edit and absent for awarded and closed tenders
- tender-create.spec: the existing tests pass unchanged against the refactored shared form

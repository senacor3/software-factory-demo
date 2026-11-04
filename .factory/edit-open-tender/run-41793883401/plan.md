---
schema_version: 1
story_slug: edit-open-tender
stage: analysis
status: ready-for-review
updated: 2026-11-04T07:41:17Z
---

## Proposal

Add `PUT /api/tenders/{id}` to the backend and an edit page at `/tenders/:id/edit` to the frontend. The edit page reuses the create form, which is moved into a shared definition. The story is detailed and its dependencies are already in the repo, so no design decision needs the author.

**Backend (`freight-tenders/backend/.../tender/`)**
- `TenderController.updateTender` takes `@PathVariable id` and a `CreateTenderRequest` body. It does not use `@Valid`, because the 404, then 400, then 409 order requires loading the tender first. It returns `TenderResponse` with status 200.
- `TenderService.updateTender(id, request)` runs the checks in the story's order:
  1. Load the tender, or throw `TenderNotFoundException` (404).
  2. Validate the body (400).
  3. Call `rejectIfClosed`, which gives 409 for AWARDED or CLOSED tenders.
  4. If the tender has offers (any, expired or not), compare the locked fields and throw a new `TenderLockedFieldsException` (409) naming the differing fields.
  5. Apply the new values through a new `Tender.update(...)` mutator. Id, status, remarks, offers and awardedOffer are untouched.
- Step 2 reuses the existing field constraints on `CreateTenderRequest` through the injected `jakarta.validation.Validator`.
- The "today or later" rules for `pickupDate` and `bidDeadline` apply only when the request changes the date, so they cannot be evaluated without the stored tender. `CreateTenderRequestValidator` is therefore refactored into a shared rule set with a `today` argument and a per-field "past dates allowed" input.
  - Create passes "never allowed", so its behaviour stays identical.
  - Update passes the stored dates, and a date equal to the stored value skips the past check.
  - The relative rules always apply: delivery not before pickup, deadline not after pickup, and the ADR and temperature rules.
- Because a manual validation call no longer goes through `MethodArgumentNotValidException`, violations are collected into a new unchecked `InvalidTenderException` (carrying `List<Violation>`). `TenderExceptionHandler` maps it to the existing 400 shape with the same field names as on create.
- Locked-field comparison is by value:
  - `loadingMeters` uses `compareTo` (13.6 equals 13.60).
  - Absent values equal a stored null.
  - Address fields, `dangerousGoods`, `temperatureControlled`, `equipmentType`, `currency` and the others use `Objects.equals`.
  - Text is compared exactly, without trimming.
  - Only `deliveryDate` and `bidDeadline` may differ.
- `TenderExceptionHandler` maps the new locked-fields exception to 409 in the standard error shape.

**Frontend (`freight-tenders/frontend/src/app/`)**
- Extract the form definition (the group, validators, `ERROR_MESSAGES`, `toRequest`, the conditional-field toggling and the template) so the fields, groups and messages are defined once. Use either a shared form component with a `mode` input or a shared form factory. The create page keeps its behaviour and existing `data-testid` values.
- In `tender-create-validators.ts`, make `pickupNotInPast` and `deadlineNotInPast` skip the check when the value equals the loaded original. In create mode the original is empty, so the rule is unchanged.
- New `tender-edit/` page, flat folder, with `inject()` and signals:
  - It parses the id from the route. A non-numeric id or a load error shows the detail page's existing error message.
  - It shows "Ausschreibung wird geladen…" while loading.
  - A non-OPEN tender shows `not-editable` and no form.
  - Otherwise it patches the form with the stored values, including the ADR class and temperature fields when they apply.
  - "Speichern" is disabled when the form is invalid, pristine or equal to the loaded values, or while submitting.
  - On success it navigates to `/tenders/:id`.
  - It maps 409 and other failures to the two German `role="alert"` messages and keeps the entered values.
  - When `offers.length > 0` it shows `locked-fields-notice` and disables every control except `deliveryDate` and `bidDeadline`, still sending the full `getRawValue()`-based request.
  - The back link and "Abbrechen" go to `/tenders/:id` without a request. The back link renders in all states.
- `TenderApiService.update(id, data)` issues `PUT /api/tenders/{id}` with the same typed object as `create`. A 409 must be distinguishable from other errors on the edit page, so `update` either returns the error status or the page uses a status-aware error path. This stays inside `tender-api.ts` and does not add an interceptor.
- Add the route in `app.routes.ts`. In the detail page's action group, add a "Bearbeiten" `<a>` (`btn-secondary`, `data-testid="edit-tender"`, `routerLink` to `/tenders/:id/edit`) left of the close button. It is shown only while the tender is OPEN and stacks at 600px and narrower, like the close button.

**Docs**
- `freight-tenders/README.md`: tender description, `PUT` row, the new 409 cases in the error paragraph, and the `/tenders/:id` and `/tenders/:id/edit` rows.
- `EXPERIENCE.md`: the Information Architecture row, the form Component Patterns row, the State Patterns row "Tender with offers: locked fields", and a correcting-a-tender flow.

## Subtasks

- Backend: refactor CreateTenderRequestValidator's rules into a reusable form that takes 'today' and the stored pickupDate/bidDeadline, so the 'today or later' rules apply only to changed dates; create behaviour stays identical
- Backend: add Tender.update(...) mutator that replaces the 16 data fields only
- Backend: add TenderLockedFieldsException (409, names differing fields) and InvalidTenderException (400 with violations); map both in TenderExceptionHandler
- Backend: add TenderService.updateTender with check order 404 -> 400 -> 409 not-open -> 409 locked fields, value-based comparison (BigDecimal compareTo, null equals absent, exact text)
- Backend: add PUT /api/tenders/{id} in TenderController returning TenderResponse (200)
- Backend: add tests (controller, service, persistence) covering every acceptance case; run mvn -B verify, spotless:apply/check, spotbugs:check
- Frontend: extract the shared tender form (group, validators, error messages, toRequest, conditional toggling, template) so create and edit share one definition; make the past-date validators skip a value equal to the loaded original
- Frontend: add TenderApiService.update(id, data) with a way to tell 409 from other failures; add spec
- Frontend: build the tender-edit page (loading, load-error, not-editable states, prefill, dirty/valid/in-flight gating, locked-fields notice and disabling, error alerts, navigation on success, back link and Abbrechen) and register /tenders/:id/edit
- Frontend: add the 'Bearbeiten' link to the detail page header for OPEN tenders with the responsive stacking
- Frontend: add/update specs for edit page, detail page link and create page regression; run npm run lint, npm run build, npm test -- --watch=false
- Docs: update freight-tenders/README.md and EXPERIENCE.md as specified

## Tests

- PUT on an open tender without offers returns 200; GET by id and GET list show the new values and id, status and remarks are unchanged
- One rejecting PUT case per create rule returns 400 with a violations entry naming the field, tender unchanged
- Stored past bidDeadline: PUT repeating that date returns 200; PUT with a different past date returns 400 with a bidDeadline violation; same for pickupDate
- The relative rules (delivery not before pickup, deadline not after pickup) still return 400 on PUT even when dates are unchanged
- PUT on an awarded or closed tender returns 409; unknown id returns 404; an invalid body to a closed tender returns 400, not 409
- Tender with an offer: changing deliveryDate and/or bidDeadline returns 200; changing commodity, currency, pickupDate or an address field returns 409 naming the field and leaves the tender unchanged
- Tender with an offer: repeating stored values with loadingMeters 13.60 and absent palletCount/adrClass/temperature values is not treated as a change (200)
- Extending a passed bidDeadline to today (fixed Clock) makes POST /api/tenders/{id}/offers succeed again
- PUT with identical data returns 200; PUT leaves remarks and offers attached
- Existing create validation tests still pass unchanged after the validator refactor
- Frontend tender-api.spec: update() sends PUT /api/tenders/{id} with the full body
- Frontend edit spec: loading message; load error and non-numeric id show the detail page error; non-open tender shows not-editable and no form
- Frontend edit spec: form prefilled including ADR class and temperature range; Speichern disabled when unchanged, invalid or in flight and enabled after a valid change
- Frontend edit spec: success sends complete data via PUT and navigates to /tenders/:id; Abbrechen and back link navigate without any request
- Frontend edit spec: tender with offers shows locked-fields-notice, only deliveryDate and bidDeadline are enabled, and the request carries locked fields at stored values
- Frontend edit spec: a 409 and a generic failure each show their German role=alert message and keep entered values
- Frontend validator spec: past pickupDate/bidDeadline equal to the loaded value is accepted, a changed past date is rejected
- Frontend detail spec: edit-tender link shown with href /tenders/:id/edit for OPEN tenders, absent for AWARDED and CLOSED
- Frontend create spec: existing tests and data-testid values unchanged

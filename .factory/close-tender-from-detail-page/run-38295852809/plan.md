---
schema_version: 1
story_slug: close-tender-from-detail-page
stage: analysis
status: ready-for-review
updated: 2026-10-12T19:11:16Z
---

## Proposal

Frontend-only change plus a README update; no backend change.

Add `close(id)` to `TenderApiService` (`POST /api/tenders/${id}/close`). The endpoint returns a `TenderResponse` (id, origin, destination, status), not remarks or offers, so type the result as `TenderSummary`. The detail page must not replace its `tender` signal with that result, or the remarks and offers tables would be wiped. Instead `TenderDetail` merges only the status: `tender.update(v => v && { ...v, status: result.status })`.

In `tender-detail.ts`, add `closing` and `closeError` signals, a German `CLOSE_ERROR_MESSAGE` constant, and an `onClose()` handler. It follows the existing add-remark pattern. It returns early if there is no tender or a close is already in flight, sets `closing`, clears the error, and calls `tenderApi.close(id).pipe(catchError(() => of(null)))`. On null it sets the error and leaves the tender open. On success it merges the status and calls `remarkForm.disable()` and `offerForm.disable()`, mirroring what `ngOnInit` does for an already-closed tender. The existing `isClosed()` computed then drives the "Geschlossen" pill and the closed explanation, which already sits above both forms.

In `tender-detail.html`, inside the loaded-tender block, render a `type="button"` `btn-secondary` "Ausschreibung schließen" (`data-testid="close-tender"`) only when `!isClosed()`. It is `[disabled]="closing()"` and sits in or just under the page header. The German error paragraph (`data-testid="close-error"`, reusing the `form-error` class) appears next to it when set. The action disappears once the tender is closed, and a tender that loads closed never shows it. `btn-primary` stays on "Angebot hinzufügen" only. No dialog is added. Add minimal SCSS in `tender-detail.scss` only if the header needs layout for the button and error.

Update `freight-tenders/README.md`. In the `TenderDetail` table row and the paragraph around line 65, replace "There is no UI for closing a tender; that is done through the API only" with a description of the close action. In the "Running both together" section, drop the "Closing a tender has no UI; call the API directly" wording. The curl example can stay as an API illustration if reworded.

Overview behavior ("Geschlossene Ausschreibungen") needs no change, since the overview reloads from the backend on each visit.

## Subtasks

- Add `close(id: number): Observable<TenderSummary>` to `freight-tenders/frontend/src/app/tender-api.ts` (POST `/api/tenders/${id}/close`, no body).
- In `tender-detail.ts`, add `CLOSE_ERROR_MESSAGE` (German), `closing` and `closeError` signals, and `onClose()`. It guards against a null tender or an in-flight request, uses `catchError(() => of(null))`, and on success merges only `status` into the `tender` signal. It must not replace the signal with the summary response, because that would drop remarks and offers. It then disables `remarkForm` and `offerForm`.
- In `tender-detail.html`, add the `btn-secondary` "Ausschreibung schließen" button (`data-testid="close-tender"`, `type="button"`, `(click)="onClose()"`, `[disabled]="closing()"`), shown only `@if (!isClosed())`. Add the `close-error` paragraph next to it, shown when `closeError()` is set.
- Add minimal layout styles in `tender-detail.scss` if the header or action area needs them.
- Add `close` tests to `tender-api.spec.ts` and close-flow tests to `tender-detail.spec.ts` (see tests).
- Update `freight-tenders/README.md`: describe the close action in the `TenderDetail` row and page paragraph, and remove the 'no UI / API only' statements.
- Run `npm run lint`, `npm run build`, `npm test -- --watch=false` in `freight-tenders/frontend`. Confirm backend tests are untouched and still pass with `mvn -B verify` and `mvn spotless:check`.

## Tests

- tender-api.spec.ts: `close(5)` issues a POST to `/api/tenders/5/close` and emits the returned summary (HttpTestingController, with `httpMock.verify()` in afterEach).
- tender-detail.spec.ts: an open tender shows the `close-tender` button with the text "Ausschreibung schließen", and it is a secondary (non-primary) button.
- tender-detail.spec.ts: clicking the button sends POST `/api/tenders/{id}/close`. After the flush, `status` reads "Geschlossen", `closed-explanation` is present, `remark-submit` and `offer-submit` are disabled, `close-tender` is gone, and the existing remark and offer rows are still rendered (guards against replacing the tender with the summary response).
- tender-detail.spec.ts: while the close request is pending, `close-tender` is disabled, and a second click issues no second request (`expectOne` plus `verify`).
- tender-detail.spec.ts: a failing close request (e.g. 500) shows `close-error` with German text, leaves `status` as "Offen", keeps `close-tender` visible and enabled again, and keeps both add-forms usable.
- tender-detail.spec.ts: a tender that loads as CLOSED never renders `close-tender`.
- Existing tender-overview, tender-detail, tender-create and backend tests continue to pass unchanged.
- Optional: a tender-overview test that a tender with status CLOSED is listed under `closed-tenders`. It already exists, so this is only regression coverage.

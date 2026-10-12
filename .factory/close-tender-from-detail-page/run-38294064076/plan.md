---
schema_version: 1
story_slug: close-tender-from-detail-page
stage: analysis
status: ready-for-review
updated: 2026-10-12T18:55:09Z
---

## Proposal

Frontend-only change, no backend behavior changes. Add `close(id)` to `TenderApiService` (POST `/api/tenders/${id}/close`, returning a `TenderSummary`-shaped response). In `TenderDetail`, add `closing` and `closeError` signals plus an `onClose()` handler that follows the existing remark/offer pattern: guard against double submission, set `closing`, call the API through `.pipe(catchError(() => of(null)))`, and check `=== null` to set a German error message ("Die Ausschreibung konnte nicht geschlossen werden. Bitte versuchen Sie es später erneut."). On success it sets `tender.status` to `CLOSED` locally via `tender.update`, keeping the loaded remarks and offers because the close response carries no collections. It then calls `remarkForm.disable()` and `offerForm.disable()`, so the existing `isClosed()`-driven pill, explanation notice and disabled forms appear with no reload or navigation. In the template, render an outlined `btn-secondary` button "Ausschreibung schließen" (`data-testid="close-tender"`) in the page header or beside the status pill, inside `@if (!isClosed())`. It is disabled while `closing()` is true, and a `form-error` paragraph (`data-testid="close-error"`) sits next to it. Because the existing closed-state logic is already in place, an already-closed tender never shows the action. The overview already loads fresh data on each visit, so the tender appears under "Geschlossene Ausschreibungen" without further change; this should be confirmed in the tests. Update `freight-tenders/README.md`: the detail-page route row, the paragraph that says closing is API-only, and the "Running both together" curl note.

## Subtasks

- Add `close(id: number): Observable<TenderSummary>` to `freight-tenders/frontend/src/app/tender-api.ts`, posting to `/api/tenders/${id}/close`.
- In `tender-detail.ts`, add a `CLOSE_ERROR_MESSAGE` constant and `closing`/`closeError` signals.
- In `tender-detail.ts`, add `onClose()`: return early if the tender is null, already closed or `closing()`; set `closing` and clear `closeError`; call `tenderApi.close` with `catchError(() => of(null))`; on null set the error; on success update the tender status to CLOSED (keeping remarks and offers) and disable both forms.
- In `tender-detail.html`, add the `@if (!isClosed())` block with the outlined `btn-secondary` 'Ausschreibung schließen' button (`data-testid="close-tender"`, `[disabled]="closing()"`, `(click)="onClose()"`, `type="button"`) and the `close-error` message next to it. Add minimal SCSS in `tender-detail.scss` if needed for layout, using existing design tokens.
- Add `tender-api.spec.ts` coverage for `close()`.
- Add `tender-detail.spec.ts` coverage for the close flow (see tests).
- Update `freight-tenders/README.md` so it no longer says closing is API-only: the `/tenders/:id` row, the paragraph around line 65, and the curl note around line 90.
- Run `npm run lint`, `npm run build` and `npm test -- --watch=false` in `freight-tenders/frontend`.

## Tests

- tender-api.spec.ts: `close(7)` issues a POST to `/api/tenders/7/close` and returns the closed tender; paired with `httpMock.verify()` in `afterEach`.
- tender-detail.spec.ts: an open tender shows `close-tender`, with a German label 'Ausschreibung schließen'.
- tender-detail.spec.ts: a tender that is already closed when the page loads shows no `close-tender`.
- tender-detail.spec.ts: clicking the button sends the POST, and a successful response switches `status` to 'Geschlossen', shows `closed-explanation`, disables `remark-submit` and `offer-submit` and their inputs, and removes `close-tender`. No second GET is issued, and the existing remarks and offers rows remain.
- tender-detail.spec.ts: while the request is pending `close-tender` is disabled, and a second click sends no second request.
- tender-detail.spec.ts: a failed close (HTTP 500) shows a German message in `close-error`, the status stays 'Offen', the forms stay enabled and the button is enabled again.
- Existing frontend tests (`npm test -- --watch=false`) and backend tests still pass, and `npm run lint` and `npm run build` succeed.

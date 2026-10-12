---
title: 'Frontend: create & view tender'
type: 'feature'
ticket: 6
created: '2026-10-12'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '8fc4d3337a242415143e970ab2ae1728c7d542f4'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The overview (entry 5) can only list tenders -- there's no way to create one or to inspect/extend an existing one from the UI, and entries 3/4's create, detail, and add-remark/offer endpoints are still unreachable from the app.

**Approach:** Add a create-tender form and a tender-detail page (with add-remark/add-offer forms, disabled once closed) as routed pages, with the overview linking into both -- all labels, buttons, and messages in German, `status` mapped to German for display rather than shown raw.

## Boundaries & Constraints

**Always:** All form labels/buttons/messages (incl. the disabled-state explanation) are German; `status` is mapped to German text for display, never shown as the raw `OPEN`/`CLOSED` value; both new pages go through `TenderApiService`, never `HttpClient` directly.

**Never:** No edit/delete of tenders, remarks, or offers. No validation library -- native HTML/Reactive Forms validation only. No backend changes.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Create tender | Form filled in and submitted | On success, navigates to `/` and the new tender is visible in the overview | On failure, a German error message is shown, no navigation |
| Open tender detail | `GET /tenders/:id` for an open tender | Remarks/offers shown; add-forms enabled; a successful add appends to the list without a reload | No error expected |
| Closed tender detail | Same, for a closed tender | Add-forms disabled | A German message explains why, in place of the forms |
| Unreachable/unknown tender | Backend down, or an id with no match (`404`) | Rejected | German error/not-found message instead of a crash |

</frozen-after-approval>

## Code Map

- `tender-api.ts` -- has `list()`; extend with `create`, `detail`, `addRemark`, `addOffer`, mirroring the backend's `TenderResponse`/`TenderDetailResponse`/`RemarkResponse`/`OfferResponse`/`CreateTenderRequest`/`AddRemarkRequest`/`AddOfferRequest` shapes (entries 3/4).
- `tender-overview.ts`/`.html` -- lists tenders; this ticket adds a link to the create form and makes each item link to its detail page.
- `app.routes.ts` -- currently empty; wire the three pages here.
- `app.ts`/`app.html` -- currently embeds `<app-tender-overview />` directly; switch to `<router-outlet />` now that there's more than one page.
- `provideRouter(routes)` is already registered in `app.config.ts` (entry 1) -- no config change needed there.

## Tasks & Acceptance

**Execution:**
- [x] `tender-api.ts` -- add `create(origin, destination)`, `detail(id)`, `addRemark(id, text)`, `addOffer(id, supplierName, amount)`, plus the `TenderDetail`/`RemarkSummary`/`OfferSummary` types
- [x] Generate `tender-create/` (`ng generate component tender-create`) -- Reactive Form, German labels ("Von"/"Nach"), submit calls `TenderApiService.create`, navigates to `/` on success, German error message on failure, an "Abbrechen" link back to `/`
- [x] Generate `tender-detail/` (`ng generate component tender-detail`) -- reads `id` from the route; fetches detail; maps `status` to German ("Offen"/"Geschlossen") for display; shows remarks/offers with add-forms; add-forms disabled with a German explanation when closed; appends the created remark/offer to the local list on success; German not-found/error message on `404`/failure
- [x] `tender-overview.ts`/`.html` -- add a "Neue Ausschreibung erstellen" link to `/tenders/new`; make each tender item a `routerLink` to `/tenders/:id`
- [x] `app.routes.ts` -- `''` -> `TenderOverview`, `'tenders/new'` -> `TenderCreate`, `'tenders/:id'` -> `TenderDetail`
- [x] `app.html`/`app.ts` -- replace the direct `TenderOverview` embed with `<router-outlet />`
- [x] Specs for every file above, covering all four matrix rows between them

**Acceptance Criteria:**
- Given the create form is filled in and submitted successfully, when the user lands back on `/`, then the new tender is visible in the overview.
- Given an open tender's detail page, when a remark or an offer is submitted, then it appears in its list without a page reload.
- Given a closed tender's detail page, when it loads, then both add-forms are disabled and a German message explains why.

## Implementation Notes

`ng generate component` was used for both `tender-create/` and `tender-detail/` as the plan specified; both generated cleanly with no naming surprises (unlike `tender-api`'s service generation in the previous ticket).

`App`'s router outlet is tested two ways rather than one combined test: a structural check that `App`'s template renders a `<router-outlet>` element, plus a separate test (via `RouterTestingHarness` against the real `app.routes.ts`) that navigating to `/` activates `TenderOverview`. An earlier attempt to drive navigation through `App`'s own fixture directly (`TestBed.createComponent(App)` + `router.navigateByUrl('/')`) didn't reliably activate the route in the test harness, so the two-test split was used instead -- it still covers both halves of the acceptance criterion (the outlet exists; the routes wire up correctly).

`TenderDetail`'s add-remark/add-offer forms are disabled via `FormGroup.disable()` when the loaded tender's status is `CLOSED` (covering both the submit buttons and the inputs themselves), with a single German explanation paragraph shown above both forms rather than one per form -- the plan's matrix calls for "a German message," not one per form.

Verified: `npm run build` -- succeeds. `npm test -- --watch=false` -- 5 test files, 23 tests, all pass (covering all four I/O matrix rows: create success/failure, open-tender add-remark/add-offer without reload, closed-tender disabled forms with explanation, and unreachable/unknown tender showing a German error). `npm run lint` -- clean, no errors.

Not independently verified: the manual browser/backend check (create via UI, close via direct `POST .../close`, reload to confirm disabled state) was not run against a live backend in this session; the automated specs cover the equivalent behavior via mocked HTTP responses instead.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 0, medium: 0, low: 1, false: 0, maybe-false: 0

A full live end-to-end run (real backend + real `ng serve`, driven via browser automation) confirmed all acceptance criteria and matrix rows hold against real Jackson serialization, real routing, and real open/closed enforcement -- not just the mocked specs.

- `tender-detail.ts`'s `offerForm.amount` control is initialized to `0`, so the "Betrag" input visibly shows `0` on page load rather than empty -- confirmed live. Doesn't let an invalid (zero) submission through (`Validators.min(0.01)` still blocks the submit button); purely a pre-fill that could read as an already-entered value. **low**, route: **patch** -- trivial (change the initial value), and it's seen on every open of the add-offer form, not a rare case.

Patch applied: `offerForm.amount` now starts `null` (via a plain `FormBuilder.group` with a per-control builder, since `nonNullable.group` can't hold `null`), so the "Betrag" input starts empty; `onAddOffer` asserts `amount as number` after the existing `offerForm.invalid` guard, which `Validators.required` already makes true whenever `amount` is `null`. Full re-verification after patching: `npm run build` -- succeeds; `npm test -- --watch=false` -- 23/23 pass; `npm run lint` -- clean.

## Design Notes

Reactive Forms for both new forms, not template-driven -- consistent, directly testable validation without adding a library.

A successful add-remark/add-offer appends the endpoint's own response to the local signal list rather than refetching the whole detail -- avoids an extra round trip, same footprint principle as entries 3/4's own design.

`App`'s template becomes a single `<router-outlet />` -- `TenderOverview` is no longer something `App` embeds directly; it's reached via the default route like the other two pages.

## Verification

**Commands:**
- `cd freight-tenders/frontend && npm run build` -- expected: build succeeds
- `npm test -- --watch=false` -- expected: all specs (incl. all four matrix rows) pass
- `npm run lint` -- expected: no lint errors

**Manual checks (if no CLI):**
- With the backend running, open `http://localhost:4200`, create a tender via the form, confirm it appears in the overview, open its detail page, add a remark and an offer, then close it via `POST /api/tenders/{id}/close` directly (no close-UI exists yet) and reload the detail page to confirm the add-forms are disabled.

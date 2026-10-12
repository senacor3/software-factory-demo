---
title: 'Frontend: tender overview'
type: 'feature'
ticket: 5
created: '2026-10-12'
status: done
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '188b0e056848b6f4f781b12c430760fff37a9cc7'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The Angular app has nothing but entry 1's health-check tracer page; there's no view consuming entry 4's tender list endpoint.

**Approach:** Add a `TenderOverview` component, backed by a `TenderApiService`, that fetches `GET /api/tenders` once and splits the results client-side into "open" and "closed" sections under German headings, becoming the app's home view in place of the health tracer.

## Boundaries & Constraints

**Always:** All tender-facing UI text (headings, empty-state, error messages) is German; the component calls `TenderApiService`, never `HttpClient` directly; English `status` values (`OPEN`/`CLOSED`) are used only to group tenders, never rendered as text.

**Never:** No create/detail navigation yet (ticket 1.6). No backend changes. No styling library added.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Mixed tenders | Backend returns both open and closed tenders | Open ones listed under "Offene Ausschreibungen", closed under "Geschlossene Ausschreibungen" | No error expected |
| One section empty | Backend returns tenders of only one status | The empty section shows a German empty-state message instead of an empty list | No error expected |
| Backend unreachable | `GET /api/tenders` fails | A German error message is shown instead of an unhandled failure | `catchError` maps the failure to an error state, same pattern as entry 1 |

</frozen-after-approval>

## Code Map

- `app.ts`/`app.html` -- currently the health-check tracer (entry 1): injects `HttpClient` directly, calls `/api/health`, shows the result under "Systemstatus". This ticket replaces it as the home view with `TenderOverview`; the tracer's job (proving backend connectivity) is already done, and D2's requirements don't call for a persistent status indicator.
- `app.spec.ts` -- exercises `HttpTestingController` directly; simplify since `App` no longer calls `HttpClient` itself (the child `TenderOverview` will, so a shallow render still needs to flush its request).
- `proxy.conf.json` -- already proxies `/api` to the backend; reused as-is.
- Backend's `TenderResponse` (`id`, `origin`, `destination`, `status`) is the shape `GET /api/tenders` returns -- mirror it as a frontend `TenderSummary` interface.

## Tasks & Acceptance

**Execution:**
- [x] Generate `tender-api.ts` via `ng generate service tender-api` under `src/app/` -- `TenderApiService`: `list(): Observable<TenderSummary[]>` calling `GET /api/tenders`; define `TenderSummary` alongside it
- [x] Generate `tender-overview/` via `ng generate component tender-overview` -- fetches the list in `ngOnInit`, splits into `openTenders`/`closedTenders` signals by `status`, with a `loadError` signal set via `catchError`
- [x] `tender-overview.html` -- German headings ("Offene Ausschreibungen"/"Geschlossene Ausschreibungen"), per-section empty-state text, and a top-level error message when `loadError()` -- covers all three matrix rows
- [x] `tender-overview.spec.ts` -- covers all three matrix rows via `HttpTestingController`
- [x] `app.html` -- replace the health-check markup with `<app-tender-overview />`
- [x] `app.ts` -- remove the now-unused `HttpClient` health-check logic
- [x] `app.spec.ts` -- simplify: assert `App` creates and renders `app-tender-overview`, flushing the child's `GET /api/tenders` request so `HttpTestingController.verify()` doesn't fail

**Acceptance Criteria:**
- Given the backend returns a mix of open and closed tenders, when the overview page loads, then they appear under their respective German headings, matching the backend's grouping.
- Given one status has no tenders, when the overview page loads, then that section shows a German empty-state message rather than nothing.
- Given the backend is unreachable, when the overview page loads, then a German error message is shown.

## Implementation Notes

`ng generate service tender-api` on this Angular 22 CLI defaults the class to `TenderApi` (no "Service" suffix); regenerated with `--injectable` to keep the plan's `tender-api.ts` filename, then renamed the class to `TenderApiService` to match the plan exactly.

Verified: `npm run build` -- succeeds. `npm test -- --watch=false` -- 3 test files, 7 tests, all pass. `npm run lint` -- clean.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 0, medium: 2, low: 0, false: 0, maybe-false: 0

- `tender-overview.ts`/`.html` -- no loading state: `openTenders`/`closedTenders` default to `[]` before `GET /api/tenders` resolves, so the template's empty-state branch renders on every single load, telling the user "no tenders exist" when the truth is "not loaded yet." Masked in specs only because `HttpTestingController` flushes synchronously. **medium**, route: **patch** -- real on every load (not a rare edge case), fix is a trivial `loading` signal.
- `freight-tenders/README.md` -- left stale: still documents the home page as the health-check tracer ("Systemstatus"/"nicht verfügbar"/`/api/health`), none of which is true after this ticket replaced it with the tender overview (confirmed via repo-wide grep -- only the README still references it). Not in the plan's Code Map, so the implementer correctly followed the plan as written; the plan omitted it. **medium**, route: **patch** -- trivial text fix, and the epic's own Done-when 4 ("presentable as a demo... clear README") makes stale docs here a named harm, not cosmetic.

Both patches applied: `TenderOverview` gained a `loading` signal (default `true`, cleared once the response/error arrives) checked before `loadError`/the empty-state branches, with a new spec asserting the loading text shows and neither empty-state testid is present pre-flush; `freight-tenders/README.md`'s frontend section now describes the tender overview (fetch, loading/empty/error states) instead of the deleted health-check tracer. Full re-verification after patching: `npm run build` -- succeeds; `npm test -- --watch=false` -- 8/8 pass; `npm run lint` -- clean.

## Design Notes

A single unfiltered `GET /api/tenders` call, split client-side by `status`, rather than two filtered calls -- halves HTTP traffic for the same data and still fully exercises entry 4's list endpoint.

`status` is used only to group tenders into sections, never rendered as text -- showing the backend's English enum value directly would violate the German-UI boundary; the German headings already convey the grouping.

## Verification

**Commands:**
- `cd freight-tenders/frontend && npm run build` -- expected: build succeeds
- `npm test -- --watch=false` -- expected: all specs (incl. all three matrix rows) pass
- `npm run lint` -- expected: no lint errors

**Manual checks (if no CLI):**
- With the backend running and at least one tender created via the API directly (no create UI exists yet -- that's ticket 1.6), open `http://localhost:4200` and confirm the overview shows it under the correct German heading.

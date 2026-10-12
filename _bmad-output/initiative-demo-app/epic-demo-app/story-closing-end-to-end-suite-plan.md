---
title: 'Closing end-to-end suite'
type: 'chore'
ticket: 9
created: '2026-10-12'
status: done
route: 'oneshot'
route_source: 'auto'
review: ''
review_source: ''
lenses_ran: []
review_loop_iteration: 0
baseline_revision: 'e23fe94af8d92648f2cf24a4c26fd06439fec430'
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** light-factory has not yet carried a real, non-trivial freight-tenders story through all its jobs to a merge on `main` with both gates approved by a person, and the README has to be presentable to a semi-technical reader.

**Approach:** Dispatch `stories/close-tender-from-detail-page.md` through `.github/workflows/light-factory.yml`, follow it to merge (the human approves both gates), confirm the result in the running app, and leave `freight-tenders/README.md` short and accurate.

**Decisions (2026-10-12, reviewed with the user):**

- Story to run: `stories/close-tender-from-detail-page.md`. It is frontend-only; "makes a business rule usable in the UI" is accepted as meeting criterion 1.
- The agent dispatches the workflow; the human approves `plan-approval` and `evidence-approval`. The agent never approves a gate.
- Acceptance criteria, as agreed before dispatch and amended by the user after the run (2026-10-12: the README walkthrough and its security note were dropped):
  1. The dispatched run reaches merge on `main`.
  2. At `plan-approval` and `evidence-approval` the run pauses and a person approves.
  3. The `checks` job runs the demo app's build, test, and lint commands and they pass; passing after a checks-fix-loop cycle counts.
  4. With the merged app started, the story's behavior is visible in the German UI -- checked by the agent in a browser, together with the browser check of entry 11's forms and narrow layout that entry 8 re-parked here.
  5. `freight-tenders/README.md`, in English, says what the app is, lists its endpoints and pages, and gives the commands to build, test, lint, and run it. It carries no walkthrough of the run.
  6. A run that halts or fails before merge does not satisfy this story: the agent reports it and the human decides whether to fix and re-dispatch.

</frozen-after-approval>

## Implementation Notes

Oneshot: the code change is the pipeline's own; this entry's direct edits are to `freight-tenders/README.md`.

**Attempt 1 -- run `38294064076`, PR #14 (closed unmerged).** Analysis, `plan-approval` (approved by the human), implementation, checks, and review all succeeded (0 findings, 0 fix cycles), but `Merge` was `skipped`, so `evidence-approval` never opened. Cause: `checks-fix-loop` (added in `472cc33`) is `skipped` when checks pass first try, and `Merge` had no `if:`, so GitHub's default `success()` skipped it on the skipped ancestor. Fixed with the human's go-ahead in `9817eba` (`if: ${{ !cancelled() && needs.review.result == 'success' }}` on `merge`) -- pipeline logic, outside this epic's Boundaries, a deliberate exception.

**Attempt 2 -- run `38295852809`, PR #15, merged as `f0d1ad5`.** Same story, unchanged. Analysis raised no question; both gates approved by the human (`leichtundkross`, per the run's approvals API); checks build/test/lint passed first try (`checks-fix-loop` skipped), `security` recorded as `skipped`; review `resolved`, 0 findings, `fix_cycle: 0`; `Merge` succeeded, which also proves the workflow fix.

**Criteria:** 1 met (merged on `main`). 2 met. 3 met, first try. 4 met, see below. 6: attempt 1 was reported and the human chose fix and re-dispatch.

**Criterion 5 -- README.** A "Walkthrough" section was first added (commit `d9908a0`), then removed at the user's request together with the language paragraph, the backend error paragraph, and the frontend's functional prose. The README now holds the general description, the endpoint table, the route/page table, and the run commands. The criteria were amended to match; the run's record stays in PR #15 and `.factory/close-tender-from-detail-page/run-38295852809/`.

**Criterion 4 -- browser check (Chrome, against the backend on :8080 and `ng serve` on :4200 already running locally, merged `main`), using a test tender "Testhafen -> Pruefstadt" created through the UI:**
- Create form -> lands on the overview with the new tender at the top of the open table; selecting the row's Nach cell opens the detail page.
- Add remark and add offer (submitted with Enter): rows appear without reload, newest first; amounts render as `99,00 €` / `1.234,56 €`, right-aligned; sorting by Betrag gives numeric order with `aria-sort="ascending"`. Inter is loaded.
- Forced failure (one POST rejected in the page): remark error shown in `rgb(179, 38, 30)` below the field and above the submit button, typed text kept, retry succeeded.
- Close: a forced failure shows the German close error and leaves the tender open with forms enabled; the real close switches the pill to "Geschlossen", shows the explanation, disables all five form controls, removes the button, keeps remarks/offers, no navigation. The overview then lists the tender under "Geschlossene Ausschreibungen" and the open table shows its empty-state row.
- Narrow layout, checked in a 390px-wide same-origin iframe (the window itself would not resize): no horizontal overflow on any of the three pages; page, cell, sort-button, and empty-cell padding all 16px.
- Keyboard sort: Space on a focused header sorted it. Enter sent through the automation tool had no effect, so Enter is not confirmed by this check (a native `<button>` activates on Enter; entry 11's implementer reported checking it by hand).
- Not checked: the in-flight disabled state of the buttons (too brief to observe against a local backend; unit-tested).

The test tender (id 2, now closed, with two remarks and two offers) is left in the local in-memory backend; it disappears on restart.

Verified on merged `main`: `mvn -B verify` exit 0; frontend build succeeds, 64/64 tests pass, lint exit 0.

## Plan Change Log

## Review Triage Log

## Verification

**Commands:**
- `gh run view <run-id>` -- expected: conclusion `success`, all jobs through `Merge` green
- `cd freight-tenders/frontend && npm run build && npm test -- --watch=false && npm run lint` on merged `main` -- expected: all pass
- `cd freight-tenders/backend && mvn -B verify` on merged `main` -- expected: BUILD SUCCESS

**Manual checks (if no CLI):**
- Backend and frontend started from merged `main`: close a tender from its detail page; exercise add-remark/add-offer (success and failure), and view the pages at a narrow width.

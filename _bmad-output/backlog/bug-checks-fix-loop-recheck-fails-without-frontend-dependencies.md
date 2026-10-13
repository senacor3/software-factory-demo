---
id: 5
type: bug
title: "The checks fix loop cannot confirm a fix for a check that runs a frontend command and gives up on correct code"
parent: none
covers: []
after: []
assignee: ""
refined: false
hitl: false
risk: medium
severity: P2
estimate: ""
---

# The checks fix loop cannot confirm a fix for a check that runs a frontend command and gives up on correct code

## Description

When `build` passes but `test`, `lint` or `static_analysis` fails, the
`checks-fix-loop` job fixes the code but then fails the re-check for a reason
that has nothing to do with the code: the frontend tools (`ng`, `eslint`) are
not installed in that job. All three checks end in a frontend command, so this
happens whichever of them failed and whichever part of it held the original
finding -- a backend-only finding is enough, because the re-check runs the
check's whole command list. The loop spends both of its fix cycles on this,
stamps `unresolved-after-cap`, and the run ends red with `review` and `merge`
skipped and the PR left open. A fix loop that has repaired the code should
see its re-check pass and let the run continue to review.

Re-running the failed jobs of such a run gets it through, but leaves the
story branch's `checks.md` saying `unresolved-after-cap` although every check
now passes, so the merged evidence contradicts the outcome.

## Reproduction

1. Dispatch a story whose implementation passes `build` and `test` but leaves
   a frontend lint error. Observed on run 38377603346
   (github.com/senacor3/software-factory-demo/actions/runs/38377603346),
   story `tender-overview-shipment-columns`, PR #21.
2. `Checks` fails `lint` and `static_analysis` with a real finding:
   `tender-test-data.ts 31:23 error '_count' is assigned a value but never
   used @typescript-eslint/no-unused-vars` (and the same for `_lowest`).
3. `Checks fix loop` runs. Cycle 1 removes the unused variables (commit
   `448482f` on the story branch).
4. The loop re-runs `lint` and `static_analysis`. Actual: both fail with
   return code 127 --
   `> ng lint` / `sh: 1: ng: not found` and
   `> eslint -c eslint.static-analysis.config.js .` / `sh: 1: eslint: not found`.
   Expected: both pass, because the code is now clean.
5. Cycle 2 has nothing to fix. The job prints
   `{"ok": true, "status": "unresolved-after-cap", "fix_cycle": 2}` and exits 1.
   `Review & fix loop` and `Merge` are skipped; PR #21 stays open.
6. Confirmation that the code was correct: on a local checkout of the story
   branch tip (`80c7e12`), after `npm ci`, `npm run lint` reports "All files
   pass linting." and `npm run static-analysis` reports no findings
   (2026-10-13).
7. Stale state: re-run the failed jobs of that run. The `checks` job runs all
   five checks on the fixed branch and writes fresh evidence for each.
   Actual: `checks.md` keeps `status: unresolved-after-cap` and
   `fix_cycle: 2` from step 5, with the two tooling errors listed as failing
   checks. Expected: the state on the branch matches the checks' latest
   result.

### Second observation: `test`, and a backend-only finding

Run 38387681388
(github.com/senacor3/software-factory-demo/actions/runs/38387681388), story
`award-tender-to-offer`, hit the same dead end through different checks.

1. `Checks` passes `build`, `lint` and `security` and fails two checks with
   real findings: `test` with 13 failing frontend tests (12 in
   `tender-detail.spec.ts`, 1 in `tender-overview.spec.ts`), and
   `static_analysis` with one backend finding and a clean frontend part --
   SpotBugs `EI_EXPOSE_REP2` at `Tender.java:235`, in `Tender.award(Offer)`.
2. `Checks fix loop` cycle 1 corrects the two spec files and adds a SpotBugs
   exclusion for `Tender.award` (commit `f0cb4c8` on the story branch).
3. The loop re-runs `test` and `static_analysis`. Actual: both fail with
   return code 127 --
   `> ng test --watch=false` / `sh: 1: ng: not found` and
   `> eslint -c eslint.static-analysis.config.js .` / `sh: 1: eslint: not found`.
   The backend commands of both checks pass before that. Expected: both
   checks pass.
4. Cycle 2 has nothing to fix; the job stamps `unresolved-after-cap` and
   exits 1. `Review & fix loop` and `Merge` are skipped.
5. Confirmation that the code was correct: on an export of the story branch
   tip (`1fffcc6`), after `npm ci`, `npm test -- --watch=false` reports 147 of
   147 tests passed, `npm run static-analysis` reports no findings, and
   `mvn spotbugs:check` under Java 25 reports 0 bugs (2026-10-13).

## Cause Hypothesis

The frontend's `node_modules` exist only as a side effect of the `build`
check, whose command list contains `npm ci`. The `test`, `lint` and
`static_analysis` checks call `npm test`, `npm run lint` and
`npm run static-analysis` and rely on that earlier install. In the `checks` job this holds, because all five checks run
in order on one runner. The `checks-fix-loop` job starts on a fresh runner and
re-runs only the checks that failed, so when `build` passed the first time,
nothing installs the dependencies before the re-check. A re-check runs the
failed check's whole command list, so the frontend command at its end fails
even when the original finding was in the backend part.

The same job also does not perform the `checks` job's toolchain setup: it
installs Node 22 for the Claude Code CLI where the checks config names Node
26, and it has no Java or Maven-cache setup step. The backend commands passed
in both observed runs regardless, so that difference is not the cause here, but it means
a re-check does not run under the conditions the first check did.

For the stale state: `checks.md` is written only by the fix loop. The
`checks` job writes the per-check evidence files but never touches
`checks.md`, so a later passing attempt of that job cannot correct what an
earlier fix loop stamped.

## Acceptance Criteria

1. **A re-check in the fix loop runs under the same conditions as the first check**
   **Given** a story branch where a check failed in the `checks` job
   **When** the fix loop re-runs that check on code that satisfies it
   **Then** the check passes, whichever of the five checks it is and whichever
   other checks passed the first time
2. **A fixed test, lint or static-analysis failure lets the run continue**
   **Given** a run where `build` passed and any of `test`, `lint` or
   `static_analysis` failed, in its backend part, its frontend part, or both
   **When** the fix loop removes the findings
   **Then** the loop stamps `resolved` and `review` runs
3. **A tooling failure is not counted as a code finding**
   **Given** a re-check that cannot start its tool at all
   **When** the fix loop evaluates the result
   **Then** the run ends in a way that names the missing tool as the cause,
   without engaging the implementation agent to fix code for it
4. **A real, unfixed finding still caps out**
   **Given** a check failure the implementation agent does not resolve
   **When** two fix cycles have run
   **Then** the loop stamps `unresolved-after-cap` and the run fails, as today
5. **A later passing attempt corrects the recorded checks state**
   **Given** a story branch whose `checks.md` records `unresolved-after-cap`
   from an earlier attempt of the run
   **When** the `checks` job runs again and every check passes or is skipped
   **Then** `checks.md` on the branch no longer reports an unresolved failure
   or the earlier failing checks, and it still shows how many fix cycles the
   run used
6. **Tests cover the condition found and fixed**
   **Given** the test suites under `factory/graph/tests/` and
   `factory/scripts/tests/`
   **When** they run
   **Then** a test that fails on the defect and passes on the fix covers a
   re-check of each of `test`, `lint` and `static_analysis` alone after `build`
   passed, one covers the
   tooling-failure case of criterion 3, and one covers the corrected state of
   criterion 5; the behavior of criteria 1 and 2 is also confirmed on one
   live dispatch
7. **Or: no change is needed, with proof**
   **Given** the reproduction
   **When** it is run on the current code
   **Then** the re-check already passes, or the report was mistaken, with the
   evidence recorded in Notes -- this supersedes 1 to 6

## References

- parent — none
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-6 (deterministic checks run as direct pipeline steps, with its toolchain addendum) and AD-10 (the bounded checks fix loop and its cap, and which stage owns `checks.md` -- updating AD-10 for criterion 5 is in scope)
- code — .github/workflows/light-factory.yml, the `checks` and `checks-fix-loop` jobs' setup steps
- code — .github/post-implementation-checks.yml, the `checks:` command lists and `toolchains:`
- code — factory/graph/checks_fix_loop_graph.py, the re-run of only the failing checks
- related — _bmad-output/backlog/bug-checks-job-false-red-on-recovered-fix-loop.md (id 4), which changes the same two jobs' conditions
- evidence — github.com/senacor3/software-factory-demo, run 38377603346 and PR #21; state files on branch `light-factory/tender-overview-shipment-columns/run-38377603346` under `.factory/tender-overview-shipment-columns/run-38377603346/` (`checks.md`, `evidence/checks/lint.json`, `evidence/checks/static_analysis.json`)
- evidence — github.com/senacor3/software-factory-demo, run 38387681388; state files on branch `light-factory/award-tender-to-offer/run-38387681388` under `.factory/award-tender-to-offer/run-38387681388/` (`checks.md`, `evidence/checks/test.json`, `evidence/checks/static_analysis.json`)

## Notes

- Decision: filed as a standalone backlog bug, per the user's request
  (2026-10-13).
- Scope widened from frontend `lint` and `static_analysis` to every check
  that runs a frontend command, after run 38387681388 showed the same dead
  end for `test` and for a `static_analysis` failure whose only finding was
  in the backend (2026-10-13).
- Assumption: `severity: P2` -- the pipeline dead-ends for this class of
  failure, but a workaround exists: re-running the failed jobs of the same run
  makes the `checks` job run all five checks again on the fixed branch.
- Assumption: `risk: medium` -- the change is in workflow setup or
  per-repository check configuration, where a mistake only shows on a live
  run.
- Assumption: criterion 3 is in scope. It is a second defect the same run
  exposed -- return code 127 was treated like a code finding and cost a fix
  cycle -- and could be split into its own ticket.
- Decision: the fix-loop job gets the same setup as the `checks` job --
  toolchain versions from the checks config and the frontend dependencies --
  rather than making each check's command list self-sufficient (user,
  2026-10-13).
- Decision: the stale `checks.md` after a re-run is fixed in this ticket, as
  criterion 5 (user, 2026-10-13).
- Open question: how the two jobs share the setup without the steps drifting
  apart again, since a workflow job cannot simply call another job's steps.
- Open question: AD-10 gives `checks.md` to the fix loop alone. Criterion 5
  needs the `checks` job, or something acting for it, to correct that file;
  which of the two writes it has to be settled against AD-5 and AD-10.
- This ticket and bug 4 touch the same jobs; whichever is built second has to
  be planned against the first one's result.

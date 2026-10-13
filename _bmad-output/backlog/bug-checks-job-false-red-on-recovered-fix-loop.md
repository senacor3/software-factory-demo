---
id: 4
type: bug
title: "A run that recovers through the checks fix loop still shows as failed in GitHub Actions"
parent: none
covers: []
after: []
assignee: ""
refined: true
hitl: false
risk: medium
severity: P3
estimate: ""
---

# A run that recovers through the checks fix loop still shows as failed in GitHub Actions

## Description

When a mechanical check (build/test/lint/security/static_analysis) fails on
its first attempt, the `checks` job is designed to fail outright — that
failure is the signal `checks-fix-loop`'s `if:` watches for. The fix loop then
repairs the issue, `review` and `merge` both succeed, and the story's PR gets
merged normally. But because `checks` itself ended in `failure`, GitHub
Actions shows the whole run red in the Actions UI and run list, even though
the pipeline fully recovered and the story merged. Anyone scanning runs by
their badge sees a false failure and has to open the run to learn it actually
succeeded.

## Reproduction

1. Dispatch a story whose implementation fails one mechanical check on the
   first pass (e.g. lint or security).
2. Watch run 38375222879
   (github.com/senacor3/software-factory-demo/actions/runs/38375222879):
   `Checks` job ends `failure` at its `Fail job if any check failed` step
   ("at least one check failed", exit code 1).
3. `checks-fix-loop` then runs, fixes the issue, and commits the evidence;
   `Review & fix loop` and `Merge` both succeed; the PR is merged.
4. Actual: the run's overall conclusion and badge are red/failed, because
   GitHub Actions aggregates a run's status from its worst job conclusion,
   and `Checks` stayed `failure`. Expected: a run that recovers and merges
   shows green — only a run that exhausts the fix loop's cap and leaves the
   PR genuinely unresolved should show red.

## Cause Hypothesis

`checks-fix-loop`'s trigger is wired to `needs.checks.result == 'failure'`
(`.github/workflows/light-factory.yml`), so the `checks` job must itself end
in `failure` to engage the loop — there is no other channel to carry "a check
failed" between jobs. GitHub Actions has no concept of "failed then
recovered" at the run level; it only aggregates job conclusions, so this
design unavoidably paints the whole run red whenever the loop engages, even
on full recovery.

The fix is to stop using the job's own conclusion as that signal. Have
`checks` always exit 0 and instead report a job output (the same pattern
`analysis` already uses for its `status` output) — e.g.
`any-check-failed: 'true'/'false'` — read from the five steps'
`steps.<id>.outcome` values the same way the current `Fail job if any check
failed` step does, but written to `$GITHUB_OUTPUT` instead of exiting 1.
`checks-fix-loop`'s `if:` then reads
`needs.checks.outputs.any-check-failed == 'true'` instead of
`needs.checks.result == 'failure'`, and `review`'s `if:` simplifies since
`checks` is no longer ever `failure` on a recoverable path. Only
`checks-fix-loop` itself exhausting its 2-cycle cap (AD-11's pattern) should
still end a job in `failure`, which is the one case where a red run is
actually correct.

## Acceptance Criteria

1. **A first-attempt check failure that the fix loop resolves leaves the run green**
   **Given** a dispatched story whose `checks` job finds a failing check on
   the first attempt
   **When** `checks-fix-loop` subsequently resolves it and `review` and
   `merge` both succeed
   **Then** every job in the run, including `checks`, shows conclusion
   `success`, and the run's own overall conclusion/badge is `success`
2. **A capped-out, unresolved check failure still shows as failed**
   **Given** a checks failure that `checks-fix-loop` cannot resolve within
   its retry cap
   **Then** the run's overall conclusion is `failure`, and the evidence
   left behind still names which check failed and how many fix attempts
   were made, same as today
3. **An all-pass-first-try run is unaffected**
   **Given** a dispatched story whose `checks` job passes every check on the
   first attempt
   **When** the run proceeds
   **Then** `checks-fix-loop` is skipped and the run behaves exactly as it
   does today — this changes the failure *signal*, not the pass path
4. **Tests cover the condition found and fixed**
   **Given** the project's test suite for `factory/scripts/run_checks.py`
   and the workflow's job-condition logic
   **When** it runs
   **Then** a test (or an inspectable fixture, since job `if:` conditions
   aren't unit-testable directly) covers that `checks` reports
   `any-check-failed` correctly from a mix of pass/fail/skip outcomes, and
   that the real run behavior from criteria 1–3 is verified live on at
   least one dispatch per the Notes below

## References

- parent — none
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-10 (append-only per-stage state; its 2026-10-11 addendum introduced the `continue-on-error`/"fail job if any check failed" pattern this bug targets, but the addendum text doesn't actually document the job-level failure signal itself — updating AD-10 to describe the output-based signal is in scope here) and AD-11 (the bounded-fix-loop cap pattern this mirrors)
- code — .github/workflows/light-factory.yml, the `checks`, `checks-fix-loop`, and `review` jobs' `if:` conditions and the `Fail job if any check failed` step
- code — factory/scripts/run_checks.py, the `toolchains` subcommand already prints `$GITHUB_OUTPUT`-shaped lines this can mirror
- evidence — github.com/senacor3/software-factory-demo, run 38375222879: `Checks` job failed, `checks-fix-loop` recovered, `Review & fix loop` and `Merge` both succeeded, PR merged — run still shows red

## Notes

- Decision: file as a standalone backlog bug rather than inside
  `epic-pipeline-hardening`/`epic-pipeline-open-issues`, per the user's
  request (2026-10-13).
- Assumption: `hitl: false` and `risk: medium` — this changes a job
  `if:`-condition signal, not the fix loop's actual retry/cap behavior
  (which `story-checks-failure-fix-loop.md` already covers and this must
  not alter), so the blast radius is narrower than that story's `high`
  risk/`hitl: true`. Worth a second look before merging the workflow change
  given it touches the same conditionals that gate `review`/`merge`.
- Decision: AD-10 updated now (2026-10-13), as a documentation-only pass
  ahead of the fix, rather than deferred to implementation — see the
  architecture doc's new 2026-10-13 addendum under AD-10, which names the
  current undocumented continue-on-error/fail-job signal, the gap it
  causes, and this ticket as the tracked fix.

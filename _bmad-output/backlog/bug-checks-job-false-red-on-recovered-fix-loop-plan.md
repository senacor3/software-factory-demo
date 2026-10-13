---
title: 'The checks job reports failed checks through a job output, so a run the fix loop recovers shows green'
type: 'bugfix'
ticket: '4'
created: '2026-10-13'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 1
context: []
baseline_revision: '66aa2bbb4da13d4fe918e51d1bbc3061ecb80994'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The `checks` job has to end in `failure` to start the checks fix loop, and GitHub Actions takes a run's conclusion from its worst job. A run whose fix loop recovers and whose story merges therefore still shows red (run 38375222879).

**Approach:** Carry "a check failed" in a job output, `any-check-failed`, instead of the job's conclusion: `checks` ends `success` whenever its checks ran, the fix loop starts on that output, and `review` proceeds when no check failed or the fix loop succeeded. Only a fix loop that does not resolve the failure, or a job that could not do its work at all, leaves the run red.

## Boundaries & Constraints

**Always:** `review` never runs while a check failure is unresolved. An all-pass run behaves as today, with the fix loop skipped. The fix loop's cycles, cap, exit codes and `checks.md` stamps stay as they are. All five checks still run and commit their evidence whatever an earlier one did. The output is computed by `run_checks.py` from the steps' recorded outcomes, never by an agent.

**Never:** Turn a failure the pipeline did not recover from green — a capped-out or tooling-failure fix loop, a crashed step, or a checkout that setup could not prepare. Change job ids or the `merge`/`close-rejected-pr` conditions. Accept an outcome value the script does not know as "nothing failed".

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| All pass | six outcomes `success` | `any-check-failed=false`; `checks` green; fix loop skipped; `review` runs | No error expected |
| A check failed | one or more check outcomes `failure` | `any-check-failed=true`; `checks` green; fix loop runs | No error expected |
| Fix loop resolves | output `true`, fix loop `success` | `review` runs; every job green | No error expected |
| Fix loop does not resolve | output `true`, fix loop `failure` | `review`, `merge` skipped; run red | as today |
| Setup failed | setup outcome `failure` | `checks` red; fix loop and `review` do not run | job fails, naming setup |
| A step crashed before the checks | check outcomes `skipped`, job already failing | `any-check-failed=false`; `checks` red; fix loop and `review` do not run | job fails |
| Unknown or empty outcome | e.g. `''` from a mistyped step id | no output line; exit 2 naming the value | job fails |

</frozen-after-approval>

## Code Map

- `.github/workflows/light-factory.yml` -- `checks` job (l.176-331): no `outputs:` yet; steps `setup` and the five checks carry `continue-on-error: true`; last step `Fail job if any check failed` (l.317-331) exits 1 on any `failure` outcome. `checks-fix-loop` `if:` l.340, `review` `if:` l.422 with their AD-10 comments. `analysis` job's `outputs:` (l.42-47) is the pattern to mirror. `merge` (l.507) and `close-rejected-pr` (l.549) read `review`/`merge`/`implementation` only -- not touched.
- `factory/scripts/run_checks.py` -- `cmd_toolchains` prints `$GITHUB_OUTPUT`-shaped lines and exits 2 on bad input; `main` dispatches subcommands by `args.cmd`.
- `factory/scripts/tests/test_run_checks.py` -- `test_cmd_toolchains_*` as the pattern for an output-printing subcommand.
- `factory/scripts/tests/test_workflow_checks_setup.py` -- reads the workflow as data; `test_checks_job_fails_when_setup_failed` pins the step this change replaces.
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- AD-10's 2026-10-13 addendum describes the current signal and names this ticket as the planned fix.
- `factory/graph/checks_fix_loop_graph.py` -- exit 1 (cap) and 6 (tooling failure) already fail its job. Before its loop (l.186-201) it decides from the evidence on the branch whether a tooling failure is recorded; that evidence includes what its own earlier attempt committed.

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/run_checks.py` -- add `any_check_failed(outcomes)` (true when any is `failure`; `success`, `skipped`, `cancelled` are not; anything else raises) and an `any-check-failed` subcommand taking the outcomes as arguments, printing `any-check-failed=true|false`, exit 2 on an unknown value -- testable home for the signal
- [x] `.github/workflows/light-factory.yml` -- `checks`: add job output `any-check-failed`; replace `Fail job if any check failed` with `Report check outcomes` (`if: always()`, id `report`, the five check outcomes into `$GITHUB_OUTPUT`) and `Fail job if setup failed` (`if: always() && steps.setup.outcome == 'failure'`). `checks-fix-loop` `if:` -> `!cancelled() && needs.checks.result == 'success' && needs.checks.outputs.any-check-failed == 'true'`. `review` `if:` -> `!cancelled() && needs.checks.result == 'success' && (needs.checks.outputs.any-check-failed == 'false' || needs['checks-fix-loop'].result == 'success')`. Update the comments
- [x] `factory/graph/checks_fix_loop_graph.py` -- verify a tooling failure found in the starting evidence once (setup, then the failing checks; no agent call, no cycle counted) before stopping on it; correct the module docstring's description of what starts the loop -- "Re-run failed jobs" now starts here, from this job's own earlier evidence
- [x] `factory/graph/tests/test_checks_fix_loop_graph.py` -- cover a recorded tooling failure that persists, one that is gone and leaves nothing failing, and one that is gone and leaves a real finding
- [x] `factory/scripts/tests/test_run_checks.py` -- cover the function and subcommand for every outcome mix in the matrix, including the unknown and empty values
- [x] `factory/scripts/tests/test_workflow_checks_setup.py` -- replace the pinned fail-step test; assert the job output, the report step's arguments and position after the checks, the setup-failure step, and the exact `if:` of `checks-fix-loop` and `review`
- [x] `architecture-light-factory.md` -- rewrite AD-10's 2026-10-13 gap addendum to describe the output-based signal as built

**Acceptance Criteria:**
- Given the repo after this change, when the documented pytest and ruff commands run, then both pass
- Given this change merged, when a story whose first `checks` run fails one check is dispatched and the fix loop resolves it, then every job and the run show `success`
- Given this change merged, when a story's check failure survives two fix cycles, then the run shows `failure` and `checks.md` reads `unresolved-after-cap` with `fix_cycle: 2`

## Implementation Notes

## Plan Change Log

- **2026-10-13, review pass 1 (bad_plan, amended in place).** Triggering finding: with `checks` green on a failed check, "Re-run failed jobs" re-runs the fix loop alone, and the loop stopped at once on a tooling failure its own earlier attempt had recorded -- a transient `npm ci` failure became unrecoverable short of a full re-run. The Code Map had called `checks_fix_loop_graph.py` "not changed". Amended: Code Map entry; two tasks added (one verification of a recorded tooling failure, and its tests); the re-run Design Note corrected; the `review` condition changed to an allow-list (`== 'false'`). Known-bad state avoided: a fix that turns recovered runs green and makes failed ones unrecoverable. The code was not reverted and re-derived: the amendment adds a step before the loop and leaves the frozen "cycles, cap, exit codes and `checks.md` stamps stay as they are" intact -- the verification counts no cycle and stamps the same statuses. KEEP: the `any-check-failed` subcommand and its strictness about unknown outcomes; the setup-failure step keeping `checks` red; the workflow tests that pin both `if:` conditions.

## Review Triage Log

**Pass 1 (quick lens), 2026-10-13** -- high 1, medium 1, low 5, false 0, maybe-false 0.

| # | Finding | Verdict | Route | Evidence / action |
|---|---------|---------|-------|-------------------|
| 1 | "Re-run failed jobs" after a `tooling-failure` fix loop fails again without retrying anything | high | bad_plan (amended in place) | Confirmed: the loop read `setup.json`/check evidence its own earlier attempt committed and stopped before cycle 1; `checks` is no longer re-run. Fixed: a recorded tooling failure is verified once (setup, then the failing checks) before it stops the loop; three tests added, two existing ones updated. |
| 2 | `review`'s `!= 'true'` lets any other value through, unlike the script side | medium | patch | Confirmed by reading the expression; no current path yields `success` with an empty output, but the guard rested on one step. Fixed: `== 'false'`; the pinning test and AD-10 text updated. |
| 3 | AD-10's bug 5 addendum contradicts the rewritten one about when `reconcile` acts | low | patch | Confirmed. Reworded: `reconcile` acts on a full re-run. |
| 4 | `Reconcile checks state` workflow comment still says the fix loop runs when the job failed | low | patch | Confirmed. Reworded. |
| 5 | `Run checks fix loop` workflow comment states the removed `review` condition | low | patch | Confirmed. Reworded. |
| 6 | `reconcile_checks_state` docstring carries the same stale claim | low | patch | Confirmed. Reworded. |
| 7 | `checks_fix_loop_graph.py` module docstring describes the replaced wiring | low | patch | Confirmed; it is also the CLI help text. Reworded, and extended for finding 1. |

## Design Notes

- A failed setup keeps `checks` red instead of going through the output: it is not a finding the fix loop could repair, and a red `checks` job is what "Re-run failed jobs" re-runs, so a transient install failure can recover. The fix loop's own handling of a recorded failed setup (bug 5) stays as a second line of defence.
- `checks` being green on a check failure changes "Re-run failed jobs": after a fix loop that did not resolve it re-runs the fix loop only, against the evidence on the branch -- fresh cycles after a cap-out; after a tooling failure, one verification of the recorded failure first, since a record of a registry that was down must not fail every re-run. `run_checks.py reconcile` (bug 5) then only acts on a full re-run.
- `review` matches the output against the literal `false`, not "anything but `true`": an empty output must not open the gate, the same allow-list form `implementation`'s `if:` uses.
- `skipped` is not a failure because a check step is only skipped when an earlier step already failed the job.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass
- `uv run --with ruff ruff check factory/` -- expected: no findings

**Manual checks (if no CLI):**
- After merge: the two live dispatches of the second and third acceptance criteria.

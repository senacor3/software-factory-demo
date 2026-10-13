---
title: 'The checks fix loop re-checks under the same conditions as the checks job, names tooling failures, and a later passing checks attempt corrects checks.md'
type: 'bugfix'
ticket: '5'
created: '2026-10-13'
status: done
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 1
context: []
baseline_revision: '581ebd63096b06006196936f9abaed67d485e76b'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The `checks-fix-loop` job re-runs only the failed checks on a fresh runner that has neither the configured toolchains nor the frontend dependencies (`npm ci` lives in `build`), so a re-check of `test`, `lint` or `static_analysis` fails with return code 127 on correct code, burns both fix cycles and dead-ends the run (runs 38377603346, 38387681388). A later passing `checks` attempt leaves `checks.md` at `unresolved-after-cap`.

**Approach:** Give the fix loop the `checks` job's setup — one shared toolchain setup for both jobs, and workspace-preparation commands named in the checks config and run before every check run. Treat a check whose tool cannot start as a tooling failure that stops the loop and names the cause instead of engaging the agent. Let the `checks` job reset a stale `checks.md` when every check passes.

## Boundaries & Constraints

**Always:** Deterministic steps stay plain subprocess/function calls, never graph nodes or agent tools (AD-6). Commands and versions come from `.github/post-implementation-checks.yml` as read from `origin/main`; nothing project-specific is added to `factory/`. The fix loop still re-runs only the failed checks. A real unfixed finding still caps out at 2 cycles with `unresolved-after-cap` and exit 1. `fix_cycle` is stamped only by pipeline code. A config without `setup:` behaves as today.

**Never:** Change job ids, `needs:`/`if:` wiring or how `checks` signals failure (bug 4's scope). Re-run `build` or the full suite as a way to install dependencies. Count a tooling failure as a code finding. Let the `checks` job write `checks.md` in any case other than resetting a stale file once all five checks pass or are skipped. Reset the fix-cycle count.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Re-check after fix | `build` passed; one of `test`/`lint`/`static_analysis` failed; agent fixed it | setup commands run, then only that check; `resolved`, exit 0 | No error expected |
| Fix changes dependencies | cycle edits `package-lock.json` | setup runs again before each cycle's re-check | No error expected |
| Tool missing on re-check | re-checked command returns 126/127 or cannot be spawned | loop stops, no further agent call; `checks.md` status `tooling-failure` naming check and command; exit 6, stderr names it | job fails |
| Tool missing in first evidence | `checks` job evidence already shows 126/127 | loop stops before cycle 1, `fix_cycle: 0`, same as above | job fails |
| Setup command fails | a `setup:` command exits non-zero | treated as tooling failure naming that command | job fails |
| No evidence for a check | evidence file missing | unchanged: a fix cycle runs against it | as today |
| Unfixed finding | check still fails with a real finding after 2 cycles | `unresolved-after-cap`, exit 1 | as today |
| Stale state, checks re-run green | `checks.md` is `unresolved-after-cap`/`tooling-failure`; all five evidence files `pass`/`skipped` | `checks.md` rewritten: `resolved`, body `_none_`, `fix_cycle` kept | No error expected |
| Checks re-run still red, or no `checks.md` | any evidence `fail`, or file absent | `checks.md` untouched / not created | No error expected |

</frozen-after-approval>

## Code Map

- `.github/workflows/light-factory.yml` -- `checks` job (l.176-322): steps `Read toolchain versions`, `Set up Java`, `Set up Node` (l.214-233), five check steps with `continue-on-error`, `Commit checks evidence`, `Fail job if any check failed`. `checks-fix-loop` job (l.324-389): has `Install Node` 22 + Claude CLI only. `implementation` job's Node 22 step is not touched.
- `.github/post-implementation-checks.yml` -- `toolchains:` and `checks:`; `npm ci` is `build`'s third command. Read from `origin/main` only (see AGENTS.md pitfall).
- `factory/scripts/run_checks.py` -- `_read_config_text`, `_parse_commands` (command-list validation to reuse), `_run_command` (returncode `None` on `OSError`), `run_check`, `load_toolchains`/`cmd_toolchains` (pattern for a new subcommand), `main`.
- `factory/graph/checks_fix_loop_graph.py` -- `run_checks_with_fix_loop` (loop l.150-176), `_rerun_checks`, `_render_checks_body`, `_NO_EVIDENCE_DETAIL` (result has `command: None`), `main` exit codes 0/1/4/5.
- `factory/graph/fix_loop_graph.py` -- the `review` job's fix loop (l.98-119) re-runs `run_build` then `run_test` after each cycle on that job's own fresh runner; it relied on `build` running `npm ci`.
- `factory/scripts/state_io.py` -- `STATUS_BY_STAGE["checks"]` (l.75); stage `checks` governs `checks.md`; `write_state`/`read_state`.
- `factory/graph/tests/test_checks_fix_loop_graph.py`, `factory/scripts/tests/test_run_checks.py` -- `_dispatcher`/`_write_evidence` and `repo`/`_write_config` helpers to reuse; `test_repo_config_holds_the_commands_the_script_used_to_hard_code` pins `build`'s commands.
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- AD-6 and AD-10 addenda; AD-10 does not yet name `checks.md`.

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/run_checks.py` -- add `load_setup_commands` (top-level optional `setup:` list, validated like a check's commands) and `run_setup(story_slug, run_id)` returning the usual result shape (`skipped` when empty) and recording it as `evidence/checks/setup.json`, with `read_setup_result` to read it back; add `is_tooling_failure(result)` (`fail`, `command` not None, returncode 126, 127 or None); add `reconcile_checks_state(story_slug, run_id)`; add `setup` and `reconcile` subcommands -- one home for config-driven deterministic steps
- [x] `factory/scripts/state_io.py` -- add `tooling-failure` to the `checks` statuses
- [x] `factory/graph/checks_fix_loop_graph.py` -- stop before cycle 1 when the recorded setup failed; before each agent call and after each re-check, stop on any tooling failure, keeping real findings listed beside it; call `run_checks.run_setup` before each re-check and treat its failure as a tooling failure; stamp `tooling-failure`; `main` prints the named cause to stderr and exits 6; update the module docstring
- [x] `factory/graph/fix_loop_graph.py` -- call `run_checks.run_setup` before the `build`/`test` recheck; a failing setup raises `CheckRegressionError` naming it -- the review loop's recheck is a check run on a fresh runner too
- [x] `.github/actions/checks-toolchain/action.yml` -- new composite action holding the three toolchain steps, with `java`/`node` outputs -- one definition both jobs use
- [x] `.github/workflows/light-factory.yml` -- `checks`: replace the three steps with the action, add `Setup check workspace` (`run_checks.py setup`, `continue-on-error`, counted in the fail loop) before the five checks and `Reconcile checks state` (`if: always()`) before the commit step. `checks-fix-loop`: use the action after the branch checkout; keep Node 22 only when the action's `node` output is empty
- [x] `.github/post-implementation-checks.yml` -- move `npm ci` from `build` to a new `setup:` list; document the key in the header
- [x] `factory/scripts/tests/test_run_checks.py`, `factory/graph/tests/test_checks_fix_loop_graph.py`, `factory/graph/tests/test_fix_loop_graph.py` -- cover every matrix row; parametrize the re-check row over `test`, `lint`, `static_analysis` asserting setup runs before the check's commands; update the pinned repo-config test
- [x] `factory/scripts/tests/test_workflow_checks_setup.py` -- new: parse the workflow and assert both jobs use `./.github/actions/checks-toolchain` and that `checks` runs setup before the checks and reconcile before the commit
- [x] `architecture-light-factory.md` -- AD-6 addendum (`setup:`, shared toolchain action); AD-10 addendum (`checks.md` belongs to stage `checks`: the fix loop writes it, the `checks` job may only reset it; new status `tooling-failure`)

**Acceptance Criteria:**
- Given the repo after this change, when the two documented `uv run` commands for pytest and ruff run, then both pass
- Given this change merged, when one story whose first `checks` run fails only `lint`, `test` or `static_analysis` is dispatched live, then the fix loop stamps `resolved` and `review` runs

## Implementation Notes

## Plan Change Log

- **2026-10-13, review pass 1 (bad_plan, amended in place).** Triggering findings: (1) moving `npm ci` out of `build` broke the `review` job's fix loop, which re-runs `build`/`test` on a fresh runner and was not in the Code Map; (2) with setup writing no evidence, a setup that failed in the `checks` job was not named, could cost a fix cycle when the checks after it failed with an ordinary exit code, and ended `resolved` when they passed. Amended: Code Map gains `fix_loop_graph.py`; the `run_checks.py` task now records setup as `evidence/checks/setup.json`; the `checks_fix_loop_graph.py` task stops before cycle 1 on a recorded failed setup; a `fix_loop_graph.py` task was added; two Design Notes were added. Known-bad state avoided: a merge that fixes the checks fix loop and breaks the review fix loop in the same way. The code was not reverted and re-derived: both amendments add to what was built and the frozen intent ("run before every check run", "Setup command fails -> treated as tooling failure naming that command") already required them. KEEP: the shared composite action; `setup:` as a config key run from Python inside the loops; return-code-only tooling detection; `reconcile` as the `checks` job's single write case; the `_Workspace` regression tests.

## Review Triage Log

**Pass 1 (quick lens), 2026-10-13** -- high 2, medium 2, low 1, false 0, maybe-false 0.

| # | Finding | Verdict | Route | Evidence / action |
|---|---------|---------|-------|-------------------|
| 1 | `npm ci` moved out of `build` breaks the `review` job's fix loop | high | bad_plan (amended in place) | Confirmed: `fix_loop_graph.py` re-ran `run_build`/`run_test` with no setup and the `review` job installs nothing else. Fixed: `run_setup` before the recheck, failing setup raises `CheckRegressionError`; two tests added. |
| 2 | A setup failure in the `checks` job is not named and can cost a fix cycle | high | bad_plan (amended in place) | Confirmed: setup wrote no evidence, so the loop saw only the checks' results. Fixed: setup recorded as `evidence/checks/setup.json`; the loop stops before cycle 1 when it reads `fail`; parametrized test over 1/127/all-green. |
| 3 | Setup fails, all five checks green: loop stamps `resolved`, `review` runs; `reconcile` has the same blind spot | medium | same root cause as 2 | Confirmed by reading `run_checks_with_fix_loop` and `reconcile_checks_state`. Fixed with 2; `reconcile` now leaves `checks.md` alone while setup reads `fail`; test added. |
| 4 | `tooling-failure` drops real findings from `checks.md` in the mixed case | medium | patch | Confirmed: body was the tooling section only. Fixed: non-tooling failing checks are listed under `## Failing checks` after it; the mixed-case test now asserts the body. |
| 5 | `load_setup_commands` reads a non-mapping config as "no setup" | low | patch | Confirmed: `None` was passed for a non-dict. Fixed: raises `ChecksConfigError`, as `_parse_commands` does; two parametrized cases added. |
| 6 | Runs started before the merge lose `npm ci` when re-run after it | medium | not a code change -- recorded in Design Notes and raised to the human | Confirmed: an old run's workflow and story-branch `run_checks.py` ignore `setup:` but read the merged config. No fix in this diff short of keeping `npm ci` in `build` as well; left as a merge-order instruction. |

Also deferred (pre-existing, `_bmad-output/initiative-light-factory/deferred-work.md`): the `review` job does not use the shared toolchain action.

## Design Notes

- Setup runs from Python inside the loop, not as a workflow step of the fix-loop job, because it must run after the agent's edits; in `checks` it is a workflow step because nothing edits there.
- Setup's result is evidence (`setup.json`) because the fix loop runs in another job: without it a setup that failed in `checks` is visible only through whatever the checks after it reported, which need not look like a tooling failure. `reconcile` does not reset `checks.md` while it reads `fail`.
- Tooling-failure detection is by return code only (126/127/spawn error). A missing-evidence result keeps `command: None`, so it stays a fix-cycle case.
- The composite action is used after `Checkout implementation branch` in both jobs, the position the `checks` job's setup steps have today.
- `.github/post-implementation-checks.yml` takes effect only once merged; until then `run_setup` finds no `setup:` on `origin/main` and `build` still holds `npm ci`, so nothing breaks in between. The other direction does break: a run started before the merge keeps its old workflow and story-branch `run_checks.py`, which ignore `setup:`, while reading the merged config, whose `build` no longer installs -- re-running such a run's jobs after the merge fails every frontend command with 127. Re-run or close those runs before merging, or re-dispatch the story afterwards.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass, including the new tests
- `uv run --with ruff ruff check factory/` -- expected: no findings

**Manual checks (if no CLI):**
- After merge: dispatch one story as in the second acceptance criterion and confirm `checks.md` ends `resolved` and the `Review & fix loop` job runs.

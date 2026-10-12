---
title: 'static_analysis becomes a fifth fixed mechanical check name, generic pipeline mechanism only'
type: 'feature'
ticket: '2'
created: '2026-10-12'
status: 'done'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '6490dffabcd6e2ad01239ce799d66f0b9745eaa1'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** light-factory's mechanical checks only recognize `build`/`test`/`lint`/`security` (fixed by AD-6). There is no category for bug-pattern static analysis, distinct from style-only lint, anywhere in the generic pipeline mechanism.

**Approach:** Add `static_analysis` as a fifth fixed check name, mirroring the existing per-check pattern exactly in `run_checks.py`, the `checks` job, and `post_evidence_summary.py`, plus an AD-6 addendum. Leave it unconfigured (`status: "skipped"`) in this repo for now, the same way `security` is today — real commands for freight-tenders are a separate, deferred plan (Plan B, split from this one at the token-count gate; see the ticket's Notes).

## Boundaries & Constraints

**Always:** Mirror the existing per-check pattern exactly (`CHECK_NAMES` tuple, `run_<name>` wrapper, workflow step shape, fail-loop entry, evidence-file naming) so `static_analysis` behaves identically to the other four. Update `post_evidence_summary.py`'s own *duplicated* `CHECK_NAMES` tuple (it does not import `run_checks.CHECK_NAMES`). Author an AD-6 addendum mirroring the two existing addenda's shape.

**Never:** Configure any real `static_analysis` commands in `.github/post-implementation-checks.yml` (that's Plan B — freight-tenders wiring). Change what `build`/`test`/`lint`/`security` run or how they're evaluated; `security` stays a permanent `skipped` placeholder. Fold `static_analysis` into `fix_loop_graph.py`'s build/test-only regression recheck (`lint`/`security` are already excluded by design, AD-11).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Unconfigured (this repo, for now) | no `static_analysis:` key in the config | `run_checks.py static_analysis` records `status: "skipped"` | never `"pass"` |
| Unknown config key | the config names a key outside the five fixed names | `run_checks.py` raises `ChecksConfigError` naming all five | fails loudly, never silently ignored |
| `checks` job runs it | the 5th step runs with nothing configured | it succeeds (exit 0) and writes `evidence/checks/static_analysis.json` with `status: "skipped"` | the fail-loop does not fail the job for a skip |
| Existing four checks | `build`/`test`/`lint`/`security` as configured today | unchanged pass/skip results | no behavior change |

</frozen-after-approval>

## Code Map

- `factory/scripts/run_checks.py` -- `CHECK_NAMES` tuple (line 53): add `"static_analysis"`; add `run_static_analysis()` mirroring `run_security` (322-359); `_add_check_subparser`/argparse loop (365-393) and the unknown-key validator (167-171) are already generic over `CHECK_NAMES` — no edit needed beyond the tuple; update docstring mentions of "four checks... build | test | lint | security" (lines 8, 29, 140).
- `factory/scripts/post_evidence_summary.py` -- its own **duplicated** `CHECK_NAMES = ("build","test","lint","security")` (line 35, not imported from `run_checks.py`), used at lines 61, 71, 103 — extend it so the PR summary includes the 5th check.
- `factory/graph/checks_fix_loop_graph.py` -- imports `run_checks.CHECK_NAMES` directly (line 150); picks up the 5th name automatically, no edit needed; confirm with its existing tests.
- `.github/workflows/light-factory.yml` -- the `checks` job's 4 steps (237-267) and "Fail job if any check failed" bash loop (289-301); add a 5th step `id: static_analysis` and a 5th `"${{ steps.static_analysis.outcome }}"` line.
- `.github/post-implementation-checks.yml` -- add `static_analysis:` under `checks:` with **no commands** (same empty pattern `security` uses); update the header comment's fixed-names list from four to five.
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- AD-6 section; append a third, dated addendum naming the fifth fixed check, mirroring the two existing addenda.
- `factory/scripts/tests/test_run_checks.py` -- add `(run_checks.run_static_analysis, "static_analysis")` to `test_named_runners_run_their_own_check`'s parametrize list, expecting `"skipped"` (alongside `security`'s existing skipped case).
- `factory/scripts/tests/test_post_evidence_summary.py` -- add a `"static_analysis": "skipped"` entry to every `_write_checks(...)` fixture call (~lines 62, 84, 182, 196, 211), mirroring `security`'s existing entry.

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/run_checks.py` -- extend `CHECK_NAMES`, add `run_static_analysis()`, update docstring -- makes the 5th check a recognized CLI subcommand/config key on the same validation/evidence path as the other four
- [ ] `factory/scripts/post_evidence_summary.py` -- extend its own duplicated `CHECK_NAMES` tuple -- the evidence-approval PR summary must report the 5th check
- [ ] `.github/workflows/light-factory.yml` -- add the 5th `checks`-job step and fail-loop line -- wires the new check into the live pipeline the same way the other four run
- [ ] `.github/post-implementation-checks.yml` -- add `static_analysis:` with no commands; update the header comment -- names the check for this repo without configuring real tooling yet (Plan B's job)
- [ ] `architecture-light-factory.md` -- append the third AD-6 addendum -- keeps the architecture doc the source of truth for the fixed-name list
- [ ] `factory/scripts/tests/test_run_checks.py` -- extend the named-runner parametrize list -- proves the 5th check is skipped-by-default like `security`
- [ ] `factory/scripts/tests/test_post_evidence_summary.py` -- add a `static_analysis` entry to every `_write_checks(...)` fixture call -- keeps these tests passing once `post_evidence_summary.py` expects 5 names

**Acceptance Criteria:**
- Given `.github/post-implementation-checks.yml`, when it names a `static_analysis:` key with no commands, then `run_checks.py static_analysis` records `status: "skipped"`, never `"pass"`
- Given the config names a key outside the five fixed names, when `run_checks.py` reads it, then it fails validation naming all five
- Given a run of the `checks` job, when the 5th step runs with nothing configured, then it succeeds and the fail-loop does not fail the job for it
- Given today's `build`/`test`/`lint`/`security` commands and current repo state, when they run after this change, then each still records the same pass/skip result as before
- Given the full `factory/scripts/tests/` and `factory/graph/tests/` suite, when run after this change, then it passes, including the new/updated assertions above

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 1 finding):**
- `.github/workflows/light-factory.yml:280` — "Commit checks evidence" step's comment still says "4 checks above failed" while every sibling comment in the same `checks` job was updated to "5" for this change. Verdict: **low** (confirmed via grep: line 280 reads "regardless of whether any of the 4 checks above failed"). Route: **patch** — smallest fix is a one-word correction (4 → 5), no new surface, no new state.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass, including the new/updated `static_analysis` assertions
- `uv run --with ruff ruff check factory/` -- expected: clean, unchanged
- `uv run factory/scripts/run_checks.py static_analysis --story-slug <any existing> --run-id <any existing>` -- expected: exits 0, writes `evidence/checks/static_analysis.json` with `status: "skipped"`

**Manual checks (if no CLI):**
- Diff `.github/post-implementation-checks.yml` before/after: the four existing checks' commands are byte-for-byte unchanged, only a new empty `static_analysis:` key is added.

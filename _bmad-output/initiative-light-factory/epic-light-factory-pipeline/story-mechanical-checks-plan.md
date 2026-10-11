---
title: 'Mechanical checks'
type: 'feature'
ticket: '8'
created: '2026-10-02'
status: done
baseline_revision: '1b4ecd54b31a46c96e4090c4d957fb7200c0faa0'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** CAP-5 (mechanical checks) is unbuilt. Nothing in Job 2 runs build/test/lint/security against the implementation agent's output, so a run reaches the (not-yet-built) review/evidence stages with zero automated signal.

**Approach:** Add `factory/scripts/run_checks.py`, a deterministic script (AD-6 — never a graph node or agent tool call) with one function per check (`run_build`, `run_test`, `run_lint`, `run_security`), wired as 4 direct steps in Job 2 right after "Run implementation." `build` (`python -m compileall`, syntax/import sanity — this repo has no packaging step) and `test` (the existing pytest suite) are real checks that can genuinely pass or fail. `lint` and `security` have no tool configured in this repo yet (no `pyproject.toml`, no ruff/bandit config) — user's call, 2026-10-02: ship them as honest placeholders (`status: skipped`, never `pass`) rather than wire real tooling now; real lint/security tooling is deferred (see `deferred-work.md`).

## Boundaries & Constraints

**Always:** evidence is written to `.factory/<story-slug>/<run-id>/evidence/checks/<name>.json` *before* any failure/exit code — a failing check always leaves a record; `lint`/`security` record `status: "skipped"` with a reason, never `"pass"`; a `build`/`test` failure makes its own step exit non-zero (AD-6 — job stops, zero further steps run); all four checks run as plain subprocess calls from one deterministic script, never agent tool calls or graph nodes.

**Never:** no agent invocation here; no write to `plan.md`/`decisions.md`/`review.md` (AD-10 — only `evidence/checks/`); no fix-loop/selective re-run (ticket 10's scope); no real lint/security tool wired this entry (explicit v1 scope cut, user's call 2026-10-02).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Build check passes | `python -m compileall factory -q` exits 0 | `evidence/checks/build.json` status `pass`; step exits 0 | n/a |
| Build check fails | A syntax/import error under `factory/` | `evidence/checks/build.json` status `fail`, captures the error; script exits 1, step fails, job stops | Workflow step itself fails (AD-6) |
| Test check passes | pytest suite exits 0 | `evidence/checks/test.json` status `pass`; step exits 0 | n/a |
| Test check fails | pytest suite exits non-zero | `evidence/checks/test.json` status `fail`, captures output; script exits 1, step fails, job stops | Workflow step itself fails |
| Lint check (placeholder) | Always — no tool configured | `evidence/checks/lint.json` status `skipped`, reason given; step exits 0 always | n/a — never fails, never claims `pass` |
| Security check (placeholder) | Always — no tool configured | `evidence/checks/security.json` status `skipped`, reason given; step exits 0 always | n/a — never fails, never claims `pass` |

</frozen-after-approval>

## Code Map

- `factory/scripts/run_checks.py` -- new. `run_build`/`run_test(story_slug, run_id, *, state_base=state_io.FACTORY_DIR, cwd=None) -> dict` shell out to a real command (`[sys.executable, "-m", "compileall", "factory", "-q"]`; `["uv", "run", "--with", "pytest", "pytest", "factory/graph/tests/", "factory/scripts/tests/"]`), status pass/fail from the exit code. `run_lint`/`run_security` (same signature) run no command — always `{"status": "skipped", "command": None, "detail": "no lint/security tool wired for v1 -- see deferred-work.md"}`. All four write `evidence/checks/<name>.json` via `state_io.state_dir`/`state_io.write_atomic` (reused directly — already generic/shared, unlike the duplicated-`_run`-helper convention other scripts use for `git`/`gh`). CLI: one subcommand per check name, `--story-slug`/`--run-id`; exits 1 only on `fail`, 0 for `pass` or `skipped`.
- `.github/workflows/light-factory.yml` -- edit Job 2: add 4 steps after "Run implementation" — "Build check", "Test check", "Lint check (placeholder)", "Security check (placeholder)" — each `uv run factory/scripts/run_checks.py <name> --story-slug "${{ needs.analysis.outputs.story-slug }}" --run-id "${{ needs.analysis.outputs.run-id }}"`.
- `factory/scripts/tests/test_run_checks.py` -- new, covering the I/O Matrix, `subprocess.run` mocked.
- `_bmad-output/initiative-light-factory/deferred-work.md` -- append one entry: real lint (ruff)/security (bandit) tooling deferred for v1 (user's call, 2026-10-02) — written now, not at review time, since the cut is already decided.

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/run_checks.py` -- add `run_build`, `run_test`, `run_lint`, `run_security`, CLI
- [ ] `.github/workflows/light-factory.yml` -- wire the 4 check steps into Job 2
- [ ] `factory/scripts/tests/test_run_checks.py` -- new tests per the I/O Matrix
- [ ] `_bmad-output/initiative-light-factory/deferred-work.md` -- append the lint/security deferral entry
- [ ] Run `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- all pass

**Acceptance Criteria:**
- Given a build or test check that fails, when its workflow step runs, then `evidence/checks/<name>.json` records `status: fail` with captured detail and the step itself exits non-zero, with zero agent turns spent.
- Given a build or test check that passes, when its workflow step runs, then `evidence/checks/<name>.json` records `status: pass` and the step exits 0.
- Given the lint or security check, when its workflow step runs, then `evidence/checks/<name>.json` records `status: skipped` (never `pass`) and the step always exits 0.

## Implementation Notes

## Plan Change Log

## Review Triage Log

- **Quick lens, 2026-10-02: no findings.** Verified against all three acceptance criteria, the I/O Matrix, Boundaries & Constraints, and the Code Map; also ran the real test suite (109 passed) and manually exercised `run_checks.py lint` unmocked (correctly skipped, no subprocess). Confirmed evidence is always written before the exit-code decision, build/test failures produce `status: "fail"` with captured output and a non-zero exit (failing the step per AD-6), lint/security never run a command and never report `"pass"`, and the `deferred-work.md` entry was appended correctly. No loopback triggered.

## Design Notes

**Why `status: "skipped"` for lint/security, not `"pass"`:** CAP-5's success text says "pass/fail per check is recorded" — but recording `pass` for a check that ran no command would misinform the human at `evidence-approval` into thinking lint/security were clean. `skipped` is the honest third state; the deferred-work.md entry makes the gap visible rather than silently hiding it behind a green check.

**Why `compileall` for "build":** this repo has no packaging/build step (no `setup.py`/wheel). `python -m compileall factory -q` is the closest real equivalent — every script at least parses and imports cleanly — without inventing a build artifact that has no referent here.

**Why `state_io.write_atomic`/`state_io.state_dir` reused directly, not duplicated:** unlike the `_run` subprocess-wrapping helper (deliberately duplicated per-module elsewhere in this codebase, since each module owns its own exception type), `write_atomic`/`state_dir` are already stateless, generic, and explicitly meant to be shared — `state_io.py`'s own docstring calls out `evidence/checks/` as a directory other entries write into using this module's primitives.

**Not re-litigated here:** the spec's own open question ("does CAP-6 review proceed when a CAP-5 check fails outright?") predates this ticket and belongs to ticket 9/10 once the review/fix-loop stages exist — for now, a build/test failure stops the job outright (no review step exists yet to worry about skipping).

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass

**Manual checks (if no CLI):**
- Inspect the 4 new workflow steps directly for command/ordering correctness — no automated check for the exact YAML shape.

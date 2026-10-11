---
title: 'Bounded fix loop'
type: 'feature'
ticket: '10'
created: '2026-10-02'
status: done
baseline_revision: 'bc0ea4f0c4a1c65d3e037519561263c68bdee77b'
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

**Problem:** CAP-7 (bounded fix loop) is unbuilt. When ticket 9's review produces findings, nothing routes them back to the implementation agent — Job 2 just ends with `review.md` status `findings-open` and no attempt to resolve it.

**Approach:** Add `factory/graph/fix_loop_graph.py`, orchestrating: review (ticket 9, unchanged) → while findings remain and the cycle count is under 2 → re-engage the *same* implementation agent (CAP-7's own wording: "route back to the implementation agent") with the review findings as added context, re-run only `build`/`test` (the checks capable of being affected — `lint`/`security` are permanent no-op placeholders, ticket 8), then review again. A hard cap of 2 fix cycles (AD-11): if still unresolved after the second cycle's review, stop — no third fix cycle — and stamp `review.md`'s status `unresolved-after-cap` instead. The fix-cycle counter lives in `review.md`'s frontmatter, written only by this loop's own code, never by either agent's output (AD-11).

## Boundaries & Constraints

**Always:** the fix-cycle counter is incremented and stamped only by this module's own code (AD-11) — never derived from or trusted to agent output; a fix cycle reuses the existing `light-factory-implementation` skill via an added optional `review_path` argument, not a new skill; each cycle re-runs only `build`+`test` (the two checks with real pass/fail signal — `lint`/`security` are inert placeholders, ticket 8's Design Notes); exactly 2 fix cycles maximum ever run, regardless of how many consecutive reviews find issues.

**Never:** no third fix cycle, ever — the loop stops at the cap and stamps `unresolved-after-cap` directly, it does not re-invoke review a third time just to relabel; no change to `review_graph.py`'s own write logic (ticket 9, untouched — this entry re-reads and re-stamps `review.md` directly instead); a `build`/`test` regression introduced by a fix cycle is not tolerated as "just another finding" — it immediately fails the step (same hard-stop policy ticket 8 already established for AD-6, now extended into the loop), not a soft signal the loop keeps spending cycles on.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Initial review is clean | review #1 returns no findings | No fix cycle runs; `review.md` status `resolved`, `fix_cycle: 0` | n/a |
| One fix cycle resolves it | review #1 has findings; review #2 (after 1 fix cycle) is clean | 1 fix cycle runs (fix, recheck, re-review); `review.md` status `resolved`, `fix_cycle: 1` | n/a |
| Two fix cycles, still unresolved | review #1, #2, #3 all have findings | Exactly 2 fix cycles run; no 3rd; `review.md` status `unresolved-after-cap`, `fix_cycle: 2`, carrying review #3's findings | n/a — legitimate capped outcome, not a failure |
| A fix cycle regresses `build`/`test` | A re-check after a fix returns `status: "fail"` | Loop stops immediately, no further review invocation | Raises `CheckRegressionError`; step exits non-zero |
| Review tooling fails mid-loop | `claude` CLI invocation fails (any review call) | Loop stops immediately | `review_graph.ReviewInvocationError` propagates; step exits non-zero |
| Fix-cycle implementation tooling fails | `claude` CLI invocation fails (the fix call) | Loop stops immediately, no recheck/re-review attempted | `implementation_graph.ImplementationInvocationError` propagates; step exits non-zero |

</frozen-after-approval>

## Code Map

- `factory/scripts/state_io.py` -- edit `write_state`: add optional `extra: "dict | None" = None` kwarg, merged into `meta` after the fixed AD-10 fields (`schema_version`/`story_slug`/`stage`/`status`/`updated`) when given. Backward compatible — every existing caller omits it, behavior unchanged.
- `.claude/skills/light-factory-implementation/SKILL.md` -- edit: add a short "Fix cycle (optional third argument)" section — when invoked with a third `<review-path>` argument, read `review.md`'s findings and address them specifically, in addition to (not instead of) `plan.md`'s subtasks already done.
- `factory/graph/implementation_graph.py` -- edit `_build_command`/`invoke_skill`/`run_implementation`: add an optional `review_path: "str | None" = None` parameter, appended to the skill's invocation prompt (`/light-factory-implementation {plan} {decisions} {review}`) only when given. Backward compatible — ticket 7's existing calls/tests omit it, behavior unchanged.
- `factory/graph/fix_loop_graph.py` -- new. `CheckRegressionError(RuntimeError)`. `run_review_with_fix_loop(story_slug, run_id, *, claude_bin="claude", state_base=state_io.FACTORY_DIR, cwd=None) -> dict`: calls `review_graph.run_review` (unchanged); while `status == "findings-open"` and `cycle < 2`: increment cycle, call `implementation_graph.run_implementation(..., review_path=<review.md path>)`, then `run_checks.run_build`/`run_checks.run_test` (raise `CheckRegressionError` on either `"fail"`), then `review_graph.run_review` again. After the loop, re-read `review.md`'s already-written body via `state_io.read_state` and re-write it once via `state_io.write_state(..., status=("unresolved-after-cap" if still findings-open else the resolved status), extra={"fix_cycle": cycle})` — the only place the counter is stamped, and the only place `unresolved-after-cap` is ever written. `build_graph()`/`main()` CLI pair (mirrors the existing thin-wrapper pattern; exit codes 3/4/5/6 for `ReviewInvocationError`/`ImplementationInvocationError`/`CheckoutError`&`CommitPushError`/`CheckRegressionError`).
- `.github/workflows/light-factory.yml` -- edit Job 2: retarget the "Run review" step from `review_graph.py` to `fix_loop_graph.py` (rename "Run review (bounded fix loop)"), same `CLAUDE_CODE_OAUTH_TOKEN` env/arg pattern.
- `factory/graph/tests/test_fix_loop_graph.py` -- new, covering the I/O Matrix, `subprocess.run` mocked (same pattern as the existing graph test files).
- `factory/scripts/tests/test_state_io.py`, `factory/graph/tests/test_implementation_graph.py` -- extend with a couple of tests for the new optional `extra`/`review_path` parameters.

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/state_io.py` -- add `extra` kwarg to `write_state`
- [ ] `.claude/skills/light-factory-implementation/SKILL.md` -- add the fix-cycle section
- [ ] `factory/graph/implementation_graph.py` -- add `review_path` param
- [ ] `factory/graph/fix_loop_graph.py` -- add `run_review_with_fix_loop`, `CheckRegressionError`, CLI
- [ ] `.github/workflows/light-factory.yml` -- retarget the review step to the fix loop
- [ ] `factory/graph/tests/test_fix_loop_graph.py` -- new tests per the I/O Matrix
- [ ] `factory/scripts/tests/test_state_io.py`, `factory/graph/tests/test_implementation_graph.py` -- extend for the new params
- [ ] Run `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- all pass

**Acceptance Criteria:**
- Given two consecutive unresolved reviews, when the loop runs, then exactly 2 fix cycles run (never 3), and `review.md` ends with status `unresolved-after-cap` and `fix_cycle: 2`.
- Given a fix cycle resolves the findings, when the loop runs, then it stops immediately (no further cycles attempted) with `review.md` status `resolved` and the actual cycle count stamped.
- Given a fix cycle's recheck regresses `build` or `test`, when the loop runs, then it raises `CheckRegressionError` immediately rather than continuing to spend cycles.

## Implementation Notes

## Plan Change Log

## Review Triage Log

- **Quick lens, 2026-10-02: no findings against this diff.** Verified against all three acceptance criteria, all 6 I/O Matrix rows, and the Boundaries & Constraints; cross-checked against the actual current source (not just the diff's own docstrings); ran the real test suite (143 passed). Confirmed the loop guard has no off-by-one, the `fix_cycle` counter is stamped exactly once post-loop (truthy-dict check correctly handles `0`), `CheckRegressionError` pre-empts any further review/re-stamp, both backward-compatible signature extensions (`extra`, `review_path`) are verified unchanged for existing callers, and `review_graph.py` is confirmed untouched. One pre-existing doc-drift observation noted (architecture doc's Structural Seed file tree and Capability→Architecture Map still attribute CAP-6/CAP-7 to `implementation_graph.py` rather than the now-separate `review_graph.py`/`fix_loop_graph.py`) — not caused by this ticket (predates it, from ticket 9 onward), routed to `deferred-work.md` rather than fixed here. No loopback triggered.

## Design Notes

**Why re-stamp `review.md` directly instead of extending `review_graph.run_review` with an `extra` param:** the simpler design — `fix_loop_graph` reads back what `run_review` already wrote and re-writes once at the very end — touches zero lines of ticket 9's already-built, already-reviewed code, and needs exactly one stamping write instead of one per cycle. `review_graph.py`'s own tests and behavior are entirely unaffected by this ticket.

**Why `build_graph()` stays a thin single-node wrapper, not a real LangGraph conditional-edge state machine:** every prior entry's `build_graph()` is already this shape — a thin wrapper around an independently-tested plain function, never actually invoked by any `main()` or workflow step (each script is called directly via its CLI). Building a true conditional-edge graph here would be the first ticket to break that precedent for a code path nothing currently exercises; the plain `run_review_with_fix_loop` function is what actually runs and is what's tested.

**Accepted simplification, not solved here:** evidence files (`evidence/checks/*.json`, `evidence/review/findings.json`) are overwritten each cycle — only the last cycle's result survives on disk, not a full per-cycle history. `review.md`'s body likewise reflects only the final review's findings. This matches every other stage's "current state, not history" posture (AD-10) and keeps this already-large ticket from also inventing per-cycle evidence versioning.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass

**Manual checks (if no CLI):**
- Inspect the retargeted "Run review (bounded fix loop)" workflow step for correctness — no automated YAML-shape check.

---
title: 'A failed mechanical check retries through a bounded agent fix loop, not a stuck PR'
type: 'feature'
ticket: '1'
created: '2026-10-12'
status: 'built'
baseline_revision: '747e31ed863013905fabe5788458999e4f877346'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** When the `checks` job (build/test/lint/security) fails, the run stops dead — `review` never starts (it needs `checks` to succeed) and `close-rejected-pr` doesn't fire either, leaving the PR stuck with no automated recovery and a human has to notice and intervene by hand.

**Approach:** Add a new `checks-fix-loop` job that runs only when `checks` fails: it re-engages the implementation agent with the failing check's output, re-runs just that check, and repeats up to the same cap-of-2 bound AD-11's review fix loop already uses (new AD-10 `checks` stage/state file, mirroring `review.md`'s `fix_cycle` pattern). `checks` keeps its check semantics and non-agentic nature (only its step wiring changes so evidence commits durably on failure); `review`'s internal steps/logic are unchanged — only its `needs`/`if` is widened to also accept a resolved `checks-fix-loop`.

## Boundaries & Constraints

**Always:**
- Reuse AD-11's existing cap value of 2 (`MAX_FIX_CYCLES`) — one counter for the whole checks-fix-loop job, not per individual check.
- A fix cycle re-runs only the check(s) that actually failed, never the full suite (mirrors AD-11).
- Commit evidence/state durably on every attempt, including the final failing one. Today's `checks` job skips its evidence-commit step when any check fails (GHA's default fail-fast behavior aborts before that step runs) — the 4 check steps need `continue-on-error: true` plus `if: always()` on the evidence-commit step, with a final step that explicitly fails the job if any check failed, preserving today's "any check failure fails the job" outcome while making evidence durable regardless.
- Check pass/fail/skip semantics (AD-6) and `review` job's internal steps/logic are otherwise completely unchanged — only `checks`' step wiring (above) and `review`'s `needs`/`if` change.

**Never:**
- Never change what counts as pass/fail/skip for build/test/lint/security, or how their commands are configured (AD-6).
- Never let `review`/`merge` run while checks have not actually passed.
- Never loop past the cap, or loop silently — cap-out must fail the job the same way an ordinary `checks` failure does today (PR stays open, no auto-close, no silent merge).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|---|---|---|---|
| All checks pass first try | `checks` succeeds | `checks-fix-loop` is skipped (`if: needs.checks.result == 'failure'`); `review` runs exactly as today | No error |
| One check fails, fixed in cycle 1 | e.g. `lint` fails | `checks-fix-loop` re-engages implementation with lint's output, reruns `lint`, passes; job succeeds; `review` runs as if `checks` had passed originally | No error |
| Same check still failing after 2 cycles | cap reached | job stamps `checks.md` `unresolved-after-cap` with the failing check name + `fix_cycle: 2`, then fails; `review` is skipped; PR stays open | Job fails; no further retry |
| Multiple checks fail together | e.g. `build` and `lint` both fail | both failures passed as context in the same cycle; counts as one cycle, not two | Same cap applies jointly |
| `checks` job itself errors (not a check `fail`, e.g. checkout/toolchain crash) | `checks.result == 'failure'` for a non-check reason | `checks-fix-loop` still triggers (GHA can't distinguish); implementation is re-engaged with whatever evidence exists — acceptable, not a regression vs today | Handled like any other fix-cycle attempt |

</frozen-after-approval>

## Code Map

- `factory/graph/fix_loop_graph.py` — existing bounded review fix loop (AD-11), the pattern to mirror exactly: `MAX_FIX_CYCLES=2` (L55, module-local — duplicate the constant in the new module rather than importing, since cross-importing would couple two independently-owned stages), `run_review_with_fix_loop` (L67-137)'s shape: loop → re-engage implementation → narrow recheck → re-stamp state once at the end via `extra={"fix_cycle": cycle}`. Do not modify this file — review stays untouched (AC4).
- `factory/scripts/run_checks.py` — `run_build`/`run_test`/`run_lint`/`run_security` (L322-364) and generic `run_check` (L286): call these directly for the narrow recheck, same as `fix_loop_graph.py` already does for build/test. Do not change check semantics.
- `factory/scripts/state_io.py` — `STAGES`/`STATUS_BY_STAGE` (L65-73): add `"checks"` with its own enum (e.g. `{"checking", "findings-open", "fix-in-progress", "resolved", "unresolved-after-cap"}`). `write_state`'s `extra` kwarg (L228) already supports the `fix_cycle` field generically — no change needed there.
- `factory/graph/implementation_graph.py` — `run_implementation`/`invoke_skill` (L85-157): the existing generic "re-engage with a findings file as 3rd CLI arg" mechanism (`review_path` param). Reuse as-is, passing the new checks-failure state file's path through it.
- `.claude/skills/light-factory-implementation/SKILL.md` — "Fix cycle (optional third argument)" section (L22-24) is worded review-specific; generalize it to also describe a checks-triggered re-engagement.
- `.github/workflows/light-factory.yml` — `checks` job's 4 check steps (L231-253) need `continue-on-error: true` so they all run regardless of individual failure; "Commit checks evidence" (L259-264) needs `if: always()`; a new final step reads the evidence/results and explicitly fails the job if any check failed (preserves today's job-level outcome). `review` job (L266-339) internals unchanged; only `needs`/`if` change. New `checks-fix-loop` job: `needs: [analysis, implementation, checks]`, `if: ${{ !cancelled() && needs.checks.result == 'failure' }}`, with the same agent-invocation setup (`CLAUDE_CODE_OAUTH_TOKEN`, Node, `claude` CLI install) as `review`'s job (L290-296). `review`'s `needs` becomes `[analysis, implementation, checks, checks-fix-loop]` with `if: ${{ !cancelled() && (needs.checks.result == 'success' || needs.checks-fix-loop.result == 'success') }}`.
- `factory/scripts/close_rejected_pr.py` — confirmed not applicable: it only disambiguates a human's environment-gate reject from an ordinary failure; a capped-out checks retry is a deterministic exhaustion, not a gate reject, and the PR must stay open (not closed) — no change here.
- `factory/graph/tests/test_fix_loop_graph.py` — mirror its fixtures/test naming (`_fake_proc`, `_dispatcher`, cap/regression test names) for the new module's tests.

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/state_io.py` -- add `"checks"` to `STAGES` and a status enum to `STATUS_BY_STAGE` -- new AD-10 stage needed before anything can stamp a `checks.md` state file
- [ ] `factory/graph/checks_fix_loop_graph.py` (new) -- bounded loop mirroring `fix_loop_graph.py`: run the failing check(s), re-engage implementation via `implementation_graph.run_implementation(..., review_path=checks_path)`, recheck, loop to cap 2, final `state_io.write_state` with `extra={"fix_cycle": cycle}` and which check(s) failed -- the core new behavior (AC1/AC2/AC5)
- [ ] `.claude/skills/light-factory-implementation/SKILL.md` -- generalize the "Fix cycle" section's wording to cover a checks-triggered re-engagement, not only review -- the agent needs to understand which kind of findings file it received
- [ ] `.github/workflows/light-factory.yml` -- give `checks`' 4 check steps `continue-on-error: true`, make its evidence-commit step `if: always()`, add a final step that fails the job if any check failed; add the new `checks-fix-loop` job (agent setup + invoke the new graph's CLI); widen `review`'s `needs`/`if` as in the Code Map -- makes evidence durable on failure and wires the new stage in without touching check semantics or `review`'s internals
- [ ] `factory/graph/tests/test_checks_fix_loop_graph.py` (new) -- unit tests for: cap reached and still failing, fixed within cap, multiple simultaneous check failures counted as one cycle, tooling-failure propagation -- covers the I/O & Edge-Case Matrix

**Acceptance Criteria:**
- Given a dispatched story whose `checks` job fails, when that failure occurs, then `checks-fix-loop` re-engages implementation with the failing check's output and reruns it before the run gives up (AC1)
- Given a checks failure still present after a fix attempt, when the cap of 2 is reached, then the run stops retrying and reaches the same kind of terminal, human-actionable state the review fix loop already reaches (job fails, PR open, state names the failing check + attempt count) (AC2/AC5)
- Given a checks failure the re-engaged implementation actually resolves, when the check is rerun and passes, then `review` proceeds exactly as if `checks` had passed on the first attempt (AC3)
- Given a run whose `checks` job passes on the first attempt, when review later raises a finding, then the existing bounded review fix loop (AD-11) behaves exactly as today (AC4)

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick, review_loop_iteration 0) — verdicts: 1 medium, 1 low, 0 false, 0 maybe-false**

- `factory/graph/implementation_graph.py:50-58` (`DENY_SETTINGS`) — **medium**, route: patch. Verified: `checks_fix_loop_graph.run_checks_with_fix_loop` re-engages implementation via `run_implementation(..., review_path=checks_path)`, which shares the same global `DENY_SETTINGS` (only `plan.md`/`decisions.md`/`review.md`) — `checks.md` is a new AD-10 stage-owned file but isn't in the deny list, so the agent has live `Edit` access to it during a checks-fix-loop cycle, contradicting both AD-5's two-layer model and this module's own docstring claim that `checks.md`'s counter is "never derived from or trusted to the implementation agent's output." A mid-loop commit could carry a tampered `checks.md` into git history even though the loop's final `write_state` still overwrites it with the authoritative status before the job's commit step. Grouped with the SKILL.md finding below (same root cause: the new stage-owned file was never added to either AD-5 enforcement layer).
- `.claude/skills/light-factory-implementation/SKILL.md:3,29-31` ("Never touch these files" + frontmatter `description`) — **medium**, route: patch (same group/root cause as above). Verified: both the frontmatter `description` and the "Never touch these files" list still name only `plan.md`/`decisions.md`/`review.md`, omitting `checks.md`, even though the same file's "Fix cycle" section (added in this diff) now hands the agent `checks.md` as a findings path.
- `factory/scripts/state_io.py:17-18` (module docstring) — **low**, route: patch. Verified: the docstring says only `analysis` and `review` have enforced status enums, but `STATUS_BY_STAGE` was extended in this diff to also enforce a `checks` enum — stale, but no behavioral effect; fix is a direct text correction, not excluded by the low-rejection rule.

## Design Notes

A new dedicated `checks-fix-loop` job (rather than folding checks into `review`, or retrying inside `checks` itself) was chosen so: `checks` keeps its documented "runs no agent" invariant and stays cheap on the common all-pass path; `review`'s own job and fix loop stay completely untouched (clean AC4 isolation); and the new retry logic only pays agent-setup cost when a check actually failed. This mirrors AD-11's existing pattern (bounded cap, narrow recheck, single end-of-loop state stamp) applied one stage earlier in the pipeline, as its own independent AD-10 stage rather than overloading `review`'s.

## Verification

**Commands:**
- `cd factory/graph && uv run pytest tests/test_checks_fix_loop_graph.py` -- expected: all new unit tests pass, covering cap-reached, fixed-within-cap, and multi-check-failure scenarios
- `cd factory/graph && uv run pytest tests/test_fix_loop_graph.py` -- expected: unchanged, still passes (AC4 regression guard)
- `actionlint .github/workflows/light-factory.yml` (or equivalent workflow lint already used in this repo) -- expected: no errors in the new/changed job definitions

**Manual checks (if no CLI):**
- Inspect a dry-run of the widened `review` job's `if:` expression against GitHub Actions' expression syntax (e.g. via `act` or a scratch workflow) to confirm it evaluates correctly for all three `checks`/`checks-fix-loop` result combinations.

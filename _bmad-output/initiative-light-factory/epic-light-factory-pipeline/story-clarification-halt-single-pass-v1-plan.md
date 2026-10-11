---
title: 'Clarification halt (single-pass, v1)'
type: 'feature'
ticket: '4'
created: '2026-10-02'
status: done
baseline_revision: 'a578a558a9f9cc4c9a542e7c58bd4d0d21a206ea'
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

**Problem:** Entry 3's single analysis pass can return `status: awaiting-clarification` when it has open questions, but nothing tells the human about them or closes the PR — the branch/PR entry 3 opened just sits there indefinitely, indistinguishable from a normal in-progress PR awaiting `plan-approval`.

**Approach:** When `run_analysis` writes `status: awaiting-clarification`, post the open question(s) as a comment on the PR entry 3 already opened, and close that PR in the same call (`gh pr close --comment`, AD-13/AD-15). No new behavior for the `ready-for-review` case.

**Decision:** no loop, no round counter — one analysis pass, immediate halt-and-surface on any open question. The real bounded multi-round design (agent retry across rounds, or a live human-reply exchange) is deferred post-v1, not forgotten — see `deferred-work.md` — user's call, 2026-10-02.

## Boundaries & Constraints

**Always:** the comment+close step is a deterministic script call (`open_implementation_pr.py`), never the analysis agent's own tool — mirrors AD-5/AD-12's "script, not agent" pattern entry 3 already established; reuse `AnalysisPROpenError`/`PROpenError` for this new failure mode rather than introducing a third post-analysis exception type, since it's the same category (a deterministic script step failing after analysis itself succeeded); never pass `--delete-branch` to `gh pr close` — AD-10/AD-12/AD-15's audit-trail-over-cleanup posture keeps branches and state directories in place, only the PR closes.

**Never:** no round-counter, no loop, no re-invocation of the analysis skill (per the 2026-10-02 simplification); no AD-15 supersession-closing (still entry 3's own deferred scope, unrelated to this ticket); no change to the `ready-for-review` path's existing behavior.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Open questions present | `run_analysis`'s one analysis pass returns non-empty `open_questions` | `plan.md`/`decisions.md` written with `status: awaiting-clarification` (entry 3's existing behavior, unchanged); PR comment posted listing the question(s); PR closed in the same call | n/a |
| No open questions | `open_questions` empty, `status: ready-for-review` | No new behavior — PR stays open exactly as entry 3 already leaves it | n/a |
| Comment/close step itself fails | `gh pr close` subprocess error | Raises `AnalysisPROpenError` (reused), distinguishable from `AnalysisHalted`/`AnalysisInvocationError`; `plan.md`/`decisions.md` and the PR remain exactly as entry 3 left them — only the comment/close didn't complete | Caller sees a clear, distinct exception, same as the existing PR-open failure case |

</frozen-after-approval>

## Code Map

- `factory/scripts/open_implementation_pr.py` -- new function `close_for_clarification(pr_number, open_questions, *, cwd=None) -> None`. Formats `open_questions` into a short Markdown list, then one call: `gh pr close <pr_number> --comment "<formatted list>"` (confirmed via `gh pr close --help`: `-c/--comment` posts a closing comment atomically — one subprocess call, no separate `gh pr comment`). Raises `PROpenError` on any subprocess failure, via the module's existing `_run` helper.
- `factory/graph/analysis_graph.py` -- edit `run_analysis`: after `open_pr_for_story` returns and `status == "awaiting-clarification"`, call `open_implementation_pr.close_for_clarification(pr["pr_number"], result["open_questions"], cwd=cwd)` inside the same `try`/`except open_implementation_pr.PROpenError` block already wrapping the PR-open call, re-raising as `AnalysisPROpenError`.
- `factory/scripts/tests/test_open_implementation_pr.py` -- new tests for `close_for_clarification`: success (asserts `gh pr close` called with the right PR number and a `--comment` containing the questions), and a subprocess failure raising `PROpenError`.
- `factory/graph/tests/test_analysis_graph.py` -- extend the existing `awaiting-clarification` test to assert `close_for_clarification` was called with the right args; add one test for its failure raising `AnalysisPROpenError`; the `ready-for-review` tests are unaffected (assert `close_for_clarification` not called).

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/open_implementation_pr.py` -- add `close_for_clarification` -- posts the open question(s) and closes the PR in one `gh pr close --comment` call
- [x] `factory/graph/analysis_graph.py` -- call it from `run_analysis` on `awaiting-clarification`, reusing the existing `AnalysisPROpenError` wrapping
- [x] `factory/scripts/tests/test_open_implementation_pr.py` -- new tests for the comment+close success and failure paths
- [x] `factory/graph/tests/test_analysis_graph.py` -- extend/add tests per the I/O Matrix
- [x] Run `uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py factory/scripts/tests/test_open_implementation_pr.py factory/scripts/tests/test_state_io.py` -- all pass

**Acceptance Criteria:**
- Given a story file with unresolved open questions, when the analysis job runs, then the PR entry 3 opened carries a comment listing those questions and is closed (not deleted — branch and state directory remain).
- Given a story file with no open questions, when the analysis job runs, then nothing about the PR changes beyond what entry 3 already does — it stays open.
- Given the `gh pr close` call itself fails, when `run_analysis` runs, then it raises `AnalysisPROpenError`, distinguishable from `AnalysisHalted` and `AnalysisInvocationError`.

## Implementation Notes

Implemented exactly per the Code Map: `close_for_clarification(pr_number, open_questions, *, cwd=None)` added to `factory/scripts/open_implementation_pr.py`, formatting the questions as a Markdown list and issuing one `gh pr close <pr_number> --comment "<list>"` call via the existing `_run` helper (raises `PROpenError` on failure). `run_analysis` in `factory/graph/analysis_graph.py` calls it immediately after `open_pr_for_story` returns, gated on `status == "awaiting-clarification"`, inside the same `try`/`except open_implementation_pr.PROpenError` block already wrapping the PR-open call, re-raised as `AnalysisPROpenError`. `ready-for-review` path untouched -- verified via `mock_close.assert_not_called()` in the existing test.

## Plan Change Log

## Review Triage Log

- **Module docstring's "fourth case" and "single-invocation call" paragraphs still say "entry 4's future loop"** — verdict: `medium`. Verified: `factory/graph/analysis_graph.py` lines ~24 and ~32 both reference "entry 4's future loop"/"its own loop node" — but this ticket *is* entry 4, and its own frozen Intent/Boundaries explicitly decided "no loop, no round counter... single-pass halt-and-surface" (2026-10-02 simplification). A future reader (or session) hitting this docstring without re-reading the plan would be misled into thinking a loop is still coming from some future "entry 4" that already shipped without one — a real, named confusion risk, not just staleness. Routed `patch`: direct text correction, no code/behavior change.
- **`build_graph`'s docstring still promises "Entry 4 wraps this node in a clarification-round loop"** — verdict: `medium`. Verified: same contradiction as above, at `factory/graph/analysis_graph.py`'s `build_graph` function. Routed `patch`.
- **`AnalysisPROpenError`'s "fifth case" docstring doesn't mention `close_for_clarification` as a source** — verdict: `low`. Verified: the docstring describes the exception as covering only "the deterministic branch/PR-open step," but this ticket's own Design Notes explicitly justify reusing this exact exception type for the new comment/close failure mode too — the module-level description of the exception's scope wasn't broadened to match. No behavior impact (callers already handle the exception type uniformly; the real `gh` error text is still in the message), but routed `patch` since the fix is a direct, trivial text correction, not rejected despite `low`.

## Design Notes

**Why reuse `AnalysisPROpenError` rather than a new exception type:** both this and the existing PR-open failure are "a deterministic script step failed after the analysis itself succeeded" — the same category a caller needs to distinguish from `AnalysisHalted` (a judgment) and `AnalysisInvocationError` (the `claude` CLI itself failing). A third post-analysis exception type for what is, to any caller, the identical kind of failure would be an unjustified abstraction.

**Why no loop, no counter:** per the 2026-10-02 simplification (see `deferred-work.md`) — the real bounded multi-round design (agent retry across rounds, mirroring AD-11's fix loop, or a live human-reply exchange reusing AD-2's Environment-gate pattern) was explicitly deferred, not forgotten. This ticket only builds what v1 actually needs: halt-and-surface on the first pass.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py factory/scripts/tests/test_open_implementation_pr.py factory/scripts/tests/test_state_io.py` -- expected: all pass

**Manual checks (if no CLI):**
- Inspect a sample PR comment's formatting for the `open_questions` list — no automated check for exact prose, just that each question renders as a readable list item.

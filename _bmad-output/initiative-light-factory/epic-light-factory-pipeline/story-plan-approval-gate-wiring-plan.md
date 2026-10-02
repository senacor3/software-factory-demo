---
title: 'plan-approval gate wiring'
type: 'feature'
ticket: '5'
created: '2026-10-02'
status: 'built'
baseline_revision: '594a75f86dce3b98f25bdcd530fd647f4ecc879b'
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

**Problem:** The `plan-approval` Environment pause is already wired (entry 1, `environment: plan-approval` on Job 2), but nothing posts the human-readable gate summary AD-4 requires. A story resolving to `ready-for-review` opens a PR with only a one-line description — the reviewer has no concise summary to decide from, only the full `plan.md`/`decisions.md` files.

**Approach:** When `run_analysis` resolves to `status: ready-for-review`, post a concise gate-summary PR comment (AD-4) — the proposal, subtask/test counts, and a pointer to `plan.md`/`decisions.md` for full detail — via a new shared `factory/scripts/post_summary.py`. `awaiting-clarification` is unaffected (entry 4 already posts its own comment and closes the PR).

**Decision:** scoped to the summary-posting half only. Reject-driven PR-closing is deferred — the Environment protection isn't active yet, and even once it is, GitHub Actions cannot cleanly distinguish a reviewer reject from an ordinary job failure without a separate deployment-review API call (verified, not assumed) — see `deferred-work.md` — user's call, 2026-10-02.

## Boundaries & Constraints

**Always:** the summary-posting step is a deterministic script call (`post_summary.py`), never the analysis agent's own tool — mirrors AD-5/AD-12's "script, not agent" pattern; reuse `AnalysisPROpenError` for this failure mode too (same category as the existing PR-open and clarification-close failures — a deterministic script step failing after analysis itself succeeded), via a new `post_summary.PostCommentError` caught alongside `open_implementation_pr.PROpenError`.

**Never:** no changes to the `environment: plan-approval` wiring itself (already correct, entry 1); no reject-detection or PR-closing on reject (deferred, see Decision above); no changes to the `awaiting-clarification` path (entry 4's own comment+close is untouched).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Resolves to `ready-for-review` | `run_analysis`'s analysis pass has no open questions | Gate-summary PR comment posted (proposal, subtask/test counts, pointer to `plan.md`/`decisions.md`); PR stays open for the `plan-approval` gate | n/a |
| Resolves to `awaiting-clarification` | Open questions present | This entry's summary comment is **not** posted — entry 4's own comment+close already ran | n/a — regression guard |
| Summary-posting step itself fails | `gh pr comment` subprocess error | Raises `AnalysisPROpenError` (reused), distinguishable from `AnalysisHalted`/`AnalysisInvocationError`; `plan.md`/`decisions.md` and the PR remain exactly as entry 3 left them | Caller sees a clear, distinct exception, same pattern as the existing PR-open/clarification-close failures |

</frozen-after-approval>

## Code Map

- `factory/scripts/post_summary.py` -- new, shared (AD-4 names this file for both gates — `plan-approval` here, `evidence-approval` in entry 11). `PostCommentError(RuntimeError)`; `post_comment(pr_number, body, *, cwd=None) -> None` — one `gh pr comment <pr_number> --body <body>` call (confirmed via `gh pr comment --help`), via a small local `_run` helper mirroring `open_implementation_pr.py`'s own (not imported — that helper is private to its module; duplicating five lines beats reaching into another module's internals).
- `factory/graph/analysis_graph.py` -- edit `run_analysis`: add `_render_plan_summary(result) -> str` (parallel to the existing `_render_plan_body`/`_render_decisions_body` helpers) formatting the proposal plus subtask/test counts and a `plan.md`/`decisions.md` pointer. After `open_pr_for_story` returns, branch on `status`: `awaiting-clarification` keeps calling `close_for_clarification` as today; the `else` (i.e. `ready-for-review`) branch calls `post_summary.post_comment(pr["pr_number"], _render_plan_summary(result), cwd=cwd)`. Both branches stay inside the existing `try`/`except` that catches `open_implementation_pr.PROpenError`, now also catching `post_summary.PostCommentError`, both re-raised as `AnalysisPROpenError`.
- `factory/scripts/tests/test_post_summary.py` -- new: `post_comment` success (asserts the right `gh pr comment` call shape) and subprocess-failure raising `PostCommentError`.
- `factory/graph/tests/test_analysis_graph.py` -- extend the `ready-for-review` test to assert `post_summary.post_comment` was called with the right PR number and a body containing the proposal; extend the `awaiting-clarification` test to assert it was **not** called; add one test for its failure raising `AnalysisPROpenError`.

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/post_summary.py` -- add `post_comment` and `PostCommentError`
- [x] `factory/graph/analysis_graph.py` -- add `_render_plan_summary`, call `post_summary.post_comment` on `ready-for-review`, reuse `AnalysisPROpenError`
- [x] `factory/scripts/tests/test_post_summary.py` -- new tests for success and subprocess-failure
- [x] `factory/graph/tests/test_analysis_graph.py` -- extend/add tests per the I/O Matrix
- [x] Run `uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py factory/scripts/tests/test_post_summary.py factory/scripts/tests/test_open_implementation_pr.py factory/scripts/tests/test_state_io.py` -- all pass

**Acceptance Criteria:**
- Given a story resolving to `ready-for-review`, when the analysis job runs, then the PR entry 3 opened carries a gate-summary comment (proposal, subtask/test counts, file pointer) and stays open.
- Given a story resolving to `awaiting-clarification`, when the analysis job runs, then no gate-summary comment from this entry is posted — only entry 4's existing comment+close.
- Given the `gh pr comment` call itself fails, when `run_analysis` runs, then it raises `AnalysisPROpenError`, distinguishable from `AnalysisHalted` and `AnalysisInvocationError`.

## Implementation Notes

## Plan Change Log

## Review Triage Log

- **Quick lens, 2026-10-02: no findings.** Verified against the plan's acceptance criteria, I/O Matrix, and Design Notes: `post_summary.py`'s `_run`/`post_comment`/`PostCommentError` match the Code Map exactly (duplication of `open_implementation_pr.py`'s helper explicitly justified, not a defect); `run_analysis`'s branching and exception reuse match; all three I/O Matrix rows have passing tests; no `AGENTS.md`/`CLAUDE.md` rules exist to check against. Full suite re-confirmed independently by the orchestrator: 73/73 pass. No loopback triggered.

## Design Notes

**Why a new shared `post_summary.py` rather than adding to `open_implementation_pr.py`:** the architecture's Structural Seed already names `post_summary.py` as the shared file for AD-4's gate-summary convention, used by both `plan-approval` (this entry) and `evidence-approval` (entry 11) — it's not a hypothetical future need, it's an already-named piece of the system. `open_implementation_pr.py` is thematically about branch/PR lifecycle (open, close), not about formatting stage-specific summaries.

**Why reuse `AnalysisPROpenError` again:** same reasoning as entry 4's Design Notes — every post-analysis deterministic-script failure (PR-open, clarification-close, now summary-post) is the same category to a caller: a script step failed after the analysis itself succeeded. A fourth distinct exception type for the same category would be an unjustified abstraction.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py factory/scripts/tests/test_post_summary.py factory/scripts/tests/test_open_implementation_pr.py factory/scripts/tests/test_state_io.py` -- expected: all pass

**Manual checks (if no CLI):**
- Inspect a sample gate-summary comment for readability — no automated check for exact prose, just that the proposal, counts, and file pointer all render clearly.

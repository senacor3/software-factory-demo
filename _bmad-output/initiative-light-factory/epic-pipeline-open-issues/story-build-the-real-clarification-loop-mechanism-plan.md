---
title: 'Build the real clarification-loop mechanism'
type: 'feature'
ticket: '2'
created: '2026-10-11'
status: done
baseline_revision: 'de99b97f8c59b09b7dde278df54c587e6091c439'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['_bmad-output/initiative-light-factory/change-clarification-loop-bounded-rounds/change-clarification-loop-bounded-rounds.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `analysis_graph.py`'s clarification halt is still the v1 single-pass placeholder: every open question halts, closes the PR, and waits for an out-of-band re-trigger, with no bound and no distinction between a first attempt and a tenth. Ticket 2.1 decided the real mechanism ("Option C" — bounded rounds via re-trigger) and amended `spec-light-factory.md`/`architecture-light-factory.md` to describe it, but wrote no code.

**Approach:** Add a round-counting query over this story-slug's prior `clarification-round`-labeled PRs, **any state** (open or closed — not just closed, so the count stays correct even when a capped PR is left open), decide `awaiting-clarification` vs. `clarification-cap-reached` (cap 2, matching AD-11) before `plan.md`/`decisions.md` are written, and register the new status value in AD-10's enum. Below cap: label and close the PR with the open-questions comment, unchanged from today. **At cap (user's call, 2026-10-11): leave the PR open**, labeled, with a comment saying the clarification budget is spent and it is up to the developer to decide how to proceed — not closed automatically.

## Boundaries & Constraints

**Always:** the round count considers PRs in **any state** (open or closed) carrying the `clarification-round` label, narrowed to this exact story-slug's branch prefix (`light-factory/<story-slug>/*`) — never another story-slug's PRs. Counting "any state," not just closed, is what keeps the cap sticky once a capped PR is left open. The `clarification-round` label is created idempotently (`gh label create ... --force`) so a fresh target repo needs no manual setup, mirroring how Environments needed one-time setup for epic 1. The cap stays at 2, per the approved Sprint Change Proposal (`change-clarification-loop-bounded-rounds/`).

**Never:** no live mid-job wait is introduced — AD-2's two-gate model is untouched. `fix_loop_graph.py`'s own counter/cap is a separate mechanism and is not touched. Branches and state directories are never deleted (AD-10/AD-12/AD-15's audit-trail-over-cleanup posture) — a below-cap PR still only ever closes, never deletes anything, and an at-cap PR isn't even closed. **Never close the PR at cap-reached** — it stays open for the developer to act on. Never implement AD-15's general supersession-closing here — that's a separate, already-planned entry (epic-pipeline-open-issues/4), kept independently scoped. A developer who ignores a stopped, capped PR and re-triggers anyway will get a second open, also-capped, also-unclosed PR, repeating on every further ignored re-trigger — an accepted, documented limitation until that entry ships, not a defect to fix here (user's call, 2026-10-11; see `deferred-work.md`).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Round 1 | open_questions present, 0 prior `clarification-round`-labeled PRs (any state) for this slug | `status: awaiting-clarification`; PR labeled, closed, normal open-questions comment | No error expected |
| Round 2 (below cap) | 1 prior labeled PR (any state) for this slug | `status: awaiting-clarification`; same as round 1 | No error expected |
| Round 3 (at/above cap) | 2+ prior labeled PRs (any state) for this slug | `status: clarification-cap-reached`; PR labeled, **left open**, comment says the budget is spent and it's up to the developer to decide how to proceed | No error expected |
| Ignored re-trigger past the cap | an open, capped PR already exists for this slug; developer re-triggers anyway | New run's analysis also resolves to `clarification-cap-reached` (count already ≥ cap); its own new PR is opened, labeled, and also left open — no automatic closing of the prior one | No error — known, documented limitation (see Boundaries), not a defect |
| Decoy PR | a `clarification-round`-labeled PR exists for a *different* story-slug's branch | Not counted — prefix filter excludes it | No error expected; covered by a unit test |
| `gh` failure during round-count, label-create, label-add, close, or comment-post | any `gh` subprocess error | `AnalysisPROpenError` raised; `plan.md`/`decisions.md` are **not yet written** if the failure is in round-counting (it now runs before the state write), or **are already written** if the failure is in labeling/closing/commenting (runs after) | `AnalysisPROpenError`, both cases |

</frozen-after-approval>

## Code Map

- `factory/scripts/state_io.py` (~line 67) — `STATUS_BY_STAGE["analysis"]` frozenset: add `"clarification-cap-reached"` alongside the existing three values. One-line change; this is the only place AD-10's enum is enforced.
- `factory/scripts/open_implementation_pr.py` — add `CLARIFICATION_CAP = 2` and `CLARIFICATION_LABEL = "clarification-round"` module constants; add `count_clarification_rounds(story_slug, *, cwd=None) -> int` (lists PRs with `--label clarification-round --state all`, then filters client-side by branch-prefix — `gh pr list --head` only matches an exact branch, not a prefix, so this can't reuse `find_open_pr`'s query shape directly; `--state all` so an open, capped PR still counts); add `clarification_status(story_slug, *, cwd=None) -> str` (wraps the count against the cap); `close_for_clarification` keeps its original signature/behavior unchanged (below-cap path only: label, comment, close); add a **new** `post_clarification_cap_notice(pr_number, open_questions, *, cwd=None) -> None` (labels the PR, posts the budget-spent/decide-how-to-proceed comment, does **not** close it — the at-cap path). Update the module docstring's "Does NOT implement AD-15 supersession-closing" note to also flag that leaving a capped PR open can leave two+ open PRs for the same slug on a repeated ignored re-trigger, until that entry ships.
- `factory/graph/analysis_graph.py`, `run_analysis` (~lines 187-234) — when `open_questions` is present, call `open_implementation_pr.clarification_status(story_slug, cwd=cwd)` (wrapped in its own try/except converting `PROpenError` → `AnalysisPROpenError`, since this now runs *before* the state write, unlike the existing try/except around PR-open/comment calls) to get `status`, instead of hardcoding `"awaiting-clarification"`. In the existing PR-handling try block, branch three ways: `status == "awaiting-clarification"` → `close_for_clarification` (unchanged call); `status == "clarification-cap-reached"` → the new `post_clarification_cap_notice`; else → `post_summary.post_comment` (unchanged). Update `AnalysisPROpenError`'s docstring: state files may or may not exist yet depending on which step raised it (previously always "already written").
- `factory/scripts/tests/test_open_implementation_pr.py` — new tests for `count_clarification_rounds` (0 prior, 1 prior open, 1 prior closed, a decoy PR from a different slug excluded) and `clarification_status` (below cap, at cap); new tests for `post_clarification_cap_notice` (labels, comments, does **not** call `gh pr close`); `close_for_clarification`'s existing tests are unchanged (its behavior didn't change).
- `factory/graph/tests/test_analysis_graph.py` — update the two existing clarification tests (`test_complete_with_open_questions_writes_awaiting_clarification`, `test_close_for_clarification_failure_raises_analysis_pr_open_error_but_state_files_remain`) to mock `clarification_status` returning `"awaiting-clarification"`; add a new test for the cap-reached path (mocks `clarification_status` returning `"clarification-cap-reached"`, asserts `plan.md`/`decisions.md`'s status, that `post_clarification_cap_notice` was called, and that `close_for_clarification` was **not**); add a new test asserting a `clarification_status` failure raises `AnalysisPROpenError` with **no** state files written (the new, earlier failure point).

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/state_io.py` -- add `"clarification-cap-reached"` to `STATUS_BY_STAGE["analysis"]` -- AD-10 must accept the new status or every write call raises `ValueError`
- [x] `factory/scripts/open_implementation_pr.py` -- add `count_clarification_rounds` (any-state, labeled, prefix-filtered), `clarification_status`, and the new `post_clarification_cap_notice` (labels + comments, never closes); leave `close_for_clarification` unchanged -- the actual counting and cap-decision mechanism
- [x] `factory/graph/analysis_graph.py` -- wire `clarification_status` into `run_analysis` before the state write, branch to `close_for_clarification` (below cap) or `post_clarification_cap_notice` (at cap), update `AnalysisPROpenError`'s docstring -- connects the new mechanism to the existing flow
- [x] `factory/scripts/tests/test_open_implementation_pr.py` -- unit-test the new functions directly (mocked `gh` subprocess calls), including the decoy-PR prefix-filter case and an open (not just closed) prior PR counting correctly
- [x] `factory/graph/tests/test_analysis_graph.py` -- update/add tests covering both the below-cap and at-cap paths through `run_analysis`, and the new earlier failure point

**Acceptance Criteria:**
- Given a story-slug with 0 or 1 prior `clarification-round`-labeled PRs (any state), when analysis returns open questions, then `plan.md`/`decisions.md`'s status is `awaiting-clarification`, the PR is labeled, and it is closed with the open-questions comment.
- Given a story-slug with 2 or more prior `clarification-round`-labeled PRs (any state), when analysis again returns open questions, then `plan.md`/`decisions.md`'s status is `clarification-cap-reached`, the PR is labeled, and it **stays open** with a comment saying the budget is spent and it's up to the developer to decide how to proceed.
- Given an open, capped PR already exists for a story-slug, when the developer re-triggers anyway, then the new run also resolves to `clarification-cap-reached` and its own PR is also left open — documented as a known limitation, not a defect, pending the separate AD-15 supersession-closing entry.
- Given a labeled PR for a *different* story-slug, when counting this slug's rounds, then that PR is not counted.
- Given any `gh` failure in the round-count, label, close, or comment steps, when `run_analysis` runs, then `AnalysisPROpenError` is raised (never a raw `PROpenError`).

## Implementation Notes

The Code Map names three new `open_implementation_pr.py` functions (`count_clarification_rounds`, `clarification_status`, `post_clarification_cap_notice`) and says `close_for_clarification` keeps its original signature/behavior unchanged, with its existing tests unchanged. Taken together, those two constraints leave no function that applies the `clarification-round` label on the **below-cap** path (round 1/2's PR must still be labeled per the I/O Matrix and Acceptance Criteria, but putting that call inside `close_for_clarification` would add a second subprocess call and break `test_close_for_clarification_posts_comment_and_closes_pr`'s `len(calls) == 1` assertion, which the Code Map says must stay unchanged). Resolved by adding one small new function, `label_clarification_round(pr_number, *, cwd=None)` (idempotent `gh label create ... --force` + `gh pr edit --add-label`), called from two places: directly in `run_analysis`'s below-cap branch (alongside the still-unchanged `close_for_clarification` call) and internally by `post_clarification_cap_notice` for the at-cap path. This satisfies the Acceptance Criteria's "PR is labeled" requirement on both paths while leaving `close_for_clarification` and its tests byte-for-byte as they were.

Order of operations in `run_analysis`'s below-cap branch is label-then-close (`label_clarification_round` before `close_for_clarification`), so a label failure never leaves a closed-but-unlabeled PR that would undercount on the next round.

## Plan Change Log

- **2026-10-11 — added `label_clarification_round` (not explicitly named in the Code Map).** See Implementation Notes above: the Code Map's "`close_for_clarification` unchanged, tests unchanged" constraint left no other place to apply the below-cap path's label without a new function. Everything else matches the Code Map and I/O Matrix exactly (constants, `count_clarification_rounds`'s query shape, `clarification_status`'s cap comparison, `post_clarification_cap_notice`'s label+comment+never-close behavior, `AnalysisPROpenError`'s updated docstring, and the earlier failure point moving before the state write).
- **2026-10-11 — review loopback: same-run-id retry double-count, and stale AD-13/AD-15 architecture text.** Triaged findings: (1) `count_clarification_rounds`/`clarification_status` ran before `open_implementation_pr.open_pr_for_story` creates/finds the current run's own PR, so a same-run-id retry after a partial failure (e.g. `label_clarification_round` already succeeded, then `close_for_clarification`/`post_clarification_cap_notice` failed) would see its own already-labeled PR matching the branch prefix and double-count it as a prior round. Fixed by threading `run_id` through both functions and excluding the exact branch `light-factory/<story_slug>/<run_id>` from the count; added `test_count_clarification_rounds_excludes_own_run_id_branch_on_same_run_retry` and updated every other call site/test for the new signature. (2) `architecture-light-factory.md`'s AD-13 Rule and AD-15 Rule still described the round-count as querying prior **closed** PRs only, and AD-15 still asserted an open PR always means "still awaiting a decision" -- both stale against the shipped `--state all` design and the at-cap-PR-stays-open-but-is-terminal behavior. Updated both Rules to describe the any-state query and carve out the at-cap case explicitly.

## Review Triage Log

Quick lens, 1 run, 2 findings — both verified real, both `medium`, both route to `patch`.

- `architecture-light-factory.md`'s AD-13/AD-15 Rules still say the round-count queries prior **closed** PRs only, and AD-15 still asserts "an open PR always means still awaiting a decision, never already resolved." Verified: `count_clarification_rounds` queries `--state all` (confirmed in the diff), and the at-cap PR is deliberately left open yet is a resolved/terminal state (user's call, 2026-10-11) — both now stale against ticket 2.2's actual decided/shipped design, one day after AD-13/AD-15 were last amended (ticket 2.1, 2026-10-10). Medium: misleads anyone reading these ADs, notably entry 2.4's future builder, into a wrong mental model of what "open PR" means. **Patch.**
- `count_clarification_rounds` is called (via `clarification_status`) before `open_pr_for_story` creates/reuses the current run's own PR. Verified: on a same-run-id retry after a partial failure (label succeeds, then `close_for_clarification`/`post_clarification_cap_notice` fails), the retry's own round-count query matches its own already-open, already-labeled PR under the matching branch prefix, double-counting it as a prior round — `open_pr_for_story`'s own docstring confirms same-run-id retries are an expected, supported scenario this ticket's reordering didn't account for. Medium: can trip `clarification-cap-reached` one round earlier than real distinct human rounds warrant, in a realistic (if narrow) retry scenario. **Patch.**

## Design Notes

`gh pr list --head` only matches one exact branch name — it has no prefix/glob mode — so `count_clarification_rounds` can't reuse `find_open_pr`'s query shape. It instead lists PRs by `--label` with `--state all` (repo-wide, `--limit 100`) and filters client-side on `headRefName.startswith(f"light-factory/{story_slug}/")`. `--state all`, not `--state closed`, is deliberate: an at-cap PR is left open, and it must still count toward the cap on a later re-trigger (otherwise the cap would silently reset). Known PoC-scope limitation, consistent with AD-15's own unpaginated search: a repo with more than 100 labeled PRs across *all* story-slugs could undercount a given slug's rounds. Not worth solving now — no existing query in this codebase paginates either.

`gh label create --force` is idempotent (creates or updates), so no manual one-time label setup is needed on a fresh target repo, unlike the Environments that did need manual creation in epic 1.

Leaving the at-cap PR open means two+ open PRs can exist for the same story-slug if a developer ignores it and re-triggers anyway — there is no supersession-closing yet (a separate, already-planned entry). This is an accepted, documented limitation (Boundaries, `deferred-work.md`), not something this ticket fixes.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/scripts/tests/test_open_implementation_pr.py factory/graph/tests/test_analysis_graph.py -q` -- expected: all pass, including new cap/decoy/early-failure cases -- **ran 2026-10-11: 42 passed**
- `uv run --with pytest pytest factory/ -q` -- expected: full suite green, no regressions elsewhere -- **ran 2026-10-11: 174 passed**
- `uv run --with ruff ruff check factory/` -- expected: clean (lint is real since ticket 1.13) -- **ran 2026-10-11: All checks passed!**

No live `gh workflow run` dispatch was performed for this ticket -- the plan calls for unit-test verification only (matching the existing `git`/`gh` subprocess-mocking convention in both test files; no real `git`/`gh` process runs in the committed suite), and this ticket adds no workflow-file changes to re-dispatch.

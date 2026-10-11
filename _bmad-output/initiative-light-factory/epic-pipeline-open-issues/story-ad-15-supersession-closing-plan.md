---
title: 'AD-15 supersession-closing'
type: 'feature'
ticket: '4'
created: '2026-10-11'
status: 'built'
baseline_revision: '2922f6d6fce8ec455336062c07a5cd055f33aedf'
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

**Problem:** A re-triggered run opens a new PR on `light-factory/<story-slug>/<run-id>` but never closes its predecessor's, so every rejected, cancelled, or at-cap run leaves another open PR for the same story-slug that has to be closed by hand (AD-15's supersession rule is unbuilt).

**Approach:** Inside AD-12's deterministic PR-open step, after this run's PR exists, find every other open PR whose head branch starts with `light-factory/<story-slug>/`, close each with a "Superseded by #N" comment, and post one "Retry of #M" comment on the new PR.

## Boundaries & Constraints

**Always:** Supersession is a deterministic script step, never an agent action (AD-5/AD-12). Match by branch-name prefix `light-factory/<story-slug>/` with the trailing slash, excluding this run's own branch. Only the PR closes — never `--delete-branch`, never touch state directories (AD-10/AD-12/AD-15). Any `git`/`gh` failure raises `PROpenError`, like every other call in the module. A same-run-id job re-run must be able to finish a supersession its first attempt left incomplete. An at-cap PR that AD-13 deliberately left open is superseded like any other open PR on the next re-trigger; it still counts toward the clarification cap because that count queries all states.

**Never:** No change to `count_clarification_rounds`/`clarification_status` (separate any-state query). No change to `find_open_pr`'s signature or return shape (`merge_story.py`, `post_evidence_summary.py` depend on it). No change to `.github/workflows/light-factory.yml` — Job 1 already holds `pull-requests: write` and `GH_TOKEN`. No pagination beyond `--limit 100` (existing documented PoC limitation). No reject-closes-PR logic (entry 5). No new state or pointer file. No live `gh workflow run` dispatch and no push to `main` in this ticket — verification is unit tests only; the live two-dispatch proof is carried by entry 7 (user's call, 2026-10-11).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| First run for a slug | No other open PR with the prefix | PR opened; no close, no "Retry of" comment | No error expected |
| Re-trigger, one predecessor | Open PR #7 on `light-factory/foo/run-1`; new run `run-2` opens #9 | #7 closed with "Superseded by #9"; #9 gets one comment "Retry of #7" | No error expected |
| Cascading predecessors | Open PRs #5 and #7 for `foo` (a cancelled run never closed its own) | Both closed, each linking #9; #9 gets one comment naming #5 and #7 | No error expected |
| Other story's PR | Open PR on `light-factory/foo-bar/run-3` or `light-factory/other/run-4`, or a non-factory branch | Untouched | No error expected |
| Same-run-id re-run | This run's PR #9 already open; predecessor #7 still open | Existing PR returned, nothing recreated; #7 still superseded | No error expected |
| Supersession failure | `gh pr list`/`close`/`comment` exits non-zero | Run fails; new PR stays open | `PROpenError` → `AnalysisPROpenError` |

</frozen-after-approval>

## Code Map

- `factory/scripts/open_implementation_pr.py` -- the only production file to change. `_run` (line 52) wraps every subprocess and raises `PROpenError`; reuse it. `find_open_pr` (65) is exact-branch only — do not change. `count_clarification_rounds` (79) shows the house pattern for a prefix search: `gh pr list ... --limit 100 --json ...` then client-side `startswith(prefix)` and own-branch exclusion; mirror it with `--state open --json number,headRefName`. `open_pr_for_story` (140) has two return points (existing PR at 155–157, created PR at 196–199); supersession must run before both. `close_for_clarification` (202) shows `gh pr close <n> --comment <text>` without `--delete-branch`. Module docstring lines 17–23 say supersession is not implemented and describe the at-cap accumulation limitation — both become untrue.
- `factory/graph/analysis_graph.py` -- sole caller (line 244), inside the `try` that maps `PROpenError` to `AnalysisPROpenError`; no code change needed. Its module docstring (32–35) and `AnalysisPROpenError` docstring (83–91) enumerate the failing steps and should name supersession.
- `factory/scripts/tests/test_open_implementation_pr.py` -- mocks `open_implementation_pr.subprocess.run` with a `fake_run(cmd, ...)` dispatcher keyed on `cmd[:3]`. Existing `open_pr_for_story` tests key on `["gh","pr","list"]` and count identical calls; the new prefix query is also `gh pr list`, so they need to tell `--head` queries from the prefix query. `test_idempotent_reuse_returns_existing_pr_without_recreating` (109) asserts the exact call list and must expect the added query.
- `factory/graph/tests/test_analysis_graph.py` -- mocks `open_pr_for_story` wholesale; unaffected.
- `_bmad-output/initiative-light-factory/deferred-work.md` line 14–17 -- the source entry; gets a `resolved:` line once built, following the file's existing convention.

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/open_implementation_pr.py` -- add `supersede_prior_prs(story_slug, run_id, new_pr_number, *, cwd=None) -> list[int]`: list open PRs, keep those on the slug prefix other than this run's branch, close each with "Superseded by #N", then post one "Retry of #M[, #K]" comment on the new PR only when at least one was closed; return the closed numbers in ascending order -- the AD-15 rule itself
- [x] `factory/scripts/open_implementation_pr.py` -- call it from `open_pr_for_story` on both the existing-PR and freshly-created paths, keeping the returned dict unchanged -- a re-run must complete an interrupted supersession
- [x] `factory/scripts/open_implementation_pr.py` -- rewrite module docstring lines 17–23 to describe supersession and drop the accumulation limitation -- the text is now false
- [x] `factory/graph/analysis_graph.py` -- name the supersession step in the two docstrings that list `AnalysisPROpenError` sources -- keep the failure taxonomy accurate
- [x] `factory/scripts/tests/test_open_implementation_pr.py` -- add tests for every matrix row (including a `foo-bar` decoy for slug `foo`, no `--delete-branch`, comment text and target numbers) and adapt the existing `open_pr_for_story` tests to the extra query
- [x] `_bmad-output/initiative-light-factory/deferred-work.md` -- append a `resolved:` line to the AD-15 supersession entry -- the gap it parks is closed

**Acceptance Criteria:**
- Given a story-slug with an open PR from an earlier run, when a new run's PR is opened, then exactly one PR for that slug is open afterwards, the older one carries a comment linking the new one, and the new one carries a comment linking the older one.
- Given a predecessor PR that was already closed, when a new run's PR is opened, then no close and no "Retry of" comment is issued for it.
- Given the full existing suite, when it runs after the change, then every previously passing test still passes.

## Implementation Notes

- 2026-10-11: implemented as planned in `factory/scripts/open_implementation_pr.py` (`supersede_prior_prs`, called on both return paths of `open_pr_for_story`), docstrings in `factory/graph/analysis_graph.py`, tests in `factory/scripts/tests/test_open_implementation_pr.py`, and a `resolved:` line in `deferred-work.md`.
- Addition beyond the plan: the filter also excludes `new_pr_number` itself, so the new PR can never be closed even if its branch name differed from the computed one.
- Review patch: the order is now comment first, close second (the reverse of what Design Notes originally said). Closing first meant a same-run-id re-run after a partial failure could not name predecessors that were already closed, which broke the frozen re-run rule.
- Below-cap clarification runs end with zero open PRs for the slug (predecessor superseded, then the new PR closed for clarification); "exactly one open PR" holds for the ready-for-review and at-cap outcomes.
- Verification ran 2026-10-11: targeted suite 56 passed; `pytest factory/` 188 passed; `ruff check factory/` clean. No live dispatch, per the frozen block.

## Plan Change Log

## Review Triage Log

Pass 1 (quick lens, 2026-10-11) — high 0, medium 0, low 3, false 1, maybe-false 1.

| # | Finding | Verdict | Route | Evidence |
|---|---------|---------|-------|----------|
| 1 | `supersede_prior_prs` closed first, commented second: a re-run after a partial failure could not restore the "Retry of" back-link | low | patch | Real: after a failed comment or a partial cascade, the re-run's open-PR query no longer returns the closed predecessors. Reordered to comment first, then close; tests updated. |
| 2 | Two story files with the same basename share a slug but not a concurrency group, so simultaneous runs can close each other's PRs; re-running an older run closes a newer PR | low | defer | Real for the same-basename case: `.github/workflows/light-factory.yml` keys concurrency on raw `story_file`, while AD-15 specifies the slug. The keying predates this change and the workflow is outside this ticket. The older-run re-run case is AD-15's intended "a re-trigger always supersedes". |
| 3 | A predecessor closed or merged between the list and the close either fails the run or yields a one-sided link | maybe-false | reject | `gh pr close` behaviour on an already-closed PR was not verified by the reviewer or here; settling it needs a real `gh` call. If true it would be low: a milliseconds-wide window ending in a failed, re-runnable job. |
| 4 | No supersession-specific test for the `PROpenError` → `AnalysisPROpenError` mapping | false | reject | `test_pr_open_failure_raises_analysis_pr_open_error_but_state_files_remain` in `factory/graph/tests/test_analysis_graph.py` covers the mapping for any `PROpenError` raised by `open_pr_for_story`, which is the only way a supersession failure surfaces. |
| 5 | Test module docstring line about 115 characters against a wrap near 90 | low | patch | Real, cosmetic; rewrapped. |

## Design Notes

"Retry of #M" is a `gh pr comment`, not part of the `gh pr create` body: the ticket says "post … on the new PR", and a comment also works on the same-run-id re-run path where the PR already exists. Comment first, close second (changed in review, see Implementation Notes) — a failure part-way leaves the back-link complete, and a re-run closes whatever is still open, at worst with a duplicate comment.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/scripts/tests/test_open_implementation_pr.py factory/graph/tests/test_analysis_graph.py -q` -- expected: all pass, including the new supersession cases
- `uv run --with pytest pytest factory/ -q` -- expected: full suite green (174 passed before this change, plus the new tests)
- `uv run --with ruff ruff check factory/` -- expected: All checks passed!

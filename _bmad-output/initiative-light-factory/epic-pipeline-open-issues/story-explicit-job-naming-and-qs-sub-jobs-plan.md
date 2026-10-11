---
title: 'Explicit job naming and QS sub-jobs'
type: 'refactor'
ticket: 8
created: '2026-10-11'
status: done
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['.github/workflows/light-factory.yml']
baseline_revision: '33383b856b88122d905987a9850db45ac01db02d'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The workflow's jobs are named "Job 1: Analysis" / "Job 2: Implementation" / "Job 3: Merge" — a generic numbered prefix. "Job 2" also buries 5 distinct QS steps (4 checks + review/fix-loop) as sub-tasks instead of their own sub-jobs.

**Approach:** Drop "Job N:" everywhere, matching "Close PR on gate reject" (no prefix already). Extract QS into two new jobs after Implementation: `checks` (build/test/lint/security) then `review` (review + bounded fix-loop, posts the evidence-approval summary). No behavior change: `plan-approval`/`evidence-approval` stay on the same two job entries (AD-2); only ungated jobs are inserted. Evidence crosses the new boundaries by always git-committing it (new CLIs on `checkout_branch.py`/`commit_push_implementation.py`), reusing the existing persistence mechanism.

Scope is the workflow file and the code it restructures. `architecture-light-factory.md`'s diagram/prose and the `SKILL.md` files also say "Job 1/2/3" but are deferred to entry 6 ("Refactor sweep"), which already names entry 8 as a doc-drift source.

## Boundaries & Constraints

**Always:** Exactly two gates, same two job entries as today (AD-2). Check/review commands, schemas, evidence shape unchanged (AD-6/AD-10) — only *where* code runs moves.

**Never:** No third gate. No logic change inside `run_checks.py`/`review_graph.py`/`fix_loop_graph.py` — only checkout/commit steps around them. No duplicate AD-8 assertion in `checks`/`review`. No edits to `architecture-light-factory.md` or `SKILL.md`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Trivial story, zero fix cycles | Review passes clean | `checks`/`review` each commit evidence; `review` posts the summary; `merge` proceeds | None |
| `checks` fails (build regresses) | `build` exits non-zero | `review`/`merge` skipped; `close-rejected-pr` does NOT run — PR stays open | Job failure, no PR mutation |
| Fix loop uses both cycles | `review` returns findings twice | Fix-loop unchanged; evidence committed once, after the loop | None |
| `plan-approval` rejected | Reject at Implementation's gate | Rest skipped; `close-rejected-pr` closes the PR (unchanged) | Existing path, untouched |

</frozen-after-approval>

## Code Map

- `.github/workflows/light-factory.yml` — rename `analysis`→"Analysis", `implementation`→"Implementation"; move the 4 check steps + "Run review"/"Post evidence-approval summary" out of `implementation`. New job `checks` (`needs: implementation`, `contents: write`): Checkout, Install uv, "Checkout implementation branch" (new CLI), the 4 unchanged check steps, "Commit checks evidence" (`--label Checks`). New job `review` (`needs: [analysis, implementation, checks]`, `contents: write`, `pull-requests: write`): Checkout, Install uv, "Checkout implementation branch", Install Node + Claude CLI, unchanged "Run review (bounded fix loop)", "Commit review evidence" (`--label Review`), "Post evidence-approval summary" moved here. `merge`: rename "Merge", `needs: [analysis, implementation, review]`. `close-rejected-pr`: unchanged.
- `factory/scripts/checkout_branch.py` — thin CLI `main()` (`--story-slug`, `--run-id`) around the unchanged `checkout_branch()`.
- `factory/scripts/commit_push_implementation.py` — keyword-only `label: str = "Implementation"` on `commit_and_push` (used in the commit message); thin CLI (`--story-slug`, `--run-id`, `--label`) deriving `branch` and calling it. Existing callers unaffected.
- `factory/scripts/tests/test_checkout_branch.py`, `test_commit_push_implementation.py` — new CLI/`label` tests only.
- Docstrings naming "Job 1/2/3" in `analysis_graph.py`, `implementation_graph.py`, `review_graph.py`, `fix_loop_graph.py`, `commit_push_implementation.py`, `run_checks.py`, `post_evidence_summary.py`, `checkout_branch.py`, `merge_story.py`, `open_implementation_pr.py` — text-only reword.

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/checkout_branch.py` -- add CLI `main()`
- [ ] `factory/scripts/commit_push_implementation.py` -- add `label` param + CLI `main()`
- [ ] `factory/scripts/tests/test_checkout_branch.py` -- CLI tests
- [ ] `factory/scripts/tests/test_commit_push_implementation.py` -- CLI + `label` tests
- [ ] `.github/workflows/light-factory.yml` -- rename jobs, extract `checks`/`review`, rewire `needs:`/gates per Code Map
- [ ] Docstrings in the 10 files above -- reword Job-N mentions

**Acceptance Criteria:**
- Given the changed workflow file, when parsed as YAML, it loads with 6 jobs — `analysis`, `implementation`, `checks`, `review`, `merge`, `close-rejected-pr` — none named "Job N: ...".
- Given a trivial story with zero fix cycles, when the pipeline runs, then `checks`'/`review`'s evidence is committed right after each job finishes.
- Given `pytest factory/`, when run after the change, then every previously passing test still passes, plus the new CLI tests.
- Given a `checks` failure, when the run finishes, then `close-rejected-pr` did not run and the PR is still open.

## Implementation Notes

- 2026-10-11: implemented as planned. `checkout_branch.py`/`commit_push_implementation.py` got their new CLIs (`label` kwarg added to `commit_and_push`, default `"Implementation"`, unaffected existing callers), with new CLI/`label` tests. `.github/workflows/light-factory.yml` now has 6 jobs (`analysis`, `implementation`, `checks`, `review`, `merge`, `close-rejected-pr`); `implementation`'s `pull-requests: write` permission was dropped (no PR comment posted there anymore -- moved to `review`). Docstrings in all 10 files named in the Code Map reworded off "Job 1/2/3".
- The first implementation attempt (a subagent) stalled after finishing the two script/test files and was no longer addressable; this session verified its partial work (tests passing) and finished the rest (workflow.yml + docstrings) directly.
- I/O & Edge-Case Matrix rows 2 and 4 (job-skip/`close-rejected-pr` trigger behavior) are GitHub Actions `needs:`/`if:` semantics with no local test harness in this repo -- consistent with how entries 4 and 5 left their own gate/reject-detection wiring "unproven until entry 7" (live dispatch), these rows stay unverified by unit test here and are expected to be proven live, likely folded into entry 7.

## Plan Change Log

## Review Triage Log

Pass 1 (quick lens, 2026-10-11) — high 1, medium 0, low 0, false 0, maybe-false 0.

| # | Finding | Verdict | Route | Evidence |
|---|---------|---------|-------|----------|
| 1 | `checks` job's `needs: implementation` omits `analysis`, so every `needs.analysis.outputs.*` reference inside it (branch checkout + all 4 checks + evidence commit, 6 occurrences) resolves empty, failing the job's checkout step on every run, not just the documented failure case | high | patch | Verified: GitHub Actions exposes `needs.<job>.outputs` only for jobs listed directly in a job's own `needs:`, never transitively; `review`/`merge`/`close-rejected-pr` all correctly list `analysis` directly, `checks` alone omits it. Traced to the plan's own Code Map (`needs: implementation`), faithfully carried into the diff. Fixed by adding `analysis` to `checks`' `needs:` array. |

## Design Notes

- `checks` needs no Node/Claude CLI install — its subcommands never invoke `claude`.
- The new "Commit review evidence" step unconditionally persists `review.md`/evidence even on a clean first pass; `fix_loop_graph.py`'s own conditional fix-cycle commits are untouched and independent of it.
- `architecture-light-factory.md`/`SKILL.md`'s Job-N wording is intentionally left as-is — deferred to entry 6.

## Verification

**Commands:**
- `pytest factory/` -- all pass, incl. new CLI tests
- `ruff check factory/` -- clean
- `python -c "import yaml; yaml.safe_load(open('.github/workflows/light-factory.yml'))"` -- parses, 6 jobs

**Manual checks (if no CLI):** A live dispatch (likely folded into entry 7) showing separate evidence commits from `checks`/`review` before merge.

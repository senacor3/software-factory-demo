---
title: 'Refactor sweep'
type: 'chore'
ticket: '6'
created: '2026-10-11'
status: 'built'
baseline_revision: '05630a5a691f81e1c78aa68085eede7a81e1ebdd'
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

**Problem:** Entries 1, 2, 4, 5 and 8 left the docs behind the code: the architecture spine and the three `SKILL.md` files still describe a three-job "Job 1/2/3" pipeline (it has six named jobs), say an at-cap clarification PR is closed (it stays open), and never record how evidence crosses the new `checks`/`review` job boundaries. Three review findings also sit open in `deferred-work.md` with no disposition.

**Approach:** Bring docs, comments and docstrings in line with the shipped code, with zero behavior change, and give every deferred finding from those entries a recorded disposition: resolved here, or re-parked with a reason.

## Boundaries & Constraints

**Always:** Text follows the code as shipped at `05630a5` — when they disagree, the doc changes, never the code. Jobs are named by their workflow ids (`analysis`, `implementation`, `checks`, `review`, `merge`, `close-rejected-pr`). `SKILL.md` and `factory/` text names stages, not workflow jobs (the spine's own portability invariant). Every architecture edit keeps the AD's Binds/Prevents/Rule form. Dispositions follow epic 1 entry 12's precedent: one dated note in the epic file's Notes, plus a line on each `deferred-work.md` entry.

**Never:** No change to any executable line, `if:`/`needs:`/`permissions:`/`concurrency:` value, schema, or test assertion. No fix for the two behavior-changing findings (concurrency key vs. story-slug; clarification halt reaching `plan-approval`) — both are re-parked, and AD-15's slug-keyed concurrency rule is left as written. No edits to `tickets.toml`, the spec, other plans, `change-*/`, or the architecture folder's `reviews/` and `.memlog.md` (historical records). No live dispatch, no push.

</frozen-after-approval>

## Code Map

- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- the bulk of the work. Stale spots:
  - Frontmatter `updated`; Design Paradigm paragraph (stage list; "never needs to survive a job boundary" is now false for evidence).
  - AD-5: "Job 1's token"; no scopes named for `checks` (`contents: write`), `review` (`contents: write`, `pull-requests: write`), `implementation` (`contents: write` only).
  - AD-10: add the addendum entry 8 owed — `checks` and `review` each always commit their evidence to the run branch (`commit_push_implementation.py --label`), the next job checks that branch out (`checkout_branch.py`); no second mechanism such as artifacts.
  - AD-11, AD-12, AD-13, AD-14 Binds/Rule: Job-N wording. AD-13's first Rule sentence says the PR closes in both cases; at cap it is labeled and left open.
  - AD-15: "clarification halt (below cap or at it) each close their own run's PR" (only below cap closes); "Job 3", "Job-1 window".
  - AD-16: "fourth, trailing job after Job 3", "`needs:` all three pipeline jobs" (it needs `analysis`, `implementation`, `merge`), Job 2/3. Worth stating: a `checks` or `review` failure leaves `merge` skipped, so the job does not run.
  - Consistency Conventions rows: bounded loops (Job 1/2), PR/comment target ("clarification cap-out … closes that PR"), clarification rounds ("Each PR closed").
  - Structural Seed diagram: `Job1_Analysis`/`Job2_Implementation`/`Job3_Merge` states and labels; the Job 2 composite must become three states (implementation; checks; review and fix loop, which posts the summary); `ClarificationCapped`/`PostSummaryCapB` say "closes PR"/"PR closed".
  - File tree: workflow comment lists "intake" as a job; `checkout_branch.py` ("entry 3"), `commit_push_implementation.py` (now also the evidence commit), `run_checks.py` (lint is real), `open_implementation_pr.py` (Job 1/2).
  - Capability → Architecture Map rows CAP-1, 2, 4–7, 9; Deferred's last bullet ("Job 3").
- `.claude/skills/light-factory-analysis/SKILL.md` lines 3, 10; `light-factory-implementation/SKILL.md` lines 3, 10, 20; `light-factory-review/SKILL.md` lines 3, 10 -- "Job 1"/"Job 2" in the frontmatter `description` and the opening paragraph. Reword to stage names; nothing else in these files changes.
- `.github/workflows/light-factory.yml` -- comments and one step name only: header (lines 3–9) still says "skeleton … stub steps only"; the checks comment (178–182) says lint has no tool; step name "Lint check (placeholder)" (195). The concurrency comment (19–23) is accurate — keep.
- `factory/` docstrings/comments: `scripts/post_summary.py:10` (names `implementation_graph.py` as the evidence caller; it is `post_evidence_summary.py`), `graph/analysis_graph.py:96` and `scripts/open_implementation_pr.py:14` ("entry 4 … re-call" — no in-run loop exists), `scripts/checkout_branch.py:12,60` ("entry 3"), `graph/fix_loop_graph.py:12` (lint called a placeholder).
- `_bmad-output/initiative-light-factory/deferred-work.md` -- last three entries (source plans: tickets 4 and 5). Line formats in use: `resolved: <date> — …`, `re-deferred: <date> — …`.
- `_bmad-output/initiative-light-factory/epic-pipeline-open-issues/epic-pipeline-open-issues.md` Notes -- disposition note; model: `epic-light-factory-pipeline.md` line 57–62.
- Findings inventory: entry 1 — none deferred. Entry 2 — none (its accumulation limitation was closed by entry 4). Entry 4 — #2 concurrency key (defer). Entry 5 — #2 gate reached after clarification halt (defer), conventions-row drift (parked). Entry 8 — Job-N wording in architecture/`SKILL.md`, AD-10 addendum.

## Tasks & Acceptance

**Execution:**
- [x] `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- correct every spot listed in the Code Map; add the AD-10 addendum -- the spine must describe the six-job pipeline as built
- [x] `.claude/skills/light-factory-{analysis,implementation,review}/SKILL.md` -- replace Job-N wording with stage names -- entry 8's deferred half
- [x] `.github/workflows/light-factory.yml` -- rewrite the header comment and the checks comment, rename the lint step to "Lint check" -- comments contradict the file
- [x] `factory/` files listed in the Code Map -- reword the stale docstring/comment lines only
- [x] `_bmad-output/initiative-light-factory/deferred-work.md` -- `resolved:` on the conventions-row entry; `re-deferred:` on the concurrency-key and gate-after-clarification entries, each saying it needs a behavior change outside a no-new-behavior sweep
- [x] `_bmad-output/initiative-light-factory/epic-pipeline-open-issues/epic-pipeline-open-issues.md` -- append one dated Notes entry listing each finding's disposition, and naming what entry 7 still has to prove live (entries 4, 5, 8) including that a clarification-halted run will pause at `plan-approval`

**Acceptance Criteria:**
- Given the repository after the change, when `grep -nE "Job ?[1-4]\b|Job[1-4]_"` runs over the architecture spine, the three `SKILL.md` files, the workflow and `factory/`, then it returns nothing.
- Given `git diff 05630a5 -- factory/ .github/`, when read, then every changed line is a comment, a docstring, or the one step `name:`.
- Given the architecture spine, when its clarification text is read anywhere (AD-13, AD-15, conventions, diagram), then an at-cap PR is labeled and left open and only a below-cap PR closes.
- Given the Structural Seed diagram, when rendered as Mermaid, then it parses and shows six jobs with the two gates before `implementation` and `merge`.
- Given `deferred-work.md` and the epic Notes, when read, then each finding in the Code Map inventory has a dated disposition.

## Implementation Notes

- 2026-10-11: implemented inline in the planning session, no subagent (user's call). All six tasks done as planned.
- Architecture diagram: the old Job 2 composite became three composites (`ImplementationJob`, `ChecksJob`, `ReviewJob`); state ids `Job1_Analysis`/`Job3_Merge` became `AnalysisJob`/`MergeJob`. The fix-loop edge now returns to the review agent rather than to a checks state, since `fix_loop_graph.py` re-runs build/test itself inside the `review` job.
- AD-13 and the diagram still say a clarification halt ends the run "without reaching a gate". The code does reach `plan-approval`; that is the re-parked entry-5 finding, so the text was left stating the intended behavior, same treatment as AD-15's concurrency key.
- Beyond the Code Map's list: AD-12's Prevents also named a "clarification cap-out" as closing the PR and was corrected with the others.
- Verification ran 2026-10-11: `pytest factory/` 223 passed; `ruff check factory/` clean; workflow parses with the same six job ids; the Job-N grep returns nothing; every changed line under `factory/` and `.github/` is a comment, a docstring, or the lint step's `name:`; the Structural Seed diagram renders with `mmdc`.

## Plan Change Log

## Review Triage Log

Pass 1 (quick lens, 2026-10-11) — run inline by the implementing session against the staged diff, not by an independent context-free reviewer (user's call: no subagents). high 0, medium 0, low 1, false 0, maybe-false 0.

| # | Finding | Verdict | Route | Evidence |
|---|---------|---------|-------|----------|
| 1 | `factory/scripts/checkout_branch.py` module docstring: the reworded line ran to about 97 characters against the file's wrap near 88 | low | patch | Real, cosmetic (ruff does not flag it); paragraph rewrapped. |

## Design Notes

Why the two behavior findings are re-parked rather than fixed: the ticket is "no new behavior", and epic 1's sweep re-parked exactly this class ("genuine new control flow, not cleanup"). The concurrency fix needs either path validation in `derive_story_slug` or a different key; the gate fix needs a new job output and an `if:` on `implementation` that every downstream `needs:` chain then inherits. Both deserve their own ticket and tests.

AD-15's Rule keeps saying the group is keyed on the story-slug although the workflow keys on the raw `story_file` input: that mismatch *is* the re-parked finding, so the Rule is not rewritten to bless the current code.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/ -q` -- expected: 223 passed (unchanged from baseline)
- `uv run --with ruff ruff check factory/` -- expected: All checks passed!
- `uv run --with pyyaml python -c "import yaml; d=yaml.safe_load(open('.github/workflows/light-factory.yml')); print(list(d['jobs']))"` -- expected: the same six job ids
- `grep -rnE "Job ?[1-4]\b|Job[1-4]_" _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md .claude/skills .github factory` -- expected: no output

**Manual checks (if no CLI):**
- `git diff --stat` touches only the files named in Tasks.

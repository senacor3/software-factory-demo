---
title: 'Rename light-factory to software-factory'
type: 'refactor'
ticket: '6'
created: '2026-10-13'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '0b5a31f8fff4a30408b597f15c433ac37dda1950'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The pipeline's own identity -- its workflow file and display name, its git branch/bot/PR-title formula, its three invoked skills, and its docs -- still say "light-factory" even though the project's GitHub remote is already `senacor3/software-factory-demo`.

**Approach:** Mechanically substitute "light-factory" → "software-factory" everywhere it names the pipeline's own identity (workflow file/name/concurrency group, the branch/bot/PR-title formula repeated across six scripts, the three invoked skills, the story-project allow-list, and docs), leaving historical records and the demo app's own identity untouched.

## Boundaries & Constraints

**Always:**
- Every stage that computes the branch name, bot git identity, or PR-title prefix agrees with every other stage -- change all six scripts that repeat the formula together, atomically.
- Tests that currently assert the old strings are updated to assert the new ones, so they keep proving real behavior rather than being weakened or deleted.
- Rename the workflow file itself (`.github/workflows/light-factory.yml` → `.github/workflows/software-factory.yml`) and the three skill directories (`.claude/skills/light-factory-{analysis,implementation,review}/` → `software-factory-{analysis,implementation,review}/`).
- `STORY_PROJECTS` in `state_io.py` drops `"light-factory"` entirely -- only `"software-factory"` and `"freight-tenders"` validate going forward (decided 2026-10-13); a dispatch against `stories/light-factory/...` is rejected after this change.

**Never:**
- Do not touch `_bmad-output/initiative-light-factory/`, any `.factory/<run>/` evidence folder, or the story files already filed under `stories/light-factory/` -- they describe a past state (including mentions of the old workflow filename/branch formula) and stay exactly as written.
- Do not rename the `checks`/`checks-fix-loop` jobs' `name:` fields, their `--label` evidence-commit arguments, or the `checks-toolchain` composite action's own name -- that rename is split into backlog ticket 7 (`story-rename-checks-job-to-quality-assurance.md`); leave every other line of `.github/workflows/light-factory.yml`'s `checks`/`checks-fix-loop` jobs untouched.
- Do not touch the `checks`/`checks-fix-loop` YAML job-id keys, their `needs:`/`if:` wiring, the `checks_fix_loop_graph.py` module's internals, the five check types, or `run_checks.py`'s subcommand vocabulary.
- Do not touch the freight-tenders demo app's own name or identity.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Dispatch under the old story path | `stories/light-factory/<slug>.md`, after this change | Rejected by `state_io.py`'s path validation (`STORY_PROJECTS` no longer includes it) | Same error path as any invalid project, naming only the current valid projects |
| Dispatch under the new story path | `stories/software-factory/<slug>.md` | Accepted | No error expected |
| A run's branch, commit author, PR title | any story dispatched after this change | All three read "software-factory" consistently from open through merge | N/A |
| A run opened before this change merges | branch `light-factory/<slug>/<run-id>` already pushed, mid-flight | Out of scope -- not special-cased; merge this change only when no run is in-flight | N/A |

</frozen-after-approval>

## Code Map

- `.github/workflows/light-factory.yml` → rename to `.github/workflows/software-factory.yml` -- `name:` (L1), header comment (L3), concurrency group `light-factory-${{...}}` (L29), dispatch-input description's project example (L18); leave the AD-n comment pointing at `_bmad-output/initiative-light-factory/architecture-light-factory/...` (L11-12) untouched -- historical doc path; leave every `checks`/`checks-fix-loop` job line untouched (ticket 7)
- `.github/workflows/freight-tenders.yml` L3 -- comment naming light-factory
- `.github/post-implementation-checks.yml` L1 -- header comment naming light-factory (comment-only; this file is read from `origin/main` so the edit needs merging to take effect, but there's no behavior to verify)
- `factory/scripts/checkout_branch.py`, `commit_push_implementation.py` (docstring/help text L18/20/67/103, bot identity L80/82, branch formula L107 -- NOT the `--label` default itself, that's ticket 7), `merge_story.py`, `close_rejected_pr.py`, `post_evidence_summary.py`, `open_implementation_pr.py` (branch prefix/own_branch, bot identity, PR-title prefix `f"light-factory: {story_slug} ({run_id})"`) -- the repeated `light-factory/<story_slug>/<run_id>` branch formula and `light-factory-bot`/`light-factory-bot@users.noreply.github.com` identity, each in its own docstring and code
- `factory/scripts/state_io.py` L5 (docstring), L95 (`STORY_PROJECTS = ("light-factory", "freight-tenders")` → `("software-factory", "freight-tenders")`), L102/132/138/140 (its uses)
- `.claude/skills/light-factory-analysis/`, `light-factory-implementation/`, `light-factory-review/` → rename dirs to `software-factory-{analysis,implementation,review}/`; each `SKILL.md`'s `name:` frontmatter (L2), heading (L6), body invocation line (L10)
- `factory/graph/analysis_graph.py` (L8 docstring, L119 invocation), `implementation_graph.py` (L13 docstring, L77 invocation), `review_graph.py` (L8 docstring, L64 invocation), `fix_loop_graph.py` (L10 docstring mention) -- match the renamed skills
- `factory/graph/schemas/analysis_result.schema.json` L4, `review_result.schema.json` L4 -- `description` field naming the skill
- `AGENTS.md` L4/L15, `freight-tenders/README.md` L12/15/16, `freight-tenders/backend/AGENTS.md` L6, `freight-tenders/frontend/AGENTS.md` L6, `_bmad/config.toml` L2 (`project_name`), `.gitignore` L14-15 (comment only; the ignore glob itself, `.claude/skills/bmad*`/`bmod*`, is unaffected) -- leave `README.md` L9's historical path reference untouched
- 12 test files mirroring the source changes above: `factory/graph/tests/{test_analysis_graph,test_checks_fix_loop_graph,test_fix_loop_graph,test_implementation_graph,test_review_graph}.py`, `factory/scripts/tests/{test_checkout_branch,test_close_rejected_pr,test_commit_push_implementation,test_merge_story,test_open_implementation_pr,test_state_io,test_post_evidence_summary}.py` -- update branch/skill-invocation/bot-identity fixtures and `STORY_PROJECTS`-driven path fixtures only; leave each file's `label="Checks"`/`"Checks: ..."` assertions alone (ticket 7)
- `factory/scripts/tests/test_workflow_checks_setup.py` L22 -- `WORKFLOW` path constant must follow the workflow file's rename, or every test in this file breaks (it parses the file by that literal path)

## Tasks & Acceptance

**Execution:**
- [x] `.github/workflows/light-factory.yml` -- rename the file and update the workflow's own identity (name, header comment, concurrency group, dispatch-input description) -- leave every checks/checks-fix-loop job line untouched
- [x] `.github/workflows/freight-tenders.yml`, `.github/post-implementation-checks.yml` -- update the two comment lines -- consistency, no functional effect
- [x] `factory/scripts/{checkout_branch,commit_push_implementation,merge_story,close_rejected_pr,post_evidence_summary,open_implementation_pr}.py` -- replace the shared branch-formula and bot-identity strings and docstrings together -- these six must agree or a run's branch name and PR lookup diverge mid-pipeline
- [x] `factory/scripts/state_io.py` -- drop `"light-factory"` from `STORY_PROJECTS`, replace with `"software-factory"`, and update its docstring
- [x] `.claude/skills/light-factory-{analysis,implementation,review}/` -- rename the three directories and update each `SKILL.md`
- [x] `factory/graph/{analysis_graph,implementation_graph,review_graph,fix_loop_graph}.py`, `factory/graph/schemas/{analysis_result,review_result}.schema.json` -- update the matching skill-invocation strings/descriptions
- [x] `AGENTS.md`, `freight-tenders/README.md`, `freight-tenders/backend/AGENTS.md`, `freight-tenders/frontend/AGENTS.md`, `_bmad/config.toml`, `.gitignore` -- update the remaining project-identity mentions (leave `README.md`'s historical path reference alone)
- [x] `factory/scripts/tests/test_workflow_checks_setup.py` -- update the `WORKFLOW` path constant to match the renamed file
- [x] The 12 listed test files -- update every branch/skill-invocation/bot-identity/`STORY_PROJECTS` fixture and assertion to match the source changes above, so the suite proves the renamed behavior rather than being weakened; leave `label="Checks"`-related assertions alone (ticket 7)

**Acceptance Criteria:**
- Given a repo-wide search for "light-factory" excluding `_bmad-output/initiative-light-factory/`, any `.factory/<run>/` evidence folder, and the story files under `stories/light-factory/`, when run after implementation, then it returns nothing
- Given the full test suite, when run after implementation, then it passes
- Given `ruff check factory/`, when run after implementation, then it reports no findings

## Implementation Notes

- 2026-10-13: implemented as specified. The workflow file and three skill directories were renamed via `git mv`; the branch/bot-identity/PR-title formula was replaced identically across all six scripts (`checkout_branch.py`, `commit_push_implementation.py`, `merge_story.py`, `close_rejected_pr.py`, `post_evidence_summary.py`, `open_implementation_pr.py`); `STORY_PROJECTS` now reads `("software-factory", "freight-tenders")`. All 12 listed test files and `test_workflow_checks_setup.py` were updated via literal-string substitution for every `light-factory` occurrence found in them (all were in-scope fixtures/assertions, verified individually before the bulk replace). Verified: `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- 390 passed; `uv run --with ruff ruff check factory/` -- no findings; the plan's own manual-check grep (excluding `_bmad-output`, `.factory`, `.git`, and `stories/light-factory/`) returns only the two intentionally preserved historical references (root `README.md` L9 and the workflow's AD-n doc-path comment). Note: a broader repo-wide grep for "light-factory" (not scoped the way the plan's manual check is) still finds it in several `_bmad-output/backlog/*.md` and `_bmad-output/initiative-demo-app/*.md` files -- these are other tickets' planning docs/narrative references to the old name, not listed in this plan's Code Map, and were left untouched as out of scope.
- 2026-10-13, Matrix Test Audit (orchestrating session, post-implementation): the "branch, commit author, PR title" row had no covering test for the PR-title sub-behavior -- `test_fresh_create_creates_branch_commits_pushes_and_opens_pr` in `test_open_implementation_pr.py` only asserted `gh pr create` was called once, never inspecting its `--title` argument (a pre-existing gap, not introduced by this change). Fixed by adding two assertions there confirming `--title` is present and equals `"software-factory: foo (run-1)"`. Re-ran full suite after the fix: 390 passed; `ruff check factory/` still clean. The "dispatch under the old story path is rejected" row is covered generically -- `test_derive_story_slug_rejects_wrong_location`'s `"stories/billing/foo.md"` case already exercises the same `not in STORY_PROJECTS` branch that now also excludes `light-factory`; the code has no name-specific branching, so no dedicated `light-factory` test case is needed.

- 2026-10-13, patch from Quick review: `analysis_result.schema.json`/`review_result.schema.json`'s `title` fields renamed `LightFactoryAnalysisResult`/`LightFactoryReviewResult` → `SoftwareFactoryAnalysisResult`/`SoftwareFactoryReviewResult`. Re-verified after the patch: full suite 390 passed, `ruff check factory/` clean.

## Plan Change Log

- 2026-10-13: split off the `checks`/`checks-fix-loop` job rename ("Checks" → "Quality Assurance") into backlog ticket 7 (`story-rename-checks-job-to-quality-assurance.md`) -- the bundled plan was ~2800 tokens, well over the 1600-token ceiling; the two renames don't share any line of code, so narrowing to just the light-factory → software-factory rename brought it back into range. KEEP: everything else from the original draft (branch-formula/bot-identity atomicity, skill-dir renames, `STORY_PROJECTS` drop-entirely decision, historical-artifact boundaries).

## Review Triage Log

- **Quick, 2026-10-13** — Acceptance criterion 1's literal grep still finds `light-factory` at `README.md:9` and `.github/workflows/software-factory.yml:11-12`. Verdict: **false** (as a code defect). The AC's wording doesn't carve out these two historical-reference lines, but the plan's own frozen Boundaries and Code Map explicitly instruct leaving them untouched, and the implementation matches that more specific instruction exactly; the narrower "Manual checks" grep command (which excludes all of `_bmad-output`) already passes cleanly. The only fix available is editing the AC's wording in the plan itself — auto-rejected per the rule against findings whose fix is to edit the plan.
- **Quick, 2026-10-13** — `factory/graph/schemas/analysis_result.schema.json:3` and `review_result.schema.json:3` still read `"title": "LightFactoryAnalysisResult"` / `"LightFactoryReviewResult"` (PascalCase, no hyphen) — missed because the Code Map only named the `description` field for these two files, and no grep or test catches this casing variant. Verdict: **low** (cosmetic; a JSON Schema `title` has no effect on validation and nothing reads it in code or tests) — confirmed via `grep -rni "lightfactory"` finding only these two lines repo-wide, outside `_bmad-output`/`.factory`. Route: **patch** (direct one-line string correction in each file, no public surface, no new state).

## Design Notes

The six branch-formula scripts (`checkout_branch.py`, `commit_push_implementation.py`, `merge_story.py`, `close_rejected_pr.py`, `post_evidence_summary.py`, `open_implementation_pr.py`) all independently format or match `f"light-factory/{story_slug}/{run_id}"` -- there is no shared constant. Change the literal in all six in the same pass; a partial rename would make one stage open a branch another stage can't find.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass
- `uv run --with ruff ruff check factory/` -- expected: no findings

**Manual checks (if no CLI):**
- `grep -rn "light-factory" --exclude-dir=_bmad-output --exclude-dir=.factory --exclude-dir=.git . | grep -v "stories/light-factory/"` -- expected: empty
- Merge this change only when no software-factory pipeline run is in-flight -- an in-flight run's branch was opened under the old formula

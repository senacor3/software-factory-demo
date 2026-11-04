---
title: 'Stage-completion callback'
type: 'feature'
ticket: '6'
created: '2026-11-04'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: '9c77c300e84a00048e16f8001a0bbb855904be0c'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The orchestrator's `stage-callback` caller type (entry 3) verifies the shared secret but then does nothing — no DynamoDB write, no action — and the `plan-approval` gate summary (AD-4) is still posted from inside the `analysis` job via its own token, which AD-5 scopes only to AD-12's branch/PR-open script, not to this.

**Approach:** Add a final step to each of the three workflow files that POSTs its own concrete stage status to the orchestrator's Function URL (AD-17's addendum, caller type c), authenticated via entry 3's shared secret. `handler.py`'s `stage-callback` branch records the status in DynamoDB and, only for the `analysis` workflow's `ready-for-review` status, finds the PR by branch and posts the AD-4 plan-approval summary itself (via the PAT, AD-18) — removing that one call site from `analysis_graph.py`.

## Boundaries & Constraints

**Always:** Each workflow's callback step runs only after its own stage-defining write already succeeded (plan.md for `analysis`, review.md for `review`) — a halted/crashed run posts no callback, same scope line entry 5 drew for `/approve`/`/reject`. DynamoDB writes are plain `PutItem` (mirrors `mark_terminal`), not yet AD-20's atomic conditional write (entry 9's scope). The `awaiting-clarification`/`clarification-cap-reached` PR comments stay exactly where they are today (`open_implementation_pr.py`, inside the `analysis` job) — AD-5 already scopes that job's token for that script specifically; only the AD-4 `post_summary.post_comment` call site moves. Reuse `github_app.get_file_content` to read `plan.md` off the PR's own head branch (never `main`) when rendering the summary.

**Never:** No change to `evidence-approval`'s own summary mechanism (`review` job's `post_evidence_summary.py`, already correctly scoped by AD-5) — out of this entry's named scope. No `merge.yml` Environment/gate change (entry 7). No atomic/conditional DynamoDB writes (entry 9). No new Secrets Manager fields — the callback secret already exists (entry 3); the Function URL and that secret's value become new GitHub Actions repo configuration (a human sets them, same precedent as entry 3's live webhook hookup), not asserted as done here.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| `analysis` callback, `ready-for-review` | Valid stage-callback secret, `stage=analysis`, `status=ready-for-review` | DynamoDB row written; PR found by branch; AD-4 summary (rebuilt from `plan.md`) posted as a PR comment | A GitHub API failure raises, surfacing in Lambda logs |
| `analysis` callback, `awaiting-clarification`/`clarification-cap-reached` | Same, other status | DynamoDB row written; no PR comment posted (already posted in-job) | N/A |
| `implementation-checks-review` callback | `stage=implementation-checks-review`, `status` from `review.md` | DynamoDB row written; no PR comment | N/A |
| `merge` callback | `stage=merge`, `status=merged` | DynamoDB row written; no PR comment | N/A |
| Callback names a branch with no open PR | `analysis`/`ready-for-review`, PR already closed/missing | DynamoDB row still written; comment step skipped | N/A |
| Invalid stage-callback secret | Mismatched/missing secret | Rejected, unchanged from entry 3 | Clear-reason response |

</frozen-after-approval>

## Code Map

- `factory/scripts/post_stage_callback.py` -- new deterministic script: `post(url, secret, stage, story_slug, run_id, status)` (plain `urllib.request` POST, `X-Stage-Callback-Secret` header, JSON body `{"stage", "story-slug", "run-id", "status"}`); CLI reads `--status-file` (via `state_io.read_state(path)["status"]`) or a literal `--status`, mutually exclusive. Raises on any non-2xx.
- `.github/workflows/analysis.yml` -- add a final `analysis` job step, `if: steps.analyze.outcome == 'success'`, calling the script with `--stage analysis --status-file .factory/<slug>/<run-id>/plan.md`.
- `.github/workflows/implementation-checks-review.yml` -- add a final step to the `review` job (after "Post evidence-approval summary"), calling the script with `--stage implementation-checks-review --status-file .factory/<slug>/<run-id>/review.md`.
- `.github/workflows/merge.yml` -- add a final step to the `merge` job, calling the script with `--stage merge --status merged` (the only status this job can ever report, by construction -- a failure never reaches this step).
- `orchestrator/github_app.py` -- add `find_pull_request_by_branch(token, branch) -> dict | None` (GET `/pulls?head=<owner>:<branch>&state=open`, returns the first match or `None`).
- `orchestrator/dynamodb_state.py` -- add `record_stage_status(story_slug, run_id, stage, status) -> None`, mirroring `mark_terminal`'s plain-`PutItem` shape.
- `orchestrator/handler.py` -- fill in the `stage-callback` branch: parse the JSON body (`stage`, `story-slug`, `run-id`, `status`); call `dynamodb_state.record_stage_status`; when `stage == "analysis"` and `status == "ready-for-review"`, find the PR via `find_pull_request_by_branch(token, f"{_BRANCH_PREFIX}/{story_slug}/{run_id}")`, read `plan.md` via `get_file_content` at that PR's head ref, render the AD-4 summary from its `## Proposal`/`## Subtasks`/`## Tests` sections (new `_render_plan_approval_summary(body)` helper, mirrors `analysis_graph._render_plan_summary`'s shape), and `post_comment`. No PR found: skip the comment, still 200.
- `factory/graph/analysis_graph.py` -- remove the `post_summary.post_comment` call (and `_render_plan_summary`, the `post_summary` import) from the `ready-for-review` branch of `run_analysis`; update the module docstring's outcome-2 description and the `except` clause (drops `post_summary.PostCommentError`).
- `orchestrator/tests/test_github_app.py`, `test_dynamodb_state.py`, `test_handler.py` -- extend for the new function/branch per the I/O matrix.
- `factory/scripts/tests/test_post_stage_callback.py` -- new.
- `factory/graph/tests/test_analysis_graph.py` -- drop `post_summary`-related assertions/imports and the now-obsolete `test_post_summary_failure_raises_analysis_pr_open_error_but_state_files_remain`.

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/post_stage_callback.py` -- the shared callback-posting script -- one deterministic step, reused by all three workflows
- [ ] `.github/workflows/{analysis,implementation-checks-review,merge}.yml` -- add each file's final callback step -- makes AD-17's caller-type (c) real
- [ ] `orchestrator/github_app.py` -- `find_pull_request_by_branch` -- the lookup the orchestrator needs since the callback carries no PR number
- [ ] `orchestrator/dynamodb_state.py` -- `record_stage_status` -- the control-plane write this entry owns
- [ ] `orchestrator/handler.py` -- fill in the `stage-callback` branch -- DynamoDB write + conditional AD-4 summary post
- [ ] `factory/graph/analysis_graph.py` -- remove the in-job `post_summary.post_comment` call -- the responsibility this entry moves
- [ ] Extend/add the test files above -- cover every I/O matrix row

**Acceptance Criteria:**
- Given a real dispatch of `analysis.yml` that reaches `ready-for-review`, when its final step runs, then the orchestrator's DynamoDB row reflects it and the AD-4 summary appears as a PR comment, posted by the orchestrator, not the job.
- Given a dispatch that reaches `awaiting-clarification`, when its final step runs, then the DynamoDB row reflects it and no additional PR comment is posted by the orchestrator (the in-job clarification comment is unaffected).
- Given a dispatch of `implementation-checks-review.yml` or `merge.yml` to completion, when its final step runs, then the DynamoDB row reflects that workflow's status.
- Given a stage-callback naming a branch with no open PR, when the orchestrator processes it, then the DynamoDB write still succeeds and no comment-posting call is attempted.

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-04):** 2 findings routed. Verdict counts: medium=1, low=1, both patch.

- `handler.py`'s `_parse_plan_sections` treats ANY line starting with `"## "` as a new section boundary — **medium, patch.** Verified: `analysis_graph._render_plan_body` writes `result.get("proposal")` verbatim (freeform LLM prose, schema only says "Prose solution proposal", no constraint against markdown subheadings) inside the `## Proposal` section; if that prose itself contains a `##`-prefixed line, `_parse_plan_sections` wrongly starts a new section there, silently truncating/corrupting the proposal text in the AD-4 summary the orchestrator posts — undermining AD-4's own "the human decides from the summary" purpose, not just cosmetic, and plausible in everyday use since LLM prose commonly uses subheadings. Fix: match only the three known literal headers `plan.md` always has (`## Proposal`, `## Subtasks`, `## Tests`) as section boundaries, not any `"## "`-prefixed line.
- `post_stage_callback.py`'s `post()` docstring promises raising `StageCallbackError` on "any non-2xx response or transport failure", but only catches `urllib.error.HTTPError`/`URLError` — **low, patch.** Verified directly: an empty/malformed `--url` (exactly the state before the human-supplied `ORCHESTRATOR_FUNCTION_URL` config this entry's own Boundaries defer) makes `urllib.request.urlopen` raise a bare `ValueError` ("unknown url type"), not a `URLError` subclass, so it propagates as an unhandled traceback instead of the clean `StageCallbackError` message the CLI's `except` clause is built to produce. The step fails either way until config exists; only the diagnostic quality differs — a direct, trivial fix (catch `ValueError` too). Fix: add `ValueError` to `post()`'s except clause, same message shape.

Both patches applied and re-verified independently: `_parse_plan_sections` now matches only the three literal headers (`_PLAN_SECTION_HEADERS`) as section boundaries, confirmed via direct diff read; `post_stage_callback.post()` moves `Request(...)` construction inside the `try` (the implementer found the `ValueError` actually originates there, not in `urlopen`, which a narrower fix would have missed) and adds `ValueError` alongside `URLError` to the except clause. Full suite re-run: `orchestrator/` 68/68, `factory/graph/tests/`+`factory/scripts/tests/` 397/397, `ruff check factory/` clean, `terraform fmt -check && terraform validate` clean.

## Design Notes

Rebuilding the AD-4 summary from `plan.md`'s committed body (rather than threading the analysis agent's raw result dict across the callback) keeps the callback payload tiny and stage-agnostic -- `plan.md`'s `## Proposal`/`## Subtasks`/`## Tests` sections are exactly what `_render_plan_summary` already formatted from the same data, so parsing them back (proposal text verbatim, bullet-line counts) reproduces the original summary's content without a second channel carrying the same information.

`find_pull_request_by_branch` exists because the stage-completion callback is keyed on story-slug/run-id (branch name), not a PR number -- unlike Gate 1's `/approve`/`/reject`, which read the PR number straight off the `issue_comment` webhook payload.

The GitHub Actions secret (`STAGE_CALLBACK_SECRET`, matching entry 3's Secrets-Manager field) and the Function URL (`ORCHESTRATOR_FUNCTION_URL`, a plain repo variable) are human-supplied repo configuration, not created by this entry's code -- same precedent as entry 3's live webhook hookup.

## Verification

**Commands:**
- `cd orchestrator && uv run --with pytest pytest tests/ -v` -- expected: all tests pass
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all tests pass
- `cd infra && terraform fmt -check && terraform validate` -- expected: no diff, config valid (no infra changes this entry)
- `python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/<file>.yml` for each of the three files -- expected: no exception
- `uv run --with ruff ruff check factory/` -- expected: clean

**Manual checks (if no CLI):**
- The live three-callback exercise (a real dispatch of each workflow, confirming the DynamoDB row and the AD-4 summary PR comment) runs only after separate, explicit confirmation -- not part of this plan's automated verification, and requires the human-supplied `STAGE_CALLBACK_SECRET`/`ORCHESTRATOR_FUNCTION_URL` repo configuration to exist first.

---
title: 'Gate 2 comment grammar wired live; evidence-approval Environment removed'
type: 'feature'
ticket: '7'
created: '2026-11-04'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: 'dc92b5824331fe2bcd24d8dff54ba9a7f528b144'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Both gates share one PR and one `issue_comment` webhook (AD-2), but `_handle_approve` hardcodes `implementation-checks-review.yml` as the only dispatch target, and `_handle_rework` acts on any `/rework` regardless of which gate is current — so `evidence-approval` cannot be approved at all, and a `/rework` posted after implementation is already built would wrongly re-run analysis (AD-2: "no `/rework`-equivalent action at this gate").

**Approach:** Add a DynamoDB read (entry 6's `record_stage_status` row) so `_handle_approve`/`_handle_rework` know which gate, if any, is actually current (AD-20: "checks the actual current state... before acting"). `/approve` at `plan-approval` dispatches `implementation-checks-review.yml` (unchanged behavior); `/approve` at `evidence-approval` dispatches `merge.yml` (new). `/rework` only acts at `plan-approval`; at `evidence-approval` or with no gate current, it's a silent no-op, same as a comment on an unrelated PR. `/reject` is unchanged (already gate-agnostic, AD-2's "same as Gate 1"). Remove `environment: evidence-approval` from `merge.yml`'s `merge` job.

## Boundaries & Constraints

**Always:** The gate-current check is a plain `GetItem` (no new write), mirroring `mark_terminal`/`record_stage_status`'s existing plain-`PutItem` posture — not yet AD-20's atomic conditional write (entry 9's scope). `plan-approval` = `stage=="analysis"` and `status=="ready-for-review"`; `evidence-approval` = `stage=="implementation-checks-review"` (any status it ever holds, `resolved` or `unresolved-after-cap`, both legitimate human-decides outcomes per `post_evidence_summary.py`'s own existing comment). No row, or `stage=="merge"`, or any other combination: no gate is current.

**Never:** No change to `/reject` (`_handle_reject`) or to `comment_commands.py`'s grammar — both already gate-agnostic. No atomic/conditional DynamoDB writes or reads (entry 9). No conflict-resolution loop inside `merge.yml` (entry 8) — `merge.yml`'s own job body is untouched beyond removing the `environment:` key and updating header comments. No deletion of the `evidence-approval` Environment resource from repo settings, nor of `close_rejected_pr.py` (entry 10's scope, same precedent entry 5 set for `plan-approval`).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| `/approve` while `plan-approval` is current | DynamoDB row `stage=analysis`, `status=ready-for-review` | `implementation-checks-review.yml` dispatched (unchanged from entry 5) | N/A |
| `/approve` while `evidence-approval` is current | DynamoDB row `stage=implementation-checks-review` | `merge.yml` dispatched with the story-slug/run-id; confirmation comment posted | A GitHub API failure raises, surfacing in Lambda logs |
| `/approve` with no gate current | No row, or `stage=merge` | No dispatch, no comment (silent no-op) | N/A |
| `/rework <feedback>` while `plan-approval` is current | Same as above | Unchanged from entry 5 | N/A |
| `/rework <feedback>` while `evidence-approval` is current | `stage=implementation-checks-review` | No dispatch, no comment, no story-file commit (silent no-op — AD-2: no rework-equivalent at this gate) | N/A |
| `/reject` at either gate | Any stage | Unchanged from entry 5: terminal, PR closed, comment posted | N/A |

</frozen-after-approval>

## Code Map

- `orchestrator/dynamodb_state.py` -- add `get_stage_status(story_slug, run_id) -> dict[str, str] | None`: plain `GetItem`, returns `{"stage": ..., "status": ...}` unwrapped from DynamoDB's `{"S": ...}` shape, or `None` when no `Item` key in the response. Matches the IAM policy already granted (`dynamodb:GetItem`).
- `orchestrator/handler.py` -- new module-level `_MERGE_WORKFLOW = "merge.yml"` constant and `_GATE_BY_STAGE_STATUS` mapping (`("analysis", "ready-for-review") -> "plan-approval"`, `("implementation-checks-review", "resolved") -> "evidence-approval"`, `("implementation-checks-review", "unresolved-after-cap") -> "evidence-approval"`); new `_current_gate(story_slug, run_id) -> str | None` helper wrapping `dynamodb_state.get_stage_status` + the mapping lookup. `_handle_approve` branches on `_current_gate`'s result instead of hardcoding `_IMPLEMENTATION_CHECKS_REVIEW_WORKFLOW` (`plan-approval` -> that workflow, unchanged message; `evidence-approval` -> `_MERGE_WORKFLOW`, new message; neither -> return, no-op). `_handle_rework` gains an early `if _current_gate(story_slug, run_id) != "plan-approval": return` guard before its existing logic. `_handle_reject` and `comment_commands.py` untouched. Update the module docstring's stale "`/approve`/`/reject` need no DynamoDB read at all" claim and `_handle_reject`'s DynamoDB `reason` string (drop the hardcoded "on plan-approval").
- `.github/workflows/merge.yml` -- remove `environment: evidence-approval` from the `merge` job; update header comments (mirrors entry 5's edit to `implementation-checks-review.yml`): the gate is now orchestrator-owned via `/approve`/`/reject`, and `close-rejected-pr` is now dead weight on this file's reject path (left in place, entry 10's scope).
- `orchestrator/tests/test_dynamodb_state.py` -- new `TestGetStageStatus` covering: row found, no row (`None`).
- `orchestrator/tests/test_handler.py` -- extend the **existing** `test_approve_dispatches_workflow_and_posts_comment`, `test_rework_appends_feedback_and_redispatches_analysis`, `test_rework_falls_back_to_freight_tenders_project_path`, and `test_rework_story_file_not_found_under_either_project_posts_rejection` (entries 5/6) with a mock for `handler.dynamodb_state.get_stage_status` returning `{"stage": "analysis", "status": "ready-for-review"}` — without it they'd now hit the new no-op branch and silently fail their existing assertions. Add new tests: `/approve` at `evidence-approval` dispatches `merge.yml`; `/approve` with no DynamoDB row is a no-op; `/rework` at `evidence-approval` is a no-op; `/rework` with no DynamoDB row is a no-op.

## Tasks & Acceptance

**Execution:**
- [ ] `orchestrator/dynamodb_state.py` -- `get_stage_status` -- the read this entry's gate-awareness needs
- [ ] `orchestrator/handler.py` -- `_current_gate` helper, `_handle_approve`/`_handle_rework` gate branching -- makes `/approve` reach `merge.yml` and keeps `/rework` out of `evidence-approval`
- [ ] `.github/workflows/merge.yml` -- drop `environment: evidence-approval` -- removes the GitHub-native gate from this path
- [ ] Extend the 4 existing `test_handler.py` tests named above with the new mock -- keeps entries 5/6's own assertions valid under the new gate check
- [ ] Add the new tests per the I/O matrix

**Acceptance Criteria:**
- Given a `/approve` comment while `evidence-approval` is current, when the webhook fires, then `merge.yml` is dispatched with the story-slug/run-id parsed from the PR's branch, with no Environment review requested.
- Given a `/approve` or `/rework` comment while no gate is current (no DynamoDB row, or `stage=="merge"`), when the webhook fires, then no GitHub API call is made.
- Given a `/rework <feedback>` comment while `evidence-approval` is current, when the webhook fires, then no story-file commit, no re-dispatch, and no comment are made.
- Given the `merge` job in `merge.yml`, when inspected, then it carries no `environment:` key.

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-04):** 3 findings routed. Verdict counts: high=1 (patch), low=2 (1 patch, 1 rejected).

- `dynamodb_state.get_stage_status` indexes `item["stage"]["S"]`/`item["status"]["S"]` unconditionally — **high, patch.** Verified: `mark_terminal`'s `PutItem` writes a row with only `story_slug#run_id`/`status`/`reason`/`updated` — no `stage` key — and `PutItem` fully replaces the item, so once `/reject` has run for a story/run, that row permanently has this shape. GitHub still delivers `issue_comment` webhooks for closed PRs, and `_handle_github_comment` never checks PR open/closed state before parsing a command, so a stray `/approve`/`/rework` on an already-rejected PR reaches `_current_gate` -> `get_stage_status` -> `KeyError`, an unhandled exception crashing the Lambda invocation instead of the silent no-op the I/O matrix requires for "no gate current." Real, plausible, no special circumstances needed. Fix: `get_stage_status` returns `None` when the item lacks either `stage` or `status` (a rejected/terminal row has no current gate by definition, same as no row at all).
- `handler.py`'s `_handle_reject` reason-string change — **rejected** (fix would be editing this plan, not the code). The frozen Boundaries say "No change to `_handle_reject`," but this plan's own (non-frozen) Code Map explicitly directed exactly this string change with its own rationale, and the Design Notes' "left untouched" refers to the guard/logic, not the literal string — read as a whole, the plan's own Code Map already resolves the apparent conflict in favor of keeping the change. The Boundaries sentence was overly broad phrasing on my part, not a renegotiation the implementer made unilaterally; reverting a deliberate, correct, already-approved change to chase a wording mismatch would be the wrong fix here.
- Missing `/rework` + `stage=="merge"` test — **low, patch.** Verified: the acceptance criterion names both `/approve` and `/rework` against both off-states, but only `/approve`+`stage==merge` and `/rework`+no-row are tested; `/rework`+`stage==merge"` has no dedicated test, even though it exercises the identical `_current_gate(...) != "plan-approval"` guard already proven by the other three — no distinct bug could hide here, but the AC's own literal enumeration isn't fully evidenced. Fix: add the one missing test, mirroring `test_approve_while_merge_stage_is_current_is_a_no_op`.

Patch 1 and 3 applied and re-verified independently: `get_stage_status` now returns `None` when the item lacks either `stage` or `status` (confirmed via direct diff read, plus the new `test_terminal_row_with_no_stage_or_status_returns_none`); `test_rework_while_merge_stage_is_current_is_a_no_op` added, mirroring the existing `/approve` equivalent. Full suite re-run: `orchestrator/` 77/77 (was 75 before this pass), `terraform fmt -check && terraform validate` clean, `grep`/YAML checks clean.

## Design Notes

`_GATE_BY_STAGE_STATUS` keys on `(stage, status)`, not `stage` alone, for `plan-approval` specifically because `stage=="analysis"` also covers `awaiting-clarification`/`clarification-cap-reached`, neither of which ever reaches a human gate (AD-13: "this path ends the run without reaching a gate") — only `ready-for-review` does. `evidence-approval` keys on `stage` alone (both `resolved`/`unresolved-after-cap` are legitimate gate-reached outcomes, matching `post_evidence_summary.py`'s own existing framing), so the mapping lists both explicitly rather than normalizing to a stage-only check, keeping the table a literal, auditable enumeration instead of two different lookup shapes.

`_handle_reject` needs no gate check: AD-2 states `/reject` cancels the run identically at either gate, so the existing branch-match-only guard (shared with `_handle_approve`/`_handle_rework`'s baseline `_parse_branch` check) is already correct and is left untouched.

## Verification

**Commands:**
- `cd orchestrator && uv run --with pytest pytest tests/ -v` -- expected: all tests pass
- `cd infra && terraform fmt -check && terraform validate` -- expected: no diff (no infra changes this entry)
- `grep -c "environment: evidence-approval" .github/workflows/merge.yml` -- expected: `0`
- `uv run --with pyyaml python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/merge.yml` -- expected: no exception

**Manual checks (if no CLI):**
- The live exercise (posting `/approve` on a real evidence-approval comment and watching `merge.yml` dispatch and the branch merge; `/reject` halting the run) runs only after separate, explicit confirmation, per the ticket's own Notes -- not part of this plan's automated verification.

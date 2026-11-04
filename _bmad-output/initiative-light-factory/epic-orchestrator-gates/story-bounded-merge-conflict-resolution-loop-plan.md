---
title: 'Bounded merge-conflict-resolution loop'
type: 'feature'
ticket: '8'
created: '2026-11-04'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: '11c890d3c5ee15e9b08cbc8bf092d6e16459e48a'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `merge.yml`'s `merge` job just runs `gh pr merge --squash` and fails outright on a real conflict, requiring a human to resolve it out-of-band — CAP-11 has no implementation yet.

**Approach:** Add `detect-conflict` (deterministic git-merge dry-run against `main`) and, only when it finds one, `resolve-conflict` (a branch-scoped Claude Code agent, no git/Bash tool, editing only the conflicted files' content; a deterministic script stages the merge before it runs and commits/pushes after) as new `needs:`-chained jobs before the existing `merge` job (AD-14, unchanged). The attempt counter lives in DynamoDB (AD-19), claimed via a new orchestrator endpoint — never incremented by the agent, never a local/in-job variable, so it survives a job retry. Hard cap 2; cap-out fails the job and surfaces to the developer.

## Boundaries & Constraints

**Always:** Exactly AD-19's permission shape for the new agent: Claude Code `--allowedTools "Read Write Edit Grep Glob"` only (no Bash, no git, no merge/admin tool), scoped to the current checkout (the feature branch), any path in the conflict list (not restricted to a subtask-file list, unlike the implementation agent). "Still conflicted" is decided by scanning the conflicted files' own content for leftover `<<<<<<<`-style marker lines — never by re-running `git merge` (which reports clean the moment a conflict is *staged*, regardless of whether the agent actually removed every marker) and never by the agent's own say-so. The attempt counter is a plain `UpdateItem` (`ADD`), not yet AD-20's atomic conditional write (entry 9's scope) — same deferred-atomicity posture as entries 5-7's DynamoDB writes. `detect-conflict`'s own merge attempt is always aborted afterward (it is a pure probe, never left in progress) — only `resolve-conflict`'s own merge attempt is deliberately left staged for the agent.

**Never:** No change to the existing `merge` job's own logic (`merge_story.py`, AD-14) beyond its `needs:`/`if:` condition. No atomic/conditional DynamoDB writes (entry 9). No real conflict-resolution verification beyond marker-scanning in automated tests — the ticket's own Notes name a human reviewing the agent's first real resolution diff before trusting it unattended; that live exercise is explicitly deferred, not part of this plan's automated verification.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| No conflict | Feature branch merges cleanly against `main` | `detect-conflict` finds none; `resolve-conflict` skipped entirely; `merge` runs as today | N/A |
| Conflict, resolved on attempt 1 | `detect-conflict` finds one | `resolve-conflict` claims attempt 1, agent edits, no markers remain, commit+push; `merge` then runs | N/A |
| Conflict, resolved on attempt 2 | Attempt 1's edit leaves markers | Loop claims attempt 2 (same merge, agent re-invoked), resolves, commit+push; `merge` then runs | N/A |
| Conflict, still unresolved after attempt 2 | Attempt 2's edit still leaves markers | Merge aborted (clean working tree left behind); `resolve-conflict` job fails; `merge` never runs | Job failure surfaces to the developer, not a silent stop |
| `claim-merge-conflict-attempt` request | Valid stage-callback secret | DynamoDB `merge_conflict_attempts` atomically incremented; new count returned in the response body | A GitHub/DynamoDB failure raises, surfacing in Lambda logs |

</frozen-after-approval>

## Code Map

- `factory/scripts/attempt_target_merge.py` -- new. `attempt_merge(story_slug, run_id, target, *, cwd=None) -> tuple[bool, list[str]]`: checks out the feature branch (reuses `checkout_branch.checkout_branch`), `git fetch origin <target>`, then `git merge --no-commit --no-ff origin/<target>`. Returns `(False, [])` on a clean merge (left staged, uncommitted). On conflict, returns `(True, conflicted_paths)` where `conflicted_paths` comes from `git diff --name-only --diff-filter=U`, captured once right here (it never changes afterward -- `git add` is what would clear a path's unmerged-index state, and the agent never runs it). Raises `MergeAttemptError` if `git merge` fails for any reason other than a real conflict (its stdout/stderr must contain `"CONFLICT"`), e.g. a missing target ref. Also exposes `has_unresolved_markers(paths, *, cwd=None) -> bool`: reads each given path and checks for a `<<<<<<< ` line -- the deterministic resolution signal `merge_conflict_graph.py`'s loop re-checks after every agent attempt. CLI (`--story-slug`/`--run-id`/`--target`, default `main`): calls `attempt_merge`, always `git merge --abort` afterward regardless of outcome (a pure probe -- `detect-conflict`'s only caller), prints `{"ok": true, "has-conflict": bool}` shaped for `>> "$GITHUB_OUTPUT"` via a `has-conflict=true/false` line.
- `orchestrator/dynamodb_state.py` -- add `claim_merge_conflict_attempt(story_slug, run_id) -> int`: `UpdateItem` with `UpdateExpression="ADD merge_conflict_attempts :one"` (`ExpressionAttributeValues={":one": {"N": "1"}}`), `ReturnValues="UPDATED_NEW"`, returns the new int count. `ADD` on a non-existent attribute starts it at the given value -- no `if_not_exists` needed. Requires `dynamodb:UpdateItem`, not yet granted (see infra below).
- `orchestrator/handler.py` -- the stage-callback-secret-verified branch gains a second request shape, distinguished by an `"action"` key (absent in entry 6/7's existing `{"stage", "story-slug", "run-id", "status"}` shape, which is untouched): `{"action": "claim-merge-conflict-attempt", "story-slug", "run-id"}` routes to new `_handle_claim_merge_conflict_attempt(raw_body) -> int`, which calls `dynamodb_state.claim_merge_conflict_attempt` and returns the count. `handler()`'s stage-callback branch now calls this when `"action"` is present, `_handle_stage_callback` otherwise, and includes the count in the response body (extend `_accepted` with an optional `**extra` kwarg merged into the response dict, e.g. `_accepted("stage-callback", attempt=count)`).
- `factory/graph/merge_conflict_graph.py` -- new, mirrors `fix_loop_graph.py`'s shape. `run_conflict_resolution(story_slug, run_id, *, target="main", claude_bin="claude", orchestrator_url, stage_callback_secret, cwd=None) -> dict`: calls `attempt_target_merge.attempt_merge`; if clean, commits+pushes immediately via `commit_push_implementation.commit_and_push(..., label="Conflict Resolution")` and returns `{"resolved": True, "attempts": 0}` (handles the rare case where `main` moved between `detect-conflict`'s probe and this job's own check). If conflicted: loop -- call `claim_merge_attempt.claim(orchestrator_url, stage_callback_secret, story_slug, run_id)` (new script, mirrors `post_stage_callback.py`'s POST-with-shared-secret shape, parses the `attempt` field from the response body); if the returned count exceeds `MAX_MERGE_CONFLICT_ATTEMPTS = 2`, `git merge --abort` (cwd) and raise `ConflictCapReachedError`; otherwise invoke the new skill (`claude -p "/software-factory-merge-conflict-resolution <path> [<path> ...]" --allowedTools "Read Write Edit Grep Glob" --permission-prompts none`, conflicted paths from the first `attempt_merge` call); then `attempt_target_merge.has_unresolved_markers(conflicted_paths, cwd=cwd)` -- markers gone: commit+push, return `{"resolved": True, "attempts": cycle}`; markers remain: loop again (same merge, re-invoke the agent). `build_graph()` wraps it exactly like `fix_loop_graph.build_graph`. CLI mirrors `fix_loop_graph.py main()`'s exit-code convention (distinct codes per exception type: invocation failure, git/checkout failure, commit/push failure, cap-reached).
- `factory/scripts/claim_merge_attempt.py` -- new, mirrors `post_stage_callback.py`'s plain-`urllib.request` POST-with-shared-secret shape exactly (same `StageCallbackError`-style exception, same header). `claim(url, secret, story_slug, run_id) -> int`: POSTs `{"action": "claim-merge-conflict-attempt", "story-slug": story_slug, "run-id": run_id}`, parses `attempt` from the JSON response body.
- `.claude/skills/software-factory-merge-conflict-resolution/SKILL.md` -- new skill. Frontmatter: `name: software-factory-merge-conflict-resolution`, `description:` naming its invoker (`merge_conflict_graph.py`) and scope (CAP-11, AD-19), mirroring `software-factory-implementation/SKILL.md`'s structure/tone exactly: invoked as `/software-factory-merge-conflict-resolution <path> [<path> ...]`, told a deterministic script already staged a real `git merge --no-commit --no-ff` leaving each path's conflict regions (`<<<<<<<`/`=======`/`>>>>>>>`) for it to resolve via `Read`/`Write`/`Edit`/`Grep`/`Glob` only (no Bash/git tool, no merge/admin tool), removing every marker line, free to touch any path in the given list anywhere in the tree (not restricted to a subtask-file list, unlike the implementation agent -- AD-19's explicit difference from AD-5's path dimension), scoped to resolving the merge, not re-implementing or re-reviewing the story; no structured output, the calling script verifies by re-scanning, not by anything the agent says.
- `.github/workflows/merge.yml` -- new `detect-conflict` job (first; `contents: read` only -- no push; calls `attempt_target_merge.py`'s CLI; `outputs.has-conflict`). New `resolve-conflict` job (`needs: detect-conflict`, `if: needs.detect-conflict.outputs.has-conflict == 'true'`; `contents: write` for the commit/push; env `CLAUDE_CODE_OAUTH_TOKEN`, `ORCHESTRATOR_FUNCTION_URL`/`STAGE_CALLBACK_SECRET` as `vars`/`secrets` matching entry 6's precedent; Install Node + Claude Code CLI steps identical to `implementation`'s job; calls `uv run factory/graph/merge_conflict_graph.py`). `merge` job's `needs:` becomes `[detect-conflict, resolve-conflict]`, condition updated to `!cancelled() && (needs.detect-conflict.outputs.has-conflict == 'false' || needs.resolve-conflict.result == 'success')` (mirrors `implementation-checks-review.yml`'s `review` job's own allow-list-style condition against `checks`/`checks-fix-loop`). `close-rejected-pr`'s `needs: merge` and condition are unchanged.
- `infra/main.tf` -- add `dynamodb:UpdateItem` to `aws_iam_role_policy.lambda_dynamodb`'s `Action` list (new permission this entry needs; `GetItem`/`PutItem` already granted).
- New tests: `factory/scripts/tests/test_attempt_target_merge.py`, `test_claim_merge_attempt.py`; `factory/graph/tests/test_merge_conflict_graph.py` (mocks the skill invocation and `claim_merge_attempt.claim`, exercises the 0/1/2-attempt and cap-reached paths from the I/O matrix); `orchestrator/tests/test_dynamodb_state.py` extended (`TestClaimMergeConflictAttempt`); `orchestrator/tests/test_handler.py` extended (the new `"action"` dispatch, both success and the existing stage-report path still passing unchanged).

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/attempt_target_merge.py` -- the deterministic merge-conflict probe + marker-resolution check -- shared by `detect-conflict` and the resolve loop
- [ ] `orchestrator/dynamodb_state.py` + `handler.py` -- `claim_merge_conflict_attempt` + the new `"action"`-dispatched request shape -- the orchestrator-owned counter AD-19 requires
- [ ] `infra/main.tf` -- add `dynamodb:UpdateItem` -- the IAM permission the new write needs
- [ ] `.claude/skills/software-factory-merge-conflict-resolution/SKILL.md` -- the new agent -- AD-19's permission shape
- [ ] `factory/graph/merge_conflict_graph.py` + `factory/scripts/claim_merge_attempt.py` -- the bounded loop and its orchestrator-call script
- [ ] `.github/workflows/merge.yml` -- `detect-conflict`/`resolve-conflict` jobs, `merge`'s updated `needs:`/`if:` -- wires AD-19's 3-job chain
- [ ] All new/extended tests per the I/O matrix

**Acceptance Criteria:**
- Given a branch that merges cleanly against `main`, when `merge.yml` runs, then `resolve-conflict` is skipped entirely and `merge` runs exactly as today.
- Given a branch engineered to conflict, when `merge.yml` runs and the agent's first edit leaves no markers, then the branch is committed/pushed and `merge` proceeds.
- Given a branch engineered to still conflict after 2 attempts, when `merge.yml` runs, then `resolve-conflict` fails (merge aborted, working tree clean), `merge` never runs, and the DynamoDB row shows `merge_conflict_attempts == 2`.
- Given a `claim-merge-conflict-attempt` request, when the orchestrator processes it, then the returned count increments by exactly 1 per call for the same story/run, independent of any other control-plane field on that row.

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-04):** 3 findings routed. Verdict counts: high=1, medium=2, all patch.

- `merge_conflict_graph.py`'s loop claims an attempt from the orchestrator, THEN checks the cap — **high, patch.** Verified by tracing `run_conflict_resolution`: each iteration calls `claim()` first, compares the result to the cap, and only then invokes the skill. Reaching the cap after exactly 2 real agent invocations requires a 3rd `claim()` call purely to discover it's over budget, leaving `merge_conflict_attempts == 3` in DynamoDB — directly contradicting this plan's own frozen AC ("the DynamoDB row shows `merge_conflict_attempts == 2`"). The existing `test_cap_reached_...` test bakes in `side_effect=[1, 2, 3]` but never asserts the claim count or final value, so the suite passes despite the AC being false. Fix: check the cap against the *previously* claimed count before calling `claim()` again, not against a fresh claim's result — so a cap-out needs exactly 2 claims, matching the 2 real attempts.
- `merge_conflict_graph.py`'s `_build_command` grants `Edit`/`Write` with no `--settings` deny rule at all — **medium, patch.** Verified against `implementation_graph.py:44-59`, which pairs the same tool allowlist with a `DENY_SETTINGS` excluding `Edit` on `plan.md`/`decisions.md`/`review.md`/`checks.md`, and against root `AGENTS.md`'s explicit Policy line naming exactly this rule (AD-5's second, independent enforcement layer). The plan's Boundaries only address this agent's *path scope* being wider than the implementation agent's (deliberately, AD-19) — never that it should also skip the deny-rule layer entirely; that was an unaddressed omission, not a considered exception. `.factory/` path uniqueness (AD-8/AD-15) likely keeps the specific collision unreachable today, but AD-5's own stated point is that neither layer is sufficient alone, and this agent currently has zero of the second layer. Fix: add the same `DENY_SETTINGS` (identical paths) to `merge_conflict_graph.py`'s `_build_command`.
- `attempt_target_merge.has_unresolved_markers` only detects content-marker conflicts — **medium, patch (safety guard, not new capability).** Verified: a delete/modify conflict leaves the surviving side's full content with zero marker lines (git's own behavior for this conflict type), and the agent has no tool (Read/Write/Edit/Grep/Glob, no delete) to meaningfully resolve one anyway — so today's code would silently report "resolved" (zero markers found) on a conflict the agent never actually looked at, then commit and merge an unreviewed, git-arbitrary result. This is a real gap the plan's I/O matrix never named (it only covers content-marker conflicts) — but AD-19/the ticket's own explicit bias is unambiguous ("on cap-out the job fails and surfaces... instead of merging or looping again" — fail safe, never silently merge an unresolved state), so there is exactly one sensible reading: detect this case and fail loudly, not extend the agent's capabilities. Fix: right after the initial `attempt_merge()` reports a conflict, check every path in `conflicted_paths` for at least one marker line (reuse `has_unresolved_markers`-style scanning) *before* claiming any attempt; if any path has none, abort the merge and raise a new, distinct exception (e.g. `UnsupportedConflictTypeError`) rather than entering the loop at all.

Patches applied and re-verified independently: the cap check now runs against the locally-tracked already-claimed count *before* calling `claim()` again (confirmed via direct trace: a cap-out after 2 real attempts costs exactly 2 `claim()` calls, not 3), with a second defensive check retained right after `claim()` for a prior crashed job's count already over cap; `DENY_SETTINGS` (identical to `implementation_graph.py`'s) wired into `_build_command`; a new `_paths_without_markers` check runs before any claim/invocation, raising `UnsupportedConflictTypeError` and aborting the merge for a delete/modify-style conflict. Full suite re-run: `factory/graph/tests/`+`factory/scripts/tests/` 435/435 (was 431), `orchestrator/` 81/81, `terraform fmt -check && terraform validate` clean, YAML parse clean, `ruff check factory/` clean.

## Design Notes

Re-running `git merge` to check "is it still conflicted" would always say "clean" the instant the first conflict is staged (`--no-commit` leaves it staged in the index regardless of whether the agent actually finished), so it can never distinguish "agent fixed it" from "agent did nothing" — the only trustworthy signal is scanning the conflicted files' own content for leftover marker lines, captured once as the fixed path list from the first `attempt_merge` call (the index's "unmerged" state doesn't change without a `git add` the agent never runs, so re-querying it would be equally useless).

The attempt counter is DynamoDB, not a git-committed file (unlike AD-11/AD-13's counters), per AD-19's own explicit Rule — this keeps it correct across a GitHub Actions job retry/rerun (a local Python variable would reset to zero) without inventing a new state file with no other purpose; it reuses the per-run control-plane row entries 6/7 already established under the same composite key.

`detect-conflict` exists as a separate first job (not folded into `resolve-conflict`) specifically so the common, no-conflict case never pays for an agent invocation, Node install, or Claude Code CLI setup at all — `resolve-conflict` is entirely skipped via its own `if:`, not just a no-op loop iteration inside it.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all tests pass
- `cd orchestrator && uv run --with pytest pytest tests/ -v` -- expected: all tests pass
- `cd infra && terraform fmt -check && terraform validate` -- expected: valid (a diff is expected this entry, for the new IAM action)
- `uv run --with pyyaml python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/merge.yml` -- expected: no exception
- `uv run --with ruff ruff check factory/` -- expected: clean

**Manual checks (if no CLI):**
- The live exercise (a branch deliberately engineered to conflict, confirming the agent resolves it and the merge proceeds; a branch engineered to still conflict after 2 attempts, confirming the job stops and surfaces to the developer) runs only after separate, explicit confirmation — the ticket's own Notes name a human reviewing the agent's actual first real resolution diff before trusting it unattended, not part of this plan's automated verification.

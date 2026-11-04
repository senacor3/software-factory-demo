---
title: 'Gate 1 comment grammar wired live; plan-approval Environment removed'
type: 'feature'
ticket: '5'
created: '2026-11-04'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: 'f477a4ed5fda26d44e2c428b87bc748c1197219e'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `plan-approval` is still a dead GitHub Environment reference in `implementation-checks-review.yml`; nothing yet reads the `/approve`, `/rework <feedback>`, `/reject` command grammar AD-2 defines, so Gate 1 cannot actually be exercised via PR comments at all.

**Approach:** Extend the webhook branch of `handler.py` to parse `issue_comment` events on a PR into one of the three commands (a reusable, gate-agnostic parser) and act: `/approve` dispatches `implementation-checks-review.yml`; `/rework <feedback>` appends the feedback to the resolved story file on `main` and re-dispatches `analysis.yml`; `/reject` marks the run terminal in DynamoDB and closes the PR. Remove `environment: plan-approval` from the `implementation` job so nothing GitHub-native gates it anymore.

## Boundaries & Constraints

**Always:** Reuse existing `github_app.py`/`auth.py` patterns (urllib.request, the same `_REPO` constant, RuntimeError-on-HTTPError) — no new pip dependency. Only act on `issue_comment` events with `action == "created"`, `issue.pull_request` present, and a non-bot comment author. A comment matching none of the three commands (or `/rework` with no feedback text) is silently ignored — no reply, no error — a human chatting on the PR must never get a bot reply. The feedback-append commit and the re-dispatch's `ref` both target `main` (verified: no branch protection configured on the real repo; `workflow_dispatch` only resolves a workflow file present on the default branch regardless of `ref`, per entry 4's live finding). `/reject` writes DynamoDB via `PutItem` only, matching the IAM policy already granted. `comment_commands.parse_gate_command` is a standalone, gate-agnostic helper entry 7 reuses as-is.

**Never:** No DynamoDB read/write for `/approve` or `/rework` (stage-tracking and idempotency hardening are entries 6/9's). No UI/OAuth caller handling. No deletion of the `plan-approval` Environment resource from repo settings, nor of `close_rejected_pr.py` (entry 10). No change to `evidence-approval`'s job or Environment (entry 7's scope). No unattended live cutover — the real three-command exercise runs only after separate, explicit confirmation.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| `/approve` on an open PR | `issue_comment` created, body `/approve`, `issue.pull_request` present | `implementation-checks-review.yml` dispatched (`ref=main`) with story-slug/run-id parsed from the PR's head branch; confirmation comment posted | A GitHub API failure raises, surfacing in Lambda logs — never silently swallowed |
| `/rework <feedback>` | body `/rework please also handle X` | Feedback appended as a new commit to the resolved story file on `main`; `analysis.yml` re-dispatched with that file's path; confirmation comment posted | Story file not found under either project path -> rejected response naming the problem |
| `/reject` | body `/reject` | DynamoDB item at `story_slug#run_id` set to a terminal status; PR closed; explanatory comment posted | N/A |
| Non-command comment | body "looks good, thanks!" | Ignored: no GitHub API call, no reply, 200 accepted | N/A |
| Comment on a plain issue | `issue.pull_request` absent | Ignored | N/A |
| Comment by a bot | `comment.user.type == "Bot"` | Ignored | N/A |
| `/rework` with no feedback text | body `/rework` alone | Treated as unrecognized; ignored like a non-command comment | N/A |

</frozen-after-approval>

## Code Map

- `orchestrator/comment_commands.py` -- new: `parse_gate_command(body: str) -> GateCommand` (dataclass: `kind` in `approve`/`rework`/`reject`/`none`, `feedback: str | None`). First-line match for `/approve`/`/reject`; `/rework\s+(.+)` (DOTALL) for rework, empty/missing feedback -> `none`. Gate-agnostic, reused by entry 7.
- `orchestrator/github_app.py` -- extend with: `get_pull_request(token, pr_number) -> dict` (GET `/pulls/{n}`, need `head.ref`); `dispatch_workflow(token, workflow_file, ref, inputs) -> None` (POST `/actions/workflows/{file}/dispatches`); `get_file_content(token, path, ref) -> tuple[str, str]` (GET `/contents/{path}?ref=`, returns decoded content + `sha`); `update_file_content(token, path, branch, content, sha, message) -> None` (PUT `/contents/{path}`); `close_pull_request(token, pr_number) -> None` (PATCH `/pulls/{n}` `{"state": "closed"}`). Same `_REPO`, same error style as existing `get_installation_token`/`post_comment`.
- `orchestrator/dynamodb_state.py` -- new: `mark_terminal(story_slug: str, run_id: str, reason: str) -> None`. Lazy `import boto3` (mirrors `handler._load_github_app_credentials`), `PutItem` against table `light-factory-orchestrator-state` (must match `local.table_name` in `infra/main.tf`), key `story_slug#run_id`.
- `orchestrator/handler.py` -- extend the `github-webhook`-accepted branch: parse the JSON body as an `issue_comment` event; guard (`action == "created"`, `issue.pull_request` present, non-bot author); `comment_commands.parse_gate_command`; on `none`, return 200 with no action; otherwise mint a JWT + installation token (reuse `github_app.mint_jwt`/`get_installation_token`) and dispatch per command. Branch name `software-factory/<story-slug>/<run-id>` (from `get_pull_request`'s `head.ref`) parses directly into slug/run-id -- no DynamoDB read needed for `/approve`/`/reject`.
- `.github/workflows/implementation-checks-review.yml` -- remove `environment: plan-approval` from the `implementation` job (AD-2: Gate 1's GitHub-native path removed; repo-settings Environment resource itself stays until entry 10).
- `orchestrator/tests/test_comment_commands.py` -- new: approve/reject/rework-with-feedback/rework-without-feedback/plain-comment parsing.
- `orchestrator/tests/test_github_app.py` -- extend: the 5 new functions, success + HTTPError paths, mocking `urllib.request.urlopen`.
- `orchestrator/tests/test_dynamodb_state.py` -- new: `mark_terminal` issues the expected `PutItem` call (mock `boto3.client`).
- `orchestrator/tests/test_handler.py` -- extend: `/approve` dispatches + comments; `/rework` appends + re-dispatches; `/reject` marks terminal + closes + comments; non-command / non-PR / bot-authored comments make zero GitHub-API/DynamoDB calls (mock `github_app.*`, `dynamodb_state.mark_terminal`).

## Tasks & Acceptance

**Execution:**
- [ ] `orchestrator/comment_commands.py` -- add the gate-agnostic command parser -- the shared grammar entry 7 reuses
- [ ] `orchestrator/github_app.py` -- add dispatch/PR/content/close helpers -- the GitHub API surface `/approve`/`/rework`/`/reject` need
- [ ] `orchestrator/dynamodb_state.py` -- add `mark_terminal` -- the only DynamoDB write this entry owns
- [ ] `orchestrator/handler.py` -- wire parsing + the three command branches into the webhook path -- makes Gate 1 actually actionable
- [ ] `.github/workflows/implementation-checks-review.yml` -- drop `environment: plan-approval` -- removes the GitHub-native gate from this path
- [ ] `orchestrator/tests/test_comment_commands.py`, extended `test_github_app.py`/`test_handler.py`, new `test_dynamodb_state.py` -- cover every row of the I/O matrix

**Acceptance Criteria:**
- Given a `/approve` comment on an open PR, when the webhook fires, then `implementation-checks-review.yml` is dispatched with the story-slug/run-id parsed from the PR's branch, with no Environment review requested.
- Given a `/rework <feedback>` comment, when the webhook fires, then the feedback is committed to the resolved story file on `main` and `analysis.yml` is re-dispatched with that file's path.
- Given a `/reject` comment, when the webhook fires, then the run is marked terminal in DynamoDB and the PR is closed with an explanatory comment.
- Given a comment matching none of the three commands, when the webhook fires, then no GitHub API call is made and no reply is posted.
- Given the `implementation` job in `implementation-checks-review.yml`, when inspected, then it carries no `environment:` key.

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-04):** 2 findings routed. Verdict counts: high=2, both patch.

- `infra/main.tf`'s `null_resource.install_dependencies` (`triggers` map and `local-exec` `cp` list) was not extended for the two new modules `orchestrator/comment_commands.py`/`orchestrator/dynamodb_state.py` — **high, patch.** Verified: `handler.py` imports both at module level unconditionally; neither is hashed in `triggers` nor copied into `build_dir` before zipping. A real `terraform apply` ships a Lambda package missing both files, so the Lambda crashes with `Runtime.ImportModuleError` on cold start for every invocation — not just the webhook path, since the import happens before any dispatch logic runs. The plan's own "no infra change this entry" (Design Notes/Verification, non-frozen) was itself the gap: it's true for IAM/DynamoDB resources but missed that the existing packaging mechanism also lives in `infra/main.tf` and needs its file list extended whenever a new module `handler.py` imports is added. Fix: add `comment_commands_hash`/`dynamodb_state_hash` to `triggers` and two more `cp` lines, mirroring the existing three exactly.
- `handler.py`'s `_handle_reject` unconditionally calls `github_app.close_pull_request`/`post_comment` regardless of whether `_parse_branch(pr["head"]["ref"])` matched — **high, patch.** Verified against the diff: `_handle_approve`/`_handle_rework` both `return` immediately when `_parse_branch` returns `None` (per its own docstring: "a comment on an unrelated PR is a no-op"), but `_handle_reject` only gates the `dynamodb_state.mark_terminal` call on that check, not the close/comment calls. Practical effect: a `/reject` comment on ANY open PR in the repo — not one this pipeline opened — closes it and posts a bot comment, since GitHub webhook signature verification authenticates the webhook's origin, not which PR a comment targets. No test exercises `/reject` against a non-matching branch. Fix: guard `close_pull_request`/`post_comment` behind the same `if parsed is None: return` pattern the other two handlers already use.

Both patches applied and re-verified independently: `infra/main.tf`'s packaging `triggers`/`cp` list now includes both new modules (`terraform fmt -check && terraform validate` clean); `_handle_reject` now returns immediately on a non-matching branch, before any DynamoDB/GitHub call, with a new regression test covering it. Full suite: 62/62 tests pass (was 61 — the new regression test).

## Design Notes

Story-file path resolution for `/rework`: a slug alone doesn't carry its project subfolder (AD-8), but slugs are enforced globally unique (`epic-pipeline-hardening`/3), so trying `stories/light-factory/<slug>.md` then `stories/freight-tenders/<slug>.md` via the Contents API and using whichever responds 200 is deterministic, not a guess (the other must 404). Note: the real repo's folder is `stories/light-factory/`, not `stories/software-factory/` as AD-8's prose names it — ratifying the live repo over the prose; out of scope to fix here.

Branch-name parsing (`software-factory/<story-slug>/<run-id>`, AD-12/AD-20) gives both identifiers directly from the PR's head ref for `/approve`/`/reject` — no DynamoDB read needed.

This entry does not verify a PR is actually "currently awaiting plan-approval" before acting — stage-aware checks belong to entries 6/9. It acts on any open PR's recognized command, matching this ticket's own Notes ("a human watches a real run exercise all three commands before trusting it unattended").

DynamoDB write is a plain `PutItem`, not yet AD-20's atomic conditional write — matches the IAM policy already granted (`GetItem`/`PutItem` only, no infra change this entry) and keeps scope to "/reject marks it terminal" without pulling in entry 9's idempotency hardening.

## Verification

**Commands:**
- `cd orchestrator && uv run --with pytest --with "PyJWT[crypto]" pytest tests/ -v` -- expected: all tests pass
- `cd infra && terraform fmt -check && terraform validate` -- expected: no diff (no infra changes this entry)
- `grep -c "environment: plan-approval" .github/workflows/implementation-checks-review.yml` -- expected: `0`
- `python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/implementation-checks-review.yml` -- expected: no exception

**Manual checks (if no CLI):**
- The live three-command exercise (a human posting `/approve`, `/rework`, `/reject` on a real test PR and watching the orchestrator act on each) runs only after separate, explicit confirmation, per the ticket's own Notes — not part of this plan's automated verification.

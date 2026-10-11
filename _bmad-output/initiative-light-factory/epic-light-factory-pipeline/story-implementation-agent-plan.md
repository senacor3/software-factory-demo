---
title: 'Implementation agent'
type: 'feature'
ticket: '7'
created: '2026-10-02'
status: done
baseline_revision: 'ef2fcfe0fb68bea8b8ee2bd536722d8041555c6a'
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

**Problem:** Job 2 ("implementation") is still the ticket-1 stub — it re-derives the slug/run-id for a propagation assertion and echoes a one-line message. No implementation agent exists, and the branch entry 3 already opened at intake is never checked out or written to. CAP-4 (scoped implementation) is unbuilt.

**Approach:** Add a new `.claude/skills/light-factory-implementation/` skill (Read/Write/Edit/Grep/Glob only) invoked by a new `factory/graph/implementation_graph.py`. The graph sequences three steps around the agent: (1) a deterministic script checks out the exact branch entry 3 opened — never creates one; (2) the skill implements `plan.md`'s subtasks via Write/Edit against that checkout; (3) a second deterministic script commits and pushes the result on that same branch. AD-5's two enforcement layers both apply to step 2: a `--allowedTools` tool-allowlist (no Bash/git/gh/merge tool) plus a `--settings` inline deny rule excluding `plan.md`/`decisions.md`/`review.md` from Edit, since those files sit on the same branch the agent can otherwise write anywhere in.

## Boundaries & Constraints

**Always:** branch checkout and the post-edit commit+push are deterministic script steps, never the agent's own tool call — mirrors AD-12's "script does the git write" precedent; checkout reuses the branch formula `light-factory/<story-slug>/<run-id>` (AD-8/AD-12/AD-15), never creates/re-derives it; the agent's invocation carries both `--allowedTools "Read Write Edit Grep Glob"` and a `--settings` inline deny JSON for `Edit(.factory/**/plan.md)`, `Edit(.factory/**/decisions.md)`, `Edit(.factory/**/review.md)` (verified via WebSearch: `--settings` takes inline JSON, one session only — same per-invocation precedent as the existing `--allowedTools`/`--permission-prompts` flags).

**Never:** no new branch/PR (entry 3 already opened it); no Bash/git/gh tool on the agent's allowlist; no merge/admin tool anywhere here; no build/test/lint/security in the graph (AD-6 — entry 8's scope); no review or fix-loop logic (entries 9/10).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Agent succeeds, makes file changes | plan.md's subtasks resolved via Write/Edit calls | Checkout succeeds, agent edits land on disk, commit created and pushed to the existing branch; no new branch/PR | n/a |
| Agent succeeds, makes no changes | Trivial plan, nothing to write | `git status --porcelain` is empty; no commit attempted; outcome recorded as a no-op, not an error | n/a — distinguishable "no changes" outcome |
| `claude` CLI invocation itself fails | Non-zero exit / malformed output | Raises `ImplementationInvocationError`; no commit attempted | Distinct from the no-changes and checkout-failure outcomes |
| Branch checkout fails | Branch missing/unreachable (defensive — shouldn't happen given entry 3 already opened it) | Raises `CheckoutError` before the agent is ever invoked | Distinct exception; no agent invocation attempted |
| Commit/push fails after the agent succeeded | git/gh subprocess error | Raises `CommitPushError`; agent's edits remain on disk uncommitted for operator inspection | Distinct from the above three |

</frozen-after-approval>

## Code Map

- `factory/scripts/checkout_branch.py` -- new. `CheckoutError(RuntimeError)`; `checkout_branch(story_slug, run_id, *, cwd=None) -> str` returns the branch name; `git fetch origin <branch>` + `git checkout <branch>` via a local `_run` helper (duplicated from `open_implementation_pr.py`'s, not imported — established convention).
- `factory/scripts/commit_push_implementation.py` -- new. `CommitPushError(RuntimeError)`; `commit_and_push(branch, story_slug, run_id, *, cwd=None) -> dict` returns `{"committed": bool}`. `git status --porcelain` first; empty → `{"committed": False}`, no commit attempted; non-empty → `git add -A`, commit (same `user.name`/`user.email` as `open_implementation_pr.py`'s), `git push origin <branch>`.
- `.claude/skills/light-factory-implementation/SKILL.md` -- new. Mirrors `light-factory-analysis/SKILL.md`. Tools: Read, Write, Edit, Grep, Glob. Reads `.factory/<story-slug>/<run-id>/plan.md`/`decisions.md` (paths passed in), implements each subtask against the checked-out tree. States it must never touch `plan.md`/`decisions.md`/`review.md` (the deny rule enforces this independently of the prompt, AD-5's two-layer model).
- `factory/graph/implementation_graph.py` -- new. Mirrors `analysis_graph.py`'s shape: `_build_command` (adds `--settings` inline deny JSON alongside `--allowedTools`/`--permission-prompts none`); `invoke_skill` (raises `ImplementationInvocationError` on tooling failure; returns raw text — no JSON schema, since the agent reports no judgment verdict to branch on, unlike analysis's complete/in_scope); `run_implementation(story_slug, run_id, *, claude_bin="claude", cwd=None) -> dict` sequencing `checkout_branch.checkout_branch` -> `invoke_skill` -> `commit_push_implementation.commit_and_push`; a minimal `build_graph()`/`main()` CLI pair matching `analysis_graph.py`'s.
- `.github/workflows/light-factory.yml` -- edit the `implementation` job: keep the initial `actions/checkout@v7` and the propagation-assert step; replace "Implementation stub" with Install Node/claude-CLI steps (mirrors Job 1) and a "Run implementation" step invoking `implementation_graph.py` with `CLAUDE_CODE_OAUTH_TOKEN`/`GH_TOKEN` env (same as Job 1's "Run analysis"). Add `contents: write` to `permissions:` (no `pull-requests: write` — no PR opened/closed here).
- `factory/scripts/tests/test_checkout_branch.py`, `factory/scripts/tests/test_commit_push_implementation.py`, `factory/graph/tests/test_implementation_graph.py` -- new, `git`/`gh` mocked (same pattern as the existing test files).

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/checkout_branch.py` -- add `checkout_branch` and `CheckoutError`
- [x] `factory/scripts/commit_push_implementation.py` -- add `commit_and_push` and `CommitPushError`
- [x] `.claude/skills/light-factory-implementation/SKILL.md` -- new skill, Read/Write/Edit/Grep/Glob only
- [x] `factory/graph/implementation_graph.py` -- add `invoke_skill`, `run_implementation`, `build_graph`, `main`
- [x] `.github/workflows/light-factory.yml` -- wire the real implementation steps into Job 2, add `contents: write`
- [x] `factory/scripts/tests/test_checkout_branch.py` -- new tests per the I/O Matrix (checkout success, `CheckoutError`)
- [x] `factory/scripts/tests/test_commit_push_implementation.py` -- new tests per the I/O Matrix (committed, no-op, `CommitPushError`)
- [x] `factory/graph/tests/test_implementation_graph.py` -- new tests per the I/O Matrix (full sequence, each failure mode)
- [x] Run `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- all pass (98 passed)

**Acceptance Criteria:**
- Given a run that reached `plan-approval` and was approved, when the implementation job runs, then it checks out the exact branch entry 3 opened (no new branch/PR created), the agent edits files per `plan.md` using only Write/Edit, and those edits land as a commit pushed to that same branch.
- Given the implementation agent's Claude Code invocation, when its `--allowedTools` and `--settings` deny rules are inspected, then it carries no Bash/git/gh/merge/admin tool and cannot `Edit` `plan.md`/`decisions.md`/`review.md` despite those files sitting on the same branch.
- Given the agent makes no file changes, when `commit_and_push` runs, then no commit is attempted and the outcome is recorded as a no-op (`{"committed": False}`), not an error.

## Implementation Notes

## Plan Change Log

## Review Triage Log

- **Quick lens, 2026-10-02: 3 findings, all `false`.** Shared claimed root cause: `DENY_SETTINGS` in `implementation_graph.py` only lists `Edit(.factory/**/plan.md|decisions.md|review.md)`, not `Write(...)`, and `--allowedTools` grants both `Write` and `Edit`, so (per the reviewer) a `Write` call would bypass the deny rule.
  - Finding 1 (`implementation_graph.py:244-252`, `DENY_SETTINGS` only covers `Edit`, not `Write`) — **false**. Verified against Claude Code's own permissions docs (fetched `https://code.claude.com/docs/en/permissions`, not assumed): *"`Edit` rules apply to all built-in tools that edit files"* and *"Claude Code checks file permissions against `Edit(path)` and `Read(path)` rules only. If you write a path rule for `Write`... Claude Code accepts the rule but never consults it... Use `Edit(docs/**)` in place of `Write(docs/**)`."* `Edit(.factory/**/plan.md)` already blocks `Write` calls against that path — a `Write(...)` rule would be the one that's a no-op, not the reverse. The implementation matches the documented correct pattern exactly.
  - Finding 2 (`commit_push_implementation.py:718-750`, no downstream safeguard against a `Write` bypass) — **false**, same refutation: there is no `Write` bypass for a safeguard to catch.
  - Finding 3 (`test_implementation_graph.py:544-551`, test only asserts `Edit(...)` deny entries) — **false**, same refutation: asserting `Edit(...)` entries is the correct and complete test; a `Write(...)` assertion would test for a rule Claude Code never consults.
  No loopback triggered.

## Design Notes

**Why no JSON schema, unlike `light-factory-analysis`:** analysis's CAP-1/CAP-2 are judgment verdicts the script branches on (halt vs. write, which status). Implementation has no such branch — success is "the CLI exited 0," and the commit step decides committed-vs-no-op from `git status`, not from the agent's report. A schema here is unused ceremony.

**Why commit/push is a separate script from checkout:** checkout runs *before* the agent (working tree must exist first); commit/push runs *after* (edits must already be on disk) — two temporally distinct responsibilities bracketing one invocation, unlike entry 3's create-branch-and-open-PR, which stayed one script because both halves are the single responsibility "open the PR."

**Why `--settings` inline deny JSON, not a committed `.claude/settings.json`:** this rule is specific to one skill's one invocation, not a project-wide policy. `analysis_graph.py`'s `_build_command` already scopes flags per-invocation (`--allowedTools`/`--permission-prompts`); `--settings` follows the same precedent (verified via WebSearch, not assumed: it accepts inline JSON, one session only).

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass

**Manual checks (if no CLI):**
- Inspect the "Run implementation" workflow step's `--allowedTools`/`--settings` flags directly for the tool-allowlist and deny-rule acceptance criterion — no automated check for the exact flag string, just that both are present and correctly scoped.
- Caveat, honestly stated: unit tests mock the `claude` subprocess call entirely, so they cannot exercise whether the CLI's own `--settings` deny rule actually blocks an Edit against `plan.md`/`decisions.md`/`review.md` at runtime — only that the flag is constructed and passed correctly. That real enforcement is only provable by a live run (same category of gap as the already-deferred live-dispatch verifications); flag for a future live-verify pass if CAP-4's security boundary needs stronger proof than static inspection.

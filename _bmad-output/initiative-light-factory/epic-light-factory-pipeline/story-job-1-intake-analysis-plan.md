---
title: 'Job 1: intake + analysis'
type: 'feature'
ticket: '3'
created: '2026-10-01'
status: 'built'
baseline_revision: 'a96e829309f218e204fadb7c7e9b6816e642e6d0'
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

**Problem:** Job 1 currently only stubs an echo step. CAP-1/CAP-2 need a real analysis stage: judge whether the triggering story is complete/in-scope, and if so propose a solution with subtasks and tests, writing `plan.md`/`decisions.md` through entry 2's `state_io.py`. (Entry 4, not this ticket, adds the clarification-loop round counter and cap-out path around this.)

**Approach:** Add a read-only `.claude/skills/light-factory-analysis/` skill (judges completeness/scope, proposes a solution, derives subtasks/tests, lists open questions — all in one structured-JSON response) and `factory/graph/analysis_graph.py` (a minimal LangGraph graph: one node shells out to `claude -p "/light-factory-analysis ..." --output-format json --json-schema <schema> --allowedTools "Read Grep Glob"`, parses `structured_output`, and routes to one of three outcomes — incomplete/out-of-scope halts with no file written; complete with no open questions writes `plan.md`+`decisions.md` via `state_io.py` with `status: ready-for-review`; complete with open questions writes both with `status: awaiting-clarification`, carrying the questions for entry 4's loop to pick up). Wire the workflow's `analysis` job to invoke it after the existing slug/run-id derivation step, replacing the stub echo.

**Decision:** CAP-1's "complete"/"in-scope" judgment is loose and agent-driven — no required template or sections; the skill prompt asks only "is this clear enough to design a solution, and does it belong in this codebase's scope?" — user's call, 2026-10-01.

**Decision:** implement the full workflow-wiring now (not split into a separate ticket), but defer the live dispatch itself: `CLAUDE_CODE_OAUTH_TOKEN` is not yet a repo secret, the user will provide it later, and live verification happens then — user's call, 2026-10-01.

## Boundaries & Constraints

**Always:** the analysis skill invocation is read-only (`Read Grep Glob` only, no `Edit`/`Write` tool) — the graph, not the agent, writes state files via `state_io.py` (mirrors AD-12's "script writes, not agent" precedent); `CLAUDE_CODE_OAUTH_TOKEN` is read automatically from the environment in normal (non-`--bare`) mode — never pass `--bare` (it skips skill auto-discovery and requires `ANTHROPIC_API_KEY`, contradicting AD-9); structured output via `--json-schema` (not free-text parsing); AD-10's exact frontmatter schema via `state_io.py write`, never hand-rolled.

**Never:** no round-counter, cap enforcement, or cap-out commit-comment posting (AD-13's loop mechanics — entry 4 owns this, builds on top of this ticket's single invocation); no `implementation_graph.py`/Job 2 work (entries 6-10); no deterministic pre-agent intake gate — CAP-1's validation is the skill's own first judgment, per the architecture's Capability map ("left to the analysis-stage skill prompt, not an AD"); no required story-file template/sections (per Decision above); no live dispatch in this ticket — `CLAUDE_CODE_OAUTH_TOKEN` isn't set yet, so build and unit-test everything, then defer the one live end-to-end run to `deferred-work.md` (same posture as entry 1's gate-protection gap).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Complete, in-scope, no open questions | Story file judged complete by the skill, `open_questions: []` | `plan.md` + `decisions.md` written via `state_io.py`, `status: ready-for-review` | n/a |
| Complete, open questions remain | Skill returns `complete: true`, non-empty `open_questions` | `plan.md` + `decisions.md` written, `status: awaiting-clarification`, questions carried in the body | n/a — entry 4 consumes this |
| Incomplete or out-of-scope | Skill returns `complete: false` or `in_scope: false` with a `reason` | Run halts with the reason printed; no `plan.md`/`decisions.md` written | Graph exits non-zero with the reason on stderr |
| Claude CLI invocation fails (non-zero exit, malformed JSON) | `subprocess` call errors or `--json-schema` validation fails | Graph halts loudly, no partial state file written | Distinguish from a legitimate "incomplete" verdict — this is a tooling failure, not an intake judgment |

</frozen-after-approval>

## Code Map

- `factory/scripts/state_io.py` -- entry 2's shared library; `write_state(path, story_slug=..., stage="analysis", status=..., body=...)` is the only way this ticket touches `.factory/` state files. `STATUS_BY_STAGE["analysis"]` already has `drafted`/`awaiting-clarification`/`ready-for-review` — use these verbatim, do not add new ones.
- `factory/graph/analysis_graph.py` -- new; LangGraph graph (single node for this ticket: invoke skill, parse, route to one of the three I/O Matrix outcomes). Entry 4 wraps this in a loop node later — keep the single-invocation call isolated in its own function so entry 4 can import and re-call it rather than duplicating the subprocess logic.
- `factory/graph/schemas/analysis_result.schema.json` -- new; the `--json-schema` passed to `claude -p`. Fields: `complete` (bool), `in_scope` (bool), `reason` (string, required when `complete`/`in_scope` is false), `proposal` (string, nullable), `subtasks` (array of strings), `tests` (array of strings), `open_questions` (array of strings).
- `.claude/skills/light-factory-analysis/SKILL.md` -- new; the analysis-stage skill prompt. Judges completeness/scope first (CAP-1), then — only if complete — proposes a solution, subtasks, tests, and any open questions it can't resolve from the story file + repo alone (CAP-2). Tool access: `Read`, `Grep`, `Glob` only.
- `.github/workflows/light-factory.yml` -- edit; `analysis` job's "Analysis stub" step is replaced with a real call to `factory/graph/analysis_graph.py`, passing `story-slug`, `run-id`, and the story file path; needs `CLAUDE_CODE_OAUTH_TOKEN` in `env:` (repo secret — not yet set; live dispatch deferred, see `deferred-work.md`) and `astral-sh/setup-uv@v10.2.0` already present for the `uv run` invocation; Node >=22 + the Claude Code CLI itself need installing (not yet present in this job — `npm install -g @anthropic-ai/claude-code@latest` or equivalent, after `actions/setup-node`).
- `stories/trivial-test-story.md` -- existing trigger fixture; minimal prose, no structured sections. Will be the smoke-test input for the deferred live dispatch.

## Tasks & Acceptance

**Execution:**
- [x] `.claude/skills/light-factory-analysis/SKILL.md` -- write the analysis-stage skill prompt (intake judgment, proposal, subtasks/tests, open questions; read-only) -- the agent half of CAP-1/CAP-2
- [x] `factory/graph/schemas/analysis_result.schema.json` -- write the JSON Schema for `--json-schema` -- makes the graph's parse deterministic, no free-text scraping
- [x] `factory/graph/analysis_graph.py` -- `run_analysis(story_file, story_slug, run_id)`: shells out to `claude -p` with the schema and allowlist, parses `structured_output`, routes to the three I/O Matrix outcomes via `state_io.py write` (or a clean halt) -- the orchestration half of CAP-1/CAP-2
- [x] `factory/graph/tests/test_analysis_graph.py` -- unit tests covering the I/O Matrix's four rows, with the `claude` subprocess call mocked (no live CLI/network dependency in unit tests) -- 14/14 pass
- [x] `.github/workflows/light-factory.yml` -- replace the `analysis` job's stub echo with the real invocation; add Node/Claude Code CLI setup and `CLAUDE_CODE_OAUTH_TOKEN` env wiring
- [x] Run `uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py` -- 14/14 passed (57/57 with entry 2's suite); live `gh workflow run` deferred to `deferred-work.md` until `CLAUDE_CODE_OAUTH_TOKEN` is provided

**Acceptance Criteria:**
- Given a story file the skill judges complete and in-scope with no open questions, when the analysis job runs, then `plan.md` and `decisions.md` exist under `.factory/<story-slug>/<run-id>/` with `status: ready-for-review`.
- Given a story file the skill judges incomplete or out-of-scope, when the analysis job runs, then it halts with the reason surfaced and no `plan.md`/`decisions.md` is written.
- Given the `claude` CLI invocation itself fails (non-zero exit or schema-validation failure), when the graph runs it, then the run halts loudly and is distinguishable from a legitimate incomplete/out-of-scope verdict.

## Implementation Notes

Built per plan: `.claude/skills/light-factory-analysis/SKILL.md` (read-only intake+analysis prompt, loose agent-driven judgment per the Decision above), `factory/graph/schemas/analysis_result.schema.json` (the `--json-schema` contract), `factory/graph/analysis_graph.py` (`invoke_skill`/`run_analysis` isolated from `build_graph`'s LangGraph wiring per the plan's Code Map note so entry 4 can re-call `run_analysis` directly), and `factory/graph/tests/test_analysis_graph.py` (14 tests covering all 4 I/O Matrix rows plus command-construction and CLI-exit-code checks, `claude` subprocess mocked throughout). `.github/workflows/light-factory.yml`'s `analysis` job now installs Node 22 + the Claude Code CLI and runs a real `analysis_graph.py` invocation in place of the stub echo, with `CLAUDE_CODE_OAUTH_TOKEN` wired from `secrets.*` (per the Decision above, live dispatch itself is deferred — see `deferred-work.md`).

The initial implementation subagent (first three files: SKILL.md, analysis_graph.py, schema) was repeatedly interrupted by the host machine sleeping mid-response — six consecutive interruptions, the last three producing zero further progress despite resuming it each time. Its work up to that point was reviewed and found correct and plan-consistent, so rather than keep resuming a stalled subagent, the orchestrator (not a subagent) wrote the remaining two files (`test_analysis_graph.py`, the workflow edit) directly and verified them.

**Unplanned fix — `.gitignore` scope.** `.claude/skills/` was blanket-ignored (intended for installed BMad skill packages), which also silently swallowed the new `.claude/skills/light-factory-analysis/` — a committed pipeline deliverable per the architecture's Namespace mapping, not a reinstallable package. Narrowed the rule to `.claude/skills/bmad*/` and `.claude/skills/bmod*/` so the existing BMad skills stay ignored (still reconstructable via `skills-lock.json`) while `light-factory-*` skills are tracked. Noted in passing: the existing `bmad-*`/`bmod-*` entries are symlinks (`.claude/skills/bmad-build -> ../../.agents/skills/bmad-build`), and gitignore's trailing-slash directory-only match never actually covered symlinks even before this change — pre-existing, unrelated to this ticket, left as-is.

## Plan Change Log

## Review Triage Log

- **Tasks & Acceptance checklist stale** — verdict: `low`. Verified: all six checkboxes read `- [ ]` despite Implementation Notes describing the work as fully built and tested. Same pattern as entry 1's and entry 2's review findings. Smallest fix is correcting the checkboxes to match reality (no code touched); routed `patch`, applied directly above.
- No other findings survived verification. The dispatched Quick review lens subagent never returned (two check-ins over ~2 hours went unanswered, consistent with the same host-machine-sleep pattern that repeatedly interrupted the step-03 implementation subagent on this ticket). Rather than wait indefinitely, the orchestrator conducted the Quick review directly: re-read the plan, the architecture spine (AD-5, AD-6, AD-9, AD-10, AD-12, AD-13, Capability map), and the full diff; checked every Always/Never rule and all three acceptance criteria against the code; and directly smoke-tested the one path the unit suite doesn't exercise (`build_graph()`, confirmed it compiles — `uv run --with "langgraph>=1.2.12,<2" python3 -c "...build_graph()..."` → `CompiledStateGraph`) and the JSON Schema's own validity (`jsonschema.Draft7Validator.check_schema` + a sample validation, both passed). No unmet acceptance criteria, broken Always/Never rules, or bugs found beyond the checklist item above.

## Design Notes

**CLI invocation shape** (verified against current official docs, not training-data recall): `claude -p "/light-factory-analysis <story-file-path>" --output-format json --json-schema '<schema>' --allowedTools "Read Grep Glob" --permission-prompts none`, run from the repo root (so the skill auto-discovers) with `CLAUDE_CODE_OAUTH_TOKEN` already in the environment. Do **not** use `--bare` — it skips skill auto-discovery entirely and requires `ANTHROPIC_API_KEY` instead of the OAuth token, which would silently violate AD-9. The response JSON's `structured_output` field holds the schema-validated payload; `result` holds the raw final text (log it, don't parse it). Skill invocation is by literal `/skill-name` text in the prompt — there is no separate CLI flag for it; this is the same convention this repo's own bmad skills already use.

**Why the graph writes state, not the agent:** giving the analysis invocation zero write/edit tools is stricter than per-path `Edit` scoping and sidesteps trusting the CLI's path-scoping syntax under adversarial story-file content. It also directly mirrors AD-12's already-adopted precedent (a deterministic script opens the PR, not the agent) rather than introducing a second permission model for this ticket alone.

**Why entry 4 isn't duplicated here:** the ticket's own `verify` text names exactly two tested outcomes (ready-for-review happy path, halt-on-incomplete) and the epic's breakdown lists "Bounded clarification loop" as a separate, later entry (`after: [3]`) covering CAP-2's loop/cap half. This ticket still has to produce the `awaiting-clarification` state (otherwise entry 4 has nothing to loop on), but the retry/cap/cap-out-comment logic itself is out of scope here.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/test_analysis_graph.py` -- expected: all pass, `claude` subprocess call mocked
- `uv run --with pyyaml python3 -c "import yaml; yaml.safe_load(open('.github/workflows/light-factory.yml'))"` -- expected: `YAML OK`
- `gh workflow run light-factory.yml -f story_file=stories/trivial-test-story.md` then `gh run view <run-id> --log` -- **run live 2026-10-02** (run `36970131400`), once the user set `CLAUDE_CODE_OAUTH_TOKEN` as a repo secret: the CLI invocation, skill dispatch, and structured-output parse all worked end-to-end; the `analysis` job halted cleanly (exit 1) with reason "The story is an explicit placeholder used only to trigger and verify the light-factory.yml pipeline skeleton ... there is nothing to design a solution from" -- the correct `AnalysisHalted` outcome for this fixture (CAP-1 judged it in-scope but not actionable), matching the halt-on-incomplete branch already covered by unit tests. No `plan.md`/`decisions.md` written, as expected for a halt.

**Manual checks (if no CLI):**
- Read the written `plan.md`/`decisions.md` frontmatter and confirm it matches AD-10's schema exactly (no extra/renamed fields).

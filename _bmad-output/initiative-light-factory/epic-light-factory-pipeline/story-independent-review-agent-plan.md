---
title: 'Independent review agent'
type: 'feature'
ticket: '9'
created: '2026-10-02'
status: 'built'
baseline_revision: 'f376699203f1359bb445b55f8db61e7a2ec2514e'
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

**Problem:** CAP-6 (independent review) is unbuilt. Job 2 ends after ticket 8's mechanical checks with no judgment-level evaluation of the implementation agent's actual work against the plan and acceptance criteria.

**Approach:** Add `.claude/skills/light-factory-review/` (Read, Grep, Glob only — no Write/Edit tool at all, mirrors `light-factory-analysis`'s model) and `factory/graph/review_graph.py` (mirrors `analysis_graph.py`'s shape: `--json-schema` structured output against a new `review_result.schema.json`). Wired as a new "Run review" step in Job 2 right after "Security check." Writes `review.md` (status `resolved` when clean, `findings-open` otherwise — AD-10's existing enum) via `state_io.write_state`, plus the raw findings to `evidence/review/findings.json` (AD-8's evidence split) for ticket 11's evidence-approval summary to read later.

## Boundaries & Constraints

**Always:** the skill's invocation grants no Write/Edit/Bash/git/gh tool at all — AD-5's first layer is "no tool to violate," not a deny-rule carve-out (stronger than ticket 7's Edit-scoped case, since review needs zero mutation capability); review reads `plan.md`/`decisions.md` (for the proposal and acceptance criteria) and explores the checked-out branch's actual files via Read/Grep/Glob; `review.md` status is `resolved` when `findings` is empty, `findings-open` otherwise (AD-10's existing enum, no new status invented); raw findings are also written to `evidence/review/findings.json` (AD-8).

**Never:** no fix-loop or counter logic (ticket 10's scope); no write to `plan.md`/`decisions.md` (AD-10 — this entry only writes `review.md` + `evidence/review/`); no change to the mechanical-checks steps (ticket 8, untouched); a review that produces findings is a legitimate outcome, not a failure — only the `claude` CLI invocation itself failing fails this step.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Clean implementation | Skill returns empty `findings` | `review.md` status `resolved`; `evidence/review/findings.json` has an empty `findings` array; step exits 0 | n/a |
| Implementation has findings | Skill returns non-empty `findings` | `review.md` status `findings-open`, listing each finding; `evidence/review/findings.json` carries the same raw findings; step exits 0 | n/a — a legitimate outcome, not a failure |
| `claude` CLI invocation itself fails | Non-zero exit / malformed output | Raises `ReviewInvocationError`; no `review.md`/evidence written | Distinct from both outcomes above; step exits non-zero |

</frozen-after-approval>

## Code Map

- `factory/graph/schemas/review_result.schema.json` -- new. `findings`: array of `{location: string, description: string}` (mirrors `analysis_result.schema.json`'s style); required, empty array = clean pass.
- `.claude/skills/light-factory-review/SKILL.md` -- new. Tools: Read, Grep, Glob only (mirrors `light-factory-analysis`'s "no tool for it" framing). Invoked as `/light-factory-review <plan-path> <decisions-path>`; reads the plan's proposal/subtasks for acceptance criteria, explores the checked-out branch's actual files, evaluates the implementation against them — never re-judges the original story file (ticket 3's concern, not this one's).
- `factory/graph/review_graph.py` -- new. Mirrors `analysis_graph.py`'s shape exactly: `_build_command` (`--allowedTools "Read Grep Glob"`, `--json-schema` against the new schema, `--permission-prompts none`); `invoke_skill` (raises `ReviewInvocationError` on tooling failure); `run_review(story_slug, run_id, *, claude_bin="claude", state_base=state_io.FACTORY_DIR, cwd=None) -> dict` reads `plan.md`/`decisions.md` paths from `state_io.state_dir`, invokes the skill, writes `review.md` via `state_io.write_state(stage="review", status=...)` and the raw findings to `evidence/review/findings.json` via `state_io.write_atomic`; `build_graph()`/`main()` CLI pair.
- `.github/workflows/light-factory.yml` -- edit Job 2: add one "Run review" step after "Security check (placeholder)", `uv run factory/graph/review_graph.py --story-slug "${{ needs.analysis.outputs.story-slug }}" --run-id "${{ needs.analysis.outputs.run-id }}"` with `CLAUDE_CODE_OAUTH_TOKEN` env (same pattern as Job 1's "Run analysis" / ticket 7's "Run implementation").
- `factory/graph/tests/test_review_graph.py` -- new, covering the I/O Matrix, `subprocess.run` mocked (same pattern as `test_analysis_graph.py`).

## Tasks & Acceptance

**Execution:**
- [ ] `factory/graph/schemas/review_result.schema.json` -- new schema
- [ ] `.claude/skills/light-factory-review/SKILL.md` -- new skill, Read/Grep/Glob only
- [ ] `factory/graph/review_graph.py` -- add `invoke_skill`, `run_review`, `build_graph`, `main`
- [ ] `.github/workflows/light-factory.yml` -- wire the "Run review" step into Job 2
- [ ] `factory/graph/tests/test_review_graph.py` -- new tests per the I/O Matrix
- [ ] Run `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- all pass

**Acceptance Criteria:**
- Given the review agent's Claude Code invocation, when its `--allowedTools` is inspected, then it carries no Write/Edit/Bash/git/gh tool at all.
- Given a clean implementation, when review runs, then `review.md` status is `resolved` and `evidence/review/findings.json`'s `findings` array is empty.
- Given findings, when review runs, then `review.md` status is `findings-open`, listing each finding, and `evidence/review/findings.json` carries the same raw findings.

## Implementation Notes

## Plan Change Log

## Review Triage Log

- **Quick lens, 2026-10-02: no findings.** Verified against all three acceptance criteria, the I/O Matrix, Boundaries & Constraints, and the Code Map; cross-checked against the mirror files (`analysis_graph.py`, both prior skills, `test_analysis_graph.py`) for consistency; ran the real test suite (122 passed). Confirmed `--allowedTools` is literally `Read Grep Glob` with no `--bare`, both status values are in AD-10's existing enum, no write to `plan.md`/`decisions.md` anywhere, mechanical-checks steps unchanged. One non-blocking observation noted (no `ensure_layout` call — harmless, `write_atomic` creates parent dirs itself and Job 1 already created the tree). No loopback triggered.

## Design Notes

**Why findings are `{location, description}` objects, not bare strings:** ticket 10's fix loop will need to re-engage a fix against a specific location, the same way `bmad-build`'s own review step cites file/line evidence — a bare string would force that ticket to re-parse prose. This is cheap to do now and avoids churn later.

**Why `review.md` writes `resolved`/`findings-open` directly, never an intermediate `in-review`:** mirrors `analysis_graph.py`'s own pattern — `plan.md`/`decisions.md` go straight to `ready-for-review`/`awaiting-clarification`, never a transient "analyzing" status. `in-review` in AD-10's enum is for a state that persists across multiple steps (e.g. mid-fix-loop); a single completed invocation has no such intermediate state to represent.

**Why `evidence/review/findings.json` duplicates what `review.md` already says:** AD-8 names `evidence/review/` specifically for "the independent review agent's findings/metrics," distinct from `review.md`'s own per-stage-ownership role (AD-10). `review.md` is the stage's source of truth for status; `evidence/review/` is the machine-readable form ticket 11's evidence-approval summary reads later, without needing to parse `review.md`'s prose body.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass

**Manual checks (if no CLI):**
- Inspect the "Run review" workflow step's `--allowedTools` flag directly for the no-write-tool acceptance criterion.

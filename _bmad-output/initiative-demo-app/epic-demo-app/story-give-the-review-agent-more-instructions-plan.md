---
title: 'Give the review agent more instructions'
type: 'chore'
ticket: '10'
created: '2026-10-11'
status: done
baseline_revision: 'dc8b3f62d9c52fb6dda785e1bab6baf0ed4103dc'
route: 'oneshot'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The bounded fix loop (CAP-7, AD-11) has never engaged on a live run — every run so far finished review with 0 findings — so initiative Done-when 3 is unproven for it.

**Approach:** Live dispatches of real stories against `senacor3/software-factory-demo` until one run's review raises a finding and the fix loop runs at least one cycle within its cap of 2. The first story is the checks-weakening guard from `deferred-work.md`, written as `stories/read-checks-config-from-target-branch.md` (user's choice, 2026-10-11): a real feature with code, tests, and several document updates, so a first pass can plausibly miss one. If a run ends with 0 fix cycles, further stories are tried until a finding appears (user's choice, 2026-10-11). Findings are never seeded: no story tells an agent to leave something out, and agents are not steered mid-run. I draft each story for the human's approval, dispatch, monitor, and report; every gate decision is the human's own action. No pipeline code is changed by hand; a defect found live becomes a `deferred-work.md` entry unless the human authorizes a fix in-session.

**Renegotiated by the human, 2026-10-11:** stopped after two attempts with 0 fix cycles and moved to `epic-demo-app` as entry 10. On resume the work has two parts: first give the review agent more instructions (an authored change to `.claude/skills/light-factory-review/SKILL.md`, which replaces the "no pipeline code is changed by hand" rule for that file only), then run real freight-tenders stories until the loop engages. Which instructions to add is decided with the human when the entry is refined.

**Renegotiated again by the human, 2026-10-11:** the fix loop engaged live on the pipeline itself before this entry started (run `38150142797` (`stories/one-input-path-per-story-slug.md`, PR #12, merged as `c60279b`): the first review found two CLI tests the plan listed and the implementer had not written; one fix cycle added them; the second review was clean; `fix_cycle: 1`). The entry is narrowed to the first part only — extending the review agent's instructions — and retitled. Its live check is now that a run on a freight-tenders story shows the review applying the new instructions.

**Renegotiated again by the human, 2026-10-12:** which instructions to add is settled — one skill, not two agents (considered and rejected a separate "technical quality" reviewer: no permission/context reason to split, and the epic's one pipeline-logic exception was scoped to editing this one file, not to standing up a second graph-invoked agent). `.claude/skills/light-factory-review/SKILL.md` gains a new Step 3, alongside the existing plan-conformance Step 2: judge the implementation's technical quality and its accordance with this repo's agent instructions (`AGENTS.md`/`CLAUDE.md`, read generically if present — not specific rules text baked into the prompt), explicitly excluding anything the mechanical `build`/`test`/`lint`/`security` checks already catch. `factory/graph/schemas/review_result.schema.json`'s `findings` descriptions were reworded to match (no structural change — `review_graph.py`/`fix_loop_graph.py` are untouched and need no change, findings of either kind flow through the same array). Prerequisite work, done first: root + `freight-tenders/backend` + `freight-tenders/frontend` each got an `AGENTS.md` via `bmad-project-context`, adapted from the human's reference harness (a different stack) rather than copied — so Step 3 has real conventions to check the demo app against. Committed as `bc6cb2a` (`AGENTS.md`s + a backend error-shape retrofit) and a second commit for the `SKILL.md`/schema change. Remaining: dispatch a real freight-tenders story through the pipeline and confirm `review.md` shows Step 3 actually applying — a finding (or an explicit clean pass) that cites `AGENTS.md` or a quality point, not just plan-conformance. That dispatch is a live, hard-to-reverse pipeline run (opens a PR, runs CI) and needs the human's go-ahead before it's triggered.

</frozen-after-approval>

## Implementation Notes

Oneshot: the authored content is one story file per attempt plus this plan; the rest is dispatching and observing.

**2026-10-12:** `.claude/skills/light-factory-review/SKILL.md` — added Step 3 (technical quality + `AGENTS.md`/`CLAUDE.md` accordance, explicitly excluding what the mechanical checks already catch) and reworded the frontmatter `description` and the `Output` section to cover both steps. `factory/graph/schemas/review_result.schema.json` — reworded `findings`'s and its items' `description` fields to stop saying "against the plan's acceptance criteria" exclusively (text only; schema shape, `review_graph.py`, and `fix_loop_graph.py` are unchanged — verified via the full test suite, still 288 passed, and `ruff check factory/` clean). Prerequisite: ran `bmad-project-context` to set up `AGENTS.md` at the repo root and in `freight-tenders/backend`/`freight-tenders/frontend`, filtered hard against a human-supplied reference harness from an unrelated project (different stack — most of its stack-specific rules didn't apply or conflicted with this already-shipped codebase; kept only what's portable or what the human explicitly chose to adopt). Also retrofitted the backend's error-response shape (`{error, message, path, timestamp}`) as part of that AGENTS.md work, since the human approved doing so immediately rather than just documenting it (verified: `mvn -B verify` 25/25 tests pass, `mvn spotless:check` clean after one `spotless:apply` fix). Both committed (`bc6cb2a`, then the `SKILL.md`/schema change at `9442760`).

**Live dispatch (2026-10-12):** drafted and dispatched `stories/validate-tender-creation-input.md` (run `38258449451`, PR #13) — a real, non-seeded story (add Bean Validation to `CreateTenderRequest`, motivated by the backend `AGENTS.md`'s own documented gap). Neither `plan-approval` nor `evidence-approval` paused for a manual click in this environment (no required reviewers configured on those Environments) — an existing gap, not caused by this change. The `checks` job's `Lint check` failed first: the implementation agent relocated the existing `closeTenderReturns200WithClosedTender` test and dropped a space before `throws` in the process — a genuine, unseeded formatting slip, caught exactly as `spotless:check` is designed to. Pushed a one-line fix directly to the PR's branch (`81a228b`) and re-ran the `Checks` job; it, `Review & fix loop`, and `Merge` all then passed, and PR #13 merged as `f311628`.

**Result is inconclusive on the one thing it was meant to prove:** `review.md` came back `status: resolved`, `findings: []` — a clean pass. This cannot be told apart from "Step 3 ran and found nothing" versus "Step 3 wasn't meaningfully engaged with" — the `claude` CLI's `--output-format json` mode returns only the final structured output, no tool-call transcript, and the GitHub Actions job log has no visibility into what the agent actually read. This mirrors the epic's own prior history (multiple 0-finding attempts before the fix loop's eventual live engagement came from an unplanned run) — a clean pass is a legitimate, valid outcome of the review, not evidence the instructions are broken, but it is not proof Step 3 specifically fired either.

Design choice in the first story, made while drafting and put to the human with the story: of the three options the deferred entry names, it takes "read the checks config from the target branch". Denying the agent writes to `.github/` and `factory/` would block legitimate stories (this one included), and flagging in the summary alone prevents nothing. The story prescribes a separate `_read_target_config` function with a working-tree fallback so the existing tests, which mock `subprocess.run` wholesale, keep passing — the implementation agent has no shell and cannot run them.

Risk to this ticket's goal: if the implementation breaks a test, `Checks` fails and the run stops before review, so the loop cannot engage on that run.

Attempts, on `senacor3/software-factory-demo`, 2026-10-11. Every gate decision was the human's own action.

- **Attempt 1 -- run `38147061301`, `stories/read-checks-config-from-target-branch.md`: 0 fix cycles.** Analysis resolved with no question (PR #9); after `plan-approval`, `Implementation`, `Checks`, and `Review & fix loop` succeeded; review `resolved`, 0 findings, `fix_cycle: 0`. The implementer missed nothing across two scripts, two test files, and three documents, so breadth alone did not produce a finding. The human approved `evidence-approval`; merged as `d28e700`. The feature works on the runner: the evidence summary shows `config: origin/main`. This resolves the checks-weakening entry in `deferred-work.md`. Local `main` after the pull: 266 tests pass, lint clean.
- **Attempt 2 -- run `38148260661`, `stories/distinct-exit-code-for-status-output-failure.md`** (user's choice, 2026-10-11): 0 fix cycles. The low finding rejected in ticket 3.2's review. The analysis plan spelled out both points a first pass might have slipped on (no stdout line on the failure path; exit codes for every failure case in the docstring), and the implementer followed it. Review `resolved`, 0 findings. Approved and merged as `eabd472` (PR #10). Local `main` after the pull: 269 tests pass.

Stopped here and moved (user's call, 2026-10-11). What the two attempts, and the four live runs before them, suggest: the loop can only engage on a deviation from the plan that no test catches, because a functional mistake fails a check and stops the run before review, and the plans have been explicit enough to leave the implementer nothing to interpret. The review skill also limits itself to the plan's subtasks. Ideas for the resumed entry, none decided: widen the review agent's remit (behavior and edge cases beyond the subtasks, adequacy of the tests); a story that needs a file removed or renamed, which the implementation agent cannot do with Read/Write/Edit/Grep/Glob -- that would likely end at the cap with `unresolved-after-cap` and expose the missing delete capability.

The plan's status is back to `draft`: the intent changed, so planning resumes from here when entry 10 starts.

What the engaging run adds to the picture above: the finding was a deviation from the plan that no test could catch — missing tests. The analysis plan listed tests the story had not asked for, and the implementer skipped two of them. That is the kind of gap the current review instructions already catch; the open question for this entry is what they do not ask for.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 0, medium: 1, low: 0, false: 0, maybe-false: 0

- Step 3's wording ("every directory the diff touches") asked the review skill to use a boundary it has no tool to enumerate — `--allowedTools` is `Read Grep Glob` only, no git/Bash, confirmed in `review_graph.py`'s `_build_command` (unchanged by this diff) — **medium**, confirmed. Not unsafe (read-only judgment work), but would cause a silent, inconsistent miss of a directory's `AGENTS.md` whenever `plan.md` doesn't name every touched path. Route: patch — reworded Step 3 to ground the check in what the agent can actually see (`plan.md`'s own references, and what `Grep`/`Glob` surfaced during Step 2's own exploration) instead of "the diff."

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass (confirms the schema/skill wording change caused no code regression)
- `uv run --with ruff ruff check factory/` -- expected: clean

**Manual checks (if no CLI):**
- Dispatch a real freight-tenders story through the pipeline; `review.md` or `evidence/review/findings.json` shows a finding (or an explicit clean pass) distinguishable as Step 3's own — citing `AGENTS.md`/`CLAUDE.md` or a technical-quality point, not just plan-conformance — proof the new instructions were actually applied, not just authored.

---
title: 'Closing end-to-end suite'
type: 'feature'
ticket: '13'
created: '2026-10-10'
status: 'in-progress'
baseline_revision: '68e7681f6ded0d849b9db19af641b48fa6276678'
route: 'oneshot'
route_source: 'auto'
review: ''
review_source: ''
lenses_ran: []
review_loop_iteration: 0
context: ['_bmad-output/initiative-light-factory/deferred-work.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Entries 1-12 built the pipeline piece by piece, each verified by unit tests and (mostly) static review — no real story has ever gone through the whole thing end to end with real agents, real gates that actually pause, and a real merge. The spec's own Success signal is unproven live.

**Approach:** Not a code-authoring ticket — a live operational run. This plan's "implementation" is: (1) write one real, complete, in-scope story file (`stories/wire-ruff-lint.md`, already decided: real `ruff` lint tooling for `run_checks.py`'s `run_lint` placeholder) and push it to `senacor3/software-factory-demo`'s `main`; (2) dispatch `light-factory.yml` against it via `gh workflow run`; (3) watch Job 1 (analysis) run for real and reach the `plan-approval` gate; (4) **the human (not me) reviews the plan-approval PR comment and approves or rejects it** — this is the whole point of CAP-3, and an AI approving its own pipeline's gate would defeat the demonstration; (5) watch Job 2 (implementation → checks → review → bounded fix loop if needed) run for real; (6) **the human reviews the evidence-approval PR comment and approves or rejects it**; (7) watch Job 3 merge for real. My role throughout is to dispatch, monitor, report each gate's summary clearly when it's reached, and verify the final state — never to click approve myself.

## Boundaries & Constraints

**Always:** every gate approval is a real action taken by the human, in the GitHub UI or via their own `gh` command — I report what's waiting and why, never approve on their behalf. The story file is genuinely complete and in-scope (a real improvement to `run_checks.py`, not throwaway content) — chosen from `deferred-work.md`'s own already-specified `ruff`-lint item. If the fix loop engages, I observe and report it — I do not intervene in or redirect what the implementation/review agents do mid-run. If a step fails for a reason unrelated to the pipeline itself (e.g. my own `gh`/monitoring commands), I say so plainly rather than treating it as a pipeline defect.

**Never:** I never submit a deployment-review approval or rejection via `gh api`/`gh run review` or any other automated path — that action is reserved for the human throughout this run. No code changes to the pipeline itself as part of this ticket (any real pipeline bug discovered live is a `deferred-work.md` entry or a follow-up ticket, not a mid-run patch).

</frozen-after-approval>

## Implementation Notes


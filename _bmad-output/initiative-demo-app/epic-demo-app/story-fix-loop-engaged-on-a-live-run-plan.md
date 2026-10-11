---
title: 'Fix loop engaged on a live run'
type: 'chore'
ticket: '10'
created: '2026-10-11'
status: 'draft'
baseline_revision: 'dc8b3f62d9c52fb6dda785e1bab6baf0ed4103dc'
route: 'oneshot'
route_source: 'auto'
review: ''
review_source: ''
lenses_ran: []
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The bounded fix loop (CAP-7, AD-11) has never engaged on a live run — every run so far finished review with 0 findings — so initiative Done-when 3 is unproven for it.

**Approach:** Live dispatches of real stories against `senacor3/software-factory-demo` until one run's review raises a finding and the fix loop runs at least one cycle within its cap of 2. The first story is the checks-weakening guard from `deferred-work.md`, written as `stories/read-checks-config-from-target-branch.md` (user's choice, 2026-10-11): a real feature with code, tests, and several document updates, so a first pass can plausibly miss one. If a run ends with 0 fix cycles, further stories are tried until a finding appears (user's choice, 2026-10-11). Findings are never seeded: no story tells an agent to leave something out, and agents are not steered mid-run. I draft each story for the human's approval, dispatch, monitor, and report; every gate decision is the human's own action. No pipeline code is changed by hand; a defect found live becomes a `deferred-work.md` entry unless the human authorizes a fix in-session.

**Renegotiated by the human, 2026-10-11:** stopped after two attempts with 0 fix cycles and moved to `epic-demo-app` as entry 10. On resume the work has two parts: first give the review agent more instructions (an authored change to `.claude/skills/light-factory-review/SKILL.md`, which replaces the "no pipeline code is changed by hand" rule for that file only), then run real freight-tenders stories until the loop engages. Which instructions to add is decided with the human when the entry is refined.

</frozen-after-approval>

## Implementation Notes

Oneshot: the authored content is one story file per attempt plus this plan; the rest is dispatching and observing.

Design choice in the first story, made while drafting and put to the human with the story: of the three options the deferred entry names, it takes "read the checks config from the target branch". Denying the agent writes to `.github/` and `factory/` would block legitimate stories (this one included), and flagging in the summary alone prevents nothing. The story prescribes a separate `_read_target_config` function with a working-tree fallback so the existing tests, which mock `subprocess.run` wholesale, keep passing — the implementation agent has no shell and cannot run them.

Risk to this ticket's goal: if the implementation breaks a test, `Checks` fails and the run stops before review, so the loop cannot engage on that run.

Attempts, on `senacor3/software-factory-demo`, 2026-10-11. Every gate decision was the human's own action.

- **Attempt 1 -- run `38147061301`, `stories/read-checks-config-from-target-branch.md`: 0 fix cycles.** Analysis resolved with no question (PR #9); after `plan-approval`, `Implementation`, `Checks`, and `Review & fix loop` succeeded; review `resolved`, 0 findings, `fix_cycle: 0`. The implementer missed nothing across two scripts, two test files, and three documents, so breadth alone did not produce a finding. The human approved `evidence-approval`; merged as `d28e700`. The feature works on the runner: the evidence summary shows `config: origin/main`. This resolves the checks-weakening entry in `deferred-work.md`. Local `main` after the pull: 266 tests pass, lint clean.
- **Attempt 2 -- run `38148260661`, `stories/distinct-exit-code-for-status-output-failure.md`** (user's choice, 2026-10-11): 0 fix cycles. The low finding rejected in ticket 3.2's review. The analysis plan spelled out both points a first pass might have slipped on (no stdout line on the failure path; exit codes for every failure case in the docstring), and the implementer followed it. Review `resolved`, 0 findings. Approved and merged as `eabd472` (PR #10). Local `main` after the pull: 269 tests pass.

Stopped here and moved (user's call, 2026-10-11). What the two attempts, and the four live runs before them, suggest: the loop can only engage on a deviation from the plan that no test catches, because a functional mistake fails a check and stops the run before review, and the plans have been explicit enough to leave the implementer nothing to interpret. The review skill also limits itself to the plan's subtasks. Ideas for the resumed entry, none decided: widen the review agent's remit (behavior and edge cases beyond the subtasks, adequacy of the tests); a story that needs a file removed or renamed, which the implementation agent cannot do with Read/Write/Edit/Grep/Glob -- that would likely end at the cap with `unresolved-after-cap` and expose the missing delete capability.

The plan's status is back to `draft`: the intent changed, so planning resumes from here when entry 10 starts.

## Plan Change Log

## Review Triage Log

## Verification

**Manual checks (if no CLI):**
- The run's `review.md` frontmatter shows `fix_cycle` of 1 or 2, and the run reaches `evidence-approval`.
- The run branch shows the fix cycle's commit(s) after the first review.

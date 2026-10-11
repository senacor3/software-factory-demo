---
title: 'Closing end-to-end suite'
type: 'chore'
ticket: '7'
created: '2026-10-11'
status: 'built'
baseline_revision: '7abcb19ba2a174f68014c9e1431b6ca9ba9e8c65'
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

**Problem:** Entries 2, 4, 5 and 8 of this epic were verified by unit tests only. The bounded clarification loop, AD-15 supersession, the reject-closes-PR job for both gates, and the six-job pipeline's evidence commits have never run live.

**Approach:** Not a code-authoring ticket — a live operational run against `senacor3/software-factory-demo`, driven by one real story (`stories/validate-story-file-location.md`: make `derive_story_slug` reject story files outside `stories/`; user's choice, 2026-10-11). Four dispatches (user's choice, 2026-10-11 — no final merge run):

1. **Clarification halt.** The story's first version leaves one decision open. Expected: `awaiting-clarification`, PR labeled `clarification-round`, commented, closed.
2. **Answered re-trigger.** The story is edited to answer the question and re-dispatched. Expected: the count sees one prior round, analysis resolves, a new PR stays open, the run pauses at `plan-approval`.
3. **Supersession, then reject at `plan-approval`.** Re-dispatched unchanged. Expected: run 2 is cancelled, its PR closed with "Superseded by #N", the new PR carries "Retry of #M". The human rejects the gate; `close-rejected-pr` closes the PR with a comment naming gate and reviewer.
4. **Reject at `evidence-approval`.** Re-dispatched; the human approves `plan-approval`; `implementation`, `checks`, `review` run, each later job committing its evidence; the human rejects `evidence-approval`; the PR is closed with a comment.

I push the story file to `main`, dispatch, monitor, report what each gate is waiting on, and verify the end state of each run. Every gate approval or rejection is the human's own action — I never submit a deployment review. No pipeline code changes in this ticket: a defect found live becomes a `deferred-work.md` entry unless the human authorizes a fix in-session. Agents are not steered mid-run; if one behaves differently from the script above (asks again, halts at intake, a check fails), I report it and the human decides how to continue.

</frozen-after-approval>

## Implementation Notes

Oneshot: the only authored content is one story file; everything else is dispatching and observing, as with epic 1's entry 13.

Known going in (re-parked in entry 6): a clarification-halted run still pauses at `plan-approval`. Run 1 will sit at that gate until run 2's dispatch cancels it through the concurrency group — no reject needed.

Also to observe, carried from entries 4, 5, 8: `close-rejected-pr`'s run condition, gate expression and `actions: read` scope; separate evidence commits from `checks` and `review`.

Results, all on `senacor3/software-factory-demo`, 2026-10-11, story `stories/validate-story-file-location.md`. Every gate decision was the human's own action.

- **Run 1 (`38140686643`) — clarification halt.** Analysis returned the one open question the story left open. PR #4 labeled `clarification-round`, commented with the question, closed. The run then paused at `plan-approval` (the re-parked dangling gate) and was cancelled by run 2's dispatch.
- **Run 2 (`38140757607`) — answered re-trigger.** Story edited to answer (sub-folders rejected, commit `09e2d7c`). Analysis resolved; PR #5 open, unlabeled, "Plan ready for review"; paused at `plan-approval`.
- **Run 3 (`38140846697`) — supersession, reject at `plan-approval`.** Run 2 cancelled by the concurrency group; PR #5 closed with "Superseded by #6"; PR #6 carries "Retry of #5". After the reject: `Implementation` `failure` with no steps, `Checks`/`Review & fix loop`/`Merge` skipped, `Close PR on gate reject` ran and closed PR #6 with a comment naming the gate and reviewer and quoting the review comment. No label.
- **Run 4 (`38141347400`) — reject at `evidence-approval`.** `plan-approval` approved; `Implementation`, `Checks`, `Review & fix loop` succeeded as separate jobs; the run branch shows one commit per job (`Analysis`, `Implementation`, `Checks`, `Review`); evidence summary posted (build/test/lint pass, security skipped, review resolved, 0 findings, 0 fix cycles). After the reject: `Merge` `failure`, `Close PR on gate reject` closed PR #7 with a comment naming `evidence-approval`; the review history's `approved` entry for `plan-approval` did not confuse it. PR #7 had no "Retry of" comment, correctly, since #6 was already closed.

No pipeline defect surfaced and no pipeline code was changed. No open PR remains; all four run branches are left in place.

Not shown by this suite: the fix loop engaging (0 cycles used; the loop demonstrated is the clarification loop, one round of two); the clarification cap being reached; the six-job pipeline merging (no final merge run, user's choice) — so the story's change is not on `main` and the concurrency-key finding stays open in `deferred-work.md`; `close-rejected-pr` staying off after a `checks` failure (no check failed); and the two `gh`-behaviour questions carried from entries 4 and 5 (closing an already-closed PR, a stale `rejected` entry across a re-run), which no run exercised.

Review: the authored diff is one story file plus this plan; read inline by the implementing session (no subagents, as for entry 6), no findings.

## Plan Change Log

## Review Triage Log

## Verification

**Manual checks (if no CLI):**
- Per run: `gh run view`, `gh pr view --comments`, PR state and labels, and the run branch's commit list match the expectation above.

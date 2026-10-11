---
title: 'Merge the story-file-location story through the pipeline'
type: 'chore'
ticket: '3'
created: '2026-10-11'
status: done
baseline_revision: '621ad6a126698423a9bbd7d6342801ee92b1add2'
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

**Problem:** `stories/validate-story-file-location.md` was dispatched four times in ticket 2.7 and never merged, so `derive_story_slug` still accepts story files outside `stories/` on `main`, the concurrency-key finding in `deferred-work.md` stays open, and the six-job pipeline has never merged anything.

**Approach:** Not a code-authoring ticket — one live dispatch of that story, unchanged, against `senacor3/software-factory-demo`, taken to merge. I dispatch, monitor, report what each gate is waiting on, and verify the end state. Both gate decisions are the human's own action; I never submit a deployment review. Agents are not steered mid-run: if the run does something else (asks a clarification question, a check fails, the review finds something), I report it and the human decides. No pipeline code is changed here; a defect found live becomes a `deferred-work.md` entry unless the human authorizes a fix in-session. After the merge, a dispatch for a story file outside `stories/` confirms it is rejected.

</frozen-after-approval>

## Implementation Notes

Oneshot: nothing is authored except this plan; the work is dispatching and observing, as with tickets 1.13 and 2.7.

Going in: the story has one prior `clarification-round` PR (#4), so one round of the cap of 2 is spent. This is also the first runner use of ticket 3.1's checks config (`.github/post-implementation-checks.yml`, PyYAML via `uv`) and of ticket 3.2's `status` job output on a clean run.

Results, on `senacor3/software-factory-demo`, 2026-10-11. Both gate decisions were the human's own action.

- **Run `38146170332` -- to merge.** Dispatched on `main` at `621ad6a`. Analysis resolved with no clarification question, opened PR #8 unlabeled, posted "Plan ready for review", and the run paused at `plan-approval` -- the clean-story half of ticket 3.2's live proof (the `status` output let a `ready-for-review` run reach the gate). After approval, `Implementation`, `Checks`, and `Review & fix loop` succeeded as separate jobs, one commit each on the run branch. Evidence summary: build/test/lint pass, security skipped, review resolved, 0 findings, 0 fix cycles. After approval of `evidence-approval`, `Merge` squash-merged PR #8 as `5f56b5f`; `Close PR on gate reject` was skipped. This is the six-job pipeline's first merge.
- **Ticket 3.1 on a runner.** `evidence/checks/test.json` records the command from `.github/post-implementation-checks.yml` (with `--with pyyaml`), and `security.json` records `skipped` with "no command configured for this check".
- **The merged change.** `derive_story_slug` in `factory/scripts/state_io.py` raises `ValueError` when the file's immediate parent is not `stories` (+9 -3, tests +27). Pulled to the local `main`; 253 tests pass.
- **Run `38146620264` -- misplaced story file.** Dispatched with `story_file=other/foo.md`. `Analysis` failed in "Derive story-slug and run-id" with `error: story file 'other/foo.md' must live directly in a 'stories/' directory` (exit 2); every other job was skipped and no PR was opened.

No pipeline defect surfaced and no pipeline code was changed by hand. No open PR remains.

Not shown: the fix loop engaging (0 cycles, entry 4's subject), and ticket 3.2's halted-run half -- this story did not ask a clarification question, so no run yet shows a halt ending without the `plan-approval` gate.

Review: the only authored content is this plan; read inline by the implementing session, no review lens launched, no findings.

## Plan Change Log

## Review Triage Log

## Verification

**Manual checks (if no CLI):**
- `gh run view`: all of Analysis, Implementation, Checks, Review & fix loop, Merge succeed; Close PR on gate reject is skipped.
- The PR is merged, and `main` holds the `derive_story_slug` change and its tests.
- A dispatch with `story_file=other/foo.md` fails in Analysis with a message naming the path.

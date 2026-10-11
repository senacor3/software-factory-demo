---
tracker_id: ""
key: ""
type: epic
title: "Configurable checks and the pipeline's remaining gaps"
parent: initiative-light-factory
covers: [CAP-1, CAP-2, CAP-3, CAP-5]
after: ["epic-pipeline-open-issues"]
assignee: ""
risk: medium
estimate: ""
estimate_basis: "envelope"
status: done
---

# Configurable checks and the pipeline's remaining gaps

> **Status:** done (2026-10-11). Shown live: the checks running from the repo's config, a clarification halt ending without the `plan-approval` gate, three stories merged through the six-job pipeline, and the fix loop engaging for the first time. Not shown live: a halt at the clarification cap. Three low findings stay open in `deferred-work.md` — see the closure note at the end of Notes.

## Description

Two epics left the pipeline live-proven but with work that had no ticket: the mechanical checks are hard-coded to this repo's own Python code (`factory/scripts/run_checks.py`), so the pipeline cannot check any other project; and three items sat open in `deferred-work.md` only. This epic gives every one of them an owner. The spec and architecture still own the capabilities; nothing here adds a new one.

## Outcome

The pipeline can check a project other than itself — `initiative-demo-app`'s Spring Boot/Angular app is the first. The fix loop's first live engagement moved to `initiative-demo-app` (see Notes).

## Requirements

- CAP-5 (reused): Build, test, lint, and security checks run as direct pipeline steps, without agent involvement. — This epic's part: the commands come from a per-repo checks config instead of being hard-coded; `security` stays a `"skipped"` placeholder in this repo (see Notes).
- CAP-2 / CAP-3 (reused): A clarification halt ends the run without a gate (AD-13). — This epic's part: a clarification-halted run no longer pauses at `plan-approval`.
- CAP-1 (reused): A story file is `stories/<story-slug>.md` (AD-8), and one story-slug cannot run twice at once (AD-15). — This epic's part: story files outside `stories/` are rejected, delivered by merging `stories/validate-story-file-location.md` through the pipeline.

## Done when

1. The check commands are read from a per-repo checks config; this repo's config reproduces today's build/test/lint results, and a check with no configured command reports `"skipped"`, never `"pass"`.
2. A run that halts for clarification, below the cap or at it, ends without opening the `plan-approval` gate.
3. `stories/validate-story-file-location.md` has merged to `main` through the pipeline, and a dispatch for a story file outside `stories/` is rejected.
4. A documented decision exists on blueprint update-propagation: build a mechanism, or close the item with a reason.

Each item is demonstrated live and merged, not only unit-tested — the same bar the two earlier epics set.

## Boundaries

The pipeline itself (`.github/workflows/`, `factory/`, `.claude/skills/`, `.factory/`) — the same boundary as the two earlier epics. Not the demo app's own code or its checks config (that is `initiative-demo-app`'s entry 7). Not real security tooling for this repo.

## References

- parent — _bmad-output/initiative-light-factory/initiative-light-factory.md, Done when
- spec — _bmad-output/initiative-light-factory/spec-light-factory/spec-light-factory.md, section Capabilities
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-6, AD-8, AD-13, AD-15
- source — _bmad-output/initiative-light-factory/deferred-work.md, its entries still open on 2026-10-11
- sibling — _bmad-output/initiative-light-factory/epic-pipeline-open-issues/epic-pipeline-open-issues.md, Notes
- consumer — _bmad-output/initiative-demo-app/epic-demo-app/epic-demo-app.md, entry 7 waits on this epic's entry 1

## Notes

- Decision: epic created from the 2026-10-11 review of the ticket tree, to own the configurable-checks story, the fix-loop live run, and every item still open in `deferred-work.md` (user's call, 2026-10-11).
- Decision: `security` is a permanent `"skipped"` placeholder in the light-factory repo; no ticket will wire a scanner here (user's call, 2026-10-11). Initiative Done-when 2 was reworded to match.
- Assumption: a project that wants a real security check supplies its command through the checks config from entry 1. The user's wording was "placeholder in light-factory only"; confirm this reading when entry 1 starts.
- Decision: the tracer bullet is entry 1; the entries form one lane in file order, since entries 1 and 2 both edit `.github/workflows/light-factory.yml` and entry 3 is a live dispatch that should run on the result.
- Decision: no separate closing end-to-end suite — entry 3 is itself a live run and the first merge through the six-job pipeline.
- Unknown: the checks config's format and location, and how one repo holding both `factory/` and `freight-tenders/` scopes its commands; entry 1 settles it and records an AD-6 addendum. `epic-demo-app`'s entry 7 waits on the answer.
- Decision (2026-10-11): entry 4, "Fix loop engaged on a live run", stopped and moved to `initiative-demo-app`'s `epic-demo-app` as its entry 10, with its plan (user's call). Two attempts here ended with 0 fix cycles — runs `38147061301` (PR #9, `d28e700`) and `38148260661` (PR #10, `eabd472`), both merged as useful fixes in their own right. The analysis plans were explicit enough that the implementer deviated nowhere, and anything functionally wrong would have failed a check before review. The moved entry adds a first step: give the review agent more instructions. CAP-7 leaves this epic's `covers`, the former Done-when 4 is gone (the decision on propagation is now 4), and entry 6 no longer waits on entry 4.
- Decision (2026-10-11, entry 5): no update-propagation mechanism is built now; the item is closed until a second repository actually adopts the pipeline (user's call). The freight-tenders app lives in this repo, so there is one copy and nothing to propagate to. When a second copy exists, choose between a documented re-copy/diff procedure, a versioned blueprint release, or the move to a dedicated orchestrating repo. This meets Done-when 4.
- Entry 6's disposition of what entries 1, 2, 3, and 5 left behind (2026-10-11), per its "no new behavior" scope; detail is in `deferred-work.md` and `story-refactor-sweep-plan.md`:
  1. **Fixed by entry 6** — AD-15's concurrency wording, open since `epic-pipeline-open-issues`: the Rule and the conventions row now say the group is keyed on the raw `story_file` input, so the guard holds per input path, not per story-slug. The workflow's own comment says the same.
  2. **Fixed by entry 6** — drift left by the two stories merged through the pipeline (PR #9, PR #10): the `checks` job's comment and the CAP-5 row of the capability map now say the config is read from `origin/main`, and they, AD-6's addendum, and `run_checks.py`'s docstrings no longer claim that a story "cannot weaken its own checks" (only the config is protected); `fix_loop_graph.py`'s docstring no longer calls `security` a placeholder. Comments and docs only.
  3. **Resolved in part, the rest re-parked** — entry 1's deferred finding (a story branch could weaken its own checks) was built through the pipeline as PR #9 for the config only; see item 4 for what remains. **Already resolved** — entry 2's rejected low finding (a failed status-output write exiting 1) as PR #10.
  4. **Re-parked, new behavior** — three new entries in `deferred-work.md`, all low and unowned: the PR left open when `analysis` fails after opening it; the two holes left in the checks guard (`run_checks.py` still runs from the story branch, and the working-tree fallback); and the concurrency guard holding per input path only — entry 3 removed the `other/foo.md` case, but `./stories/foo.md` or `docs/stories/foo.md` still share a slug with `stories/foo.md`.
  5. **Re-parked, needs a live run** — entry 2's live proof that a clarification-halted run ends without the `plan-approval` gate. It needs a dispatch of a story with an open question; its `deferred-work.md` entry stays unresolved and entry 2 stays `built` until then. Done-when 2 is not met yet.
  6. **Nothing deferred** — entries 3 and 5.
- Entry 2's live proof completed (2026-10-11): run `38149509051` halted for clarification on `stories/one-input-path-per-story-slug.md` and ended without opening `plan-approval` — every later job skipped, no review requested, PR #11 labeled and closed with the questions. Done-when 2 is met below the cap; the at-cap variant shares the code path and was not run. This closes item 5 of entry 6's disposition list. The story itself is unanswered: its question (reject or normalise other spellings of a story path) is the user's, and the per-slug concurrency finding stays open in `deferred-work.md` until it is answered and re-dispatched.
- Fix loop engaged live (2026-10-11): run `38150142797` (`stories/one-input-path-per-story-slug.md`, PR #12, merged as `c60279b`), the answered re-dispatch of the story used for entry 2's proof. The first review raised one finding (two CLI tests the plan listed were missing), one fix cycle added them, the second review was clean: `fix_cycle: 1`, within the cap of 2, then `evidence-approval` and merge. Not seeded. This is the proof entry 4 was after before it moved to `epic-demo-app`; it happened here on an unticketed run, so no entry of this epic claims it and CAP-7 stays out of `covers`. The same run also showed the second clarification round resolving (one round of two spent, PR #11) and built the per-slug half of the concurrency finding.
- Closure (2026-10-11, user's call), checked against Done when and Requirements:
  1. **Done-when 1, met** — ticket 1 (`825c3b7`); on the runner, every run since `38146170332` records the commands from `.github/post-implementation-checks.yml`, and `security` records `skipped` with "no command configured".
  2. **Done-when 2, met below the cap; at the cap not shown live** — ticket 2 (`621ad6a`); run `38149509051` halted with `awaiting-clarification`, every later job skipped, no review requested. A `clarification-cap-reached` halt takes the same path (the `implementation` job's `if:` allows only `ready-for-review`) and is covered by unit tests of the status output, but no story has spent both rounds. Accepted as closed on that basis.
  3. **Done-when 3, met** — ticket 3; run `38146170332` merged PR #8 as `5f56b5f`, and run `38146620264` rejected `other/foo.md`.
  4. **Done-when 4, met** — ticket 5: no mechanism now, reopen when a second repository adopts the pipeline.
  - **Moved, not dropped** — entry 4 (the fix loop's live proof) went to `epic-demo-app` and was then delivered here anyway, on run `38150142797`; that entry is now review-agent instructions only.
  - **Requirement met in part, by decision** — CAP-1's "one story-slug cannot run twice at once": a different file can no longer share a slug (PR #8, PR #12), but two spellings of one file are still two concurrency groups (user's call to normalise, 2026-10-11).
  - **Open in `deferred-work.md`, all low and unowned** — the PR a run can leave open when `analysis` fails after opening it; the two holes left in the checks guard (`run_checks.py` runs from the story branch; the working-tree fallback); the two-spellings remainder above. Update-propagation is re-parked by decision, not a defect.

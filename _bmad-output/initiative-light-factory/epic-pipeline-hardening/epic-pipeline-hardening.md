---
tracker_id: ""
key: ""
type: epic
title: "Configurable checks and the pipeline's remaining gaps"
parent: initiative-light-factory
covers: [CAP-1, CAP-2, CAP-3, CAP-5, CAP-7]
after: ["epic-pipeline-open-issues"]
assignee: ""
risk: medium
estimate: ""
estimate_basis: "envelope"
---

# Configurable checks and the pipeline's remaining gaps

## Description

Two epics left the pipeline live-proven but with work that had no ticket: the mechanical checks are hard-coded to this repo's own Python code (`factory/scripts/run_checks.py`), so the pipeline cannot check any other project; the fix loop has never engaged on a live run; and three items sat open in `deferred-work.md` only. This epic gives every one of them an owner. The spec and architecture still own the capabilities; nothing here adds a new one.

## Outcome

The pipeline can check a project other than itself — `initiative-demo-app`'s Spring Boot/Angular app is the first — and initiative Done-when 3 is met for the fix loop as well as the clarification loop.

## Requirements

- CAP-5 (reused): Build, test, lint, and security checks run as direct pipeline steps, without agent involvement. — This epic's part: the commands come from a per-repo checks config instead of being hard-coded; `security` stays a `"skipped"` placeholder in this repo (see Notes).
- CAP-7 (reused): Review findings route back to the implementation agent for a bounded number of fix cycles. — This epic's part: one live run on which the loop engages at least once and stays within its cap of 2.
- CAP-2 / CAP-3 (reused): A clarification halt ends the run without a gate (AD-13). — This epic's part: a clarification-halted run no longer pauses at `plan-approval`.
- CAP-1 (reused): A story file is `stories/<story-slug>.md` (AD-8), and one story-slug cannot run twice at once (AD-15). — This epic's part: story files outside `stories/` are rejected, delivered by merging `stories/validate-story-file-location.md` through the pipeline.

## Done when

1. The check commands are read from a per-repo checks config; this repo's config reproduces today's build/test/lint results, and a check with no configured command reports `"skipped"`, never `"pass"`.
2. A run that halts for clarification, below the cap or at it, ends without opening the `plan-approval` gate.
3. `stories/validate-story-file-location.md` has merged to `main` through the pipeline, and a dispatch for a story file outside `stories/` is rejected.
4. A live run shows the fix loop engaging at least once and finishing within its cap of 2.
5. A documented decision exists on blueprint update-propagation: build a mechanism, or close the item with a reason.

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
- Decision: the tracer bullet is entry 1; the entries form one lane in file order, since entries 1 and 2 both edit `.github/workflows/light-factory.yml` and entries 3 and 4 are live dispatches that should run on the result.
- Decision: no separate closing end-to-end suite — entries 3 and 4 are themselves live runs, and entry 3 is the first merge through the six-job pipeline.
- Unknown: the checks config's format and location, and how one repo holding both `factory/` and `freight-tenders/` scopes its commands; entry 1 settles it and records an AD-6 addendum. `epic-demo-app`'s entry 7 waits on the answer.
- Unknown: how to make a review finding appear reliably on a live run; entry 4 settles it when it starts.
- Open question: blueprint update-propagation was raised when the demo app was to be a second repo. The demo app now lives in this repo (user's call, 2026-10-11), so there is no second copy today; entry 5 may close the item on that basis.

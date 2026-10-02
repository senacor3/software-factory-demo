---
tracker_id: ""
key: ""
type: epic
title: "The gated delivery pipeline"
parent: initiative-light-factory
covers: [CAP-1, CAP-2, CAP-3, CAP-4, CAP-5, CAP-6, CAP-7, CAP-8, CAP-9]
after: []
assignee: ""
risk: medium
estimate: ""
estimate_basis: ""
---

# The gated delivery pipeline

## Description

One GitHub Actions workflow, one triggered run: a story file goes in, an analysis agent proposes a plan through a bounded clarification loop, the developer confirms it, an implementation agent codes it on an isolated branch behind a PR, deterministic checks and an independent read-only review agent evaluate it through a bounded fix loop, the developer approves from an evidence summary, and the pipeline merges. The spec and its architecture companion own every capability and decision this epic implements.

## Outcome

A real story run completes end-to-end to merge with both `plan-approval` and `evidence-approval` gates exercised — the spec's Success signal.

## Done when

1. A complete, in-scope story file runs through intake, analysis, and the clarification loop to a confirmed `plan.md`/`decisions.md`, and an incomplete/out-of-scope one halts with a clear reason instead.
2. `plan-approval` pauses the run as a GitHub Environment gate; approval resumes the same run, rejection ends it; no implementation commit exists before approval.
3. Implementation lands only on the isolated branch behind a PR opened before the implementation agent runs; its tool-allowlist cannot write outside that branch or another stage's state file.
4. Build/test/lint/security run as direct pipeline steps with zero agent turns, and an independent read-only review agent evaluates the result against the plan.
5. The fix loop never exceeds 2 cycles, re-running only the affected checks; `evidence-approval` lets the developer decide from a concise summary, opening the full diff only on demand.
6. Approval at `evidence-approval` merges to the target branch; a re-triggered run of the same story supersedes its predecessor's branch/PR cleanly, with no zombie approval reaching merge.

## Boundaries

The pipeline itself (`.github/workflows/`, `factory/`, `.claude/skills/`, `.factory/`), not any application it is later used to build. Not staging deployment/production rollout, not swappable AI providers, not alternative triggers, not multi-role approval, not zero-manual-edits enforcement, not ticket-system/chat integrations, not a dedicated orchestrating repo, not Temporal/Camunda — per the spec's non-goals and the architecture's Deferred list.

## References

- parent — _bmad-output/initiative-light-factory/initiative-light-factory.md
- spec — _bmad-output/initiative-light-factory/spec-light-factory/spec-light-factory.md, sections Capabilities and Constraints
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-1 through AD-15, Structural Seed, Consistency Conventions

## Notes

- Decision: full inception now, one pass — 11 build stories, a closing refactor sweep, and a closing end-to-end suite (user's call, 2026-10-01).
- Decision: tracer bullet is entry 1 (pipeline skeleton + both gates, stub Job 3) — proves the FSM/gate pause-resume mechanics end to end before any real agent work is built (2026-10-01).
- Decision: single lane, one owner — the breakdown is a strict linear chain (each entry's `after` is its immediate predecessor only); no parallel lanes, since the pipeline's own jobs are themselves sequential (2026-10-01).
- Decision: no requirement scope was deferred out of this epic — all of CAP-1..CAP-9 and AD-1..AD-15 are covered by entries 1-11 (2026-10-01).
- Decision: builds interactively via `bmad-build`, one story at a time — no `plan_checkpoint`/`done_checkpoint` added, since each entry is refined with the user when reached rather than run unattended (2026-10-01).
- Unknown: what operationally defines a "complete"/"in-scope" story file for the CAP-1 intake check (spec's own Open Questions never settled this) — entry 3 settles it with the user at refine/build time, not before.
- Unknown: Job 3's merge strategy (squash/merge-commit/rebase) and source-branch deletion policy — AD-14 deliberately left this undecided; entry 11 is the only entry that implements Job 3, so it settles this.
- Open question (not this epic's to settle): GitHub Environment protection's native 30-day gate-timeout default, and CAP-4's failure/non-completion path when the implementation agent itself gets stuck — both remain open per the spec; no entry below currently depends on resolving them, revisit if a build surfaces the gap.
- Decision: branch+PR creation moves from Job 2 (entry 6) into Job 1's intake (entry 3 amendment), gated on CAP-1's proceed decision; entry 6 retired, its remaining scope (branch reuse) folds into entry 7 (2026-10-02, see `change-pr-at-intake/change-pr-at-intake.md`).
- Dropped: entry 6 ("Deterministic PR-open step") — had no file and no plan, so removed from `tickets.toml` outright rather than marked `dropped`. Its capability (create branch, commit, open PR) is now entry 3's amendment; entry 7's `after` repoints from `[6]` to `[5]`, and entry 12's `after` list drops `6` (2026-10-02).

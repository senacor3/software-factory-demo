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
status: done
---

# The gated delivery pipeline

> **Status:** done (2026-10-10). Run `38076319765` took a real story to merge with both gates approved by a person. Done-when 1, 2, and 6 were finished by `epic-pipeline-open-issues` — see the closing note at the end of Notes.

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

- Decision: full inception now, one pass — 11 build stories, a closing refactor sweep, and a closing end-to-end suite (user's call, 2026-10-01). Amended 2026-10-02: 10 build stories once entry 6 was retired.
- Decision: tracer bullet is entry 1 (pipeline skeleton + both gates, stub Job 3) — proves the FSM/gate pause-resume mechanics end to end before any real agent work is built (2026-10-01).
- Decision: single lane, one owner — the breakdown is a strict linear chain (each entry's `after` is its immediate predecessor only); no parallel lanes, since the pipeline's own jobs are themselves sequential (2026-10-01). Amended 2026-10-02: the chain skips retired entry 6 (entry 7 follows entry 5); the sweep, entry 12, waits on every build entry.
- Decision: no requirement scope was deferred out of this epic — all of CAP-1..CAP-9 and AD-1..AD-15 are covered by entries 1-11 (2026-10-01). Superseded: scope was deferred after this date — see the closing note dated 2026-10-11.
- Decision: builds interactively via `bmad-build`, one story at a time — no `plan_checkpoint`/`done_checkpoint` added, since each entry is refined with the user when reached rather than run unattended (2026-10-01).
- Unknown: what operationally defines a "complete"/"in-scope" story file for the CAP-1 intake check (spec's own Open Questions never settled this) — entry 3 settles it with the user at refine/build time, not before.
- Unknown: Job 3's merge strategy (squash/merge-commit/rebase) and source-branch deletion policy — AD-14 deliberately left this undecided; entry 11 is the only entry that implements Job 3, so it settles this.
- Open question (not this epic's to settle): GitHub Environment protection's native 30-day gate-timeout default, and CAP-4's failure/non-completion path when the implementation agent itself gets stuck — both remain open per the spec; no entry below currently depends on resolving them, revisit if a build surfaces the gap.
- Decision: branch+PR creation moves from Job 2 (entry 6) into Job 1's intake (entry 3 amendment), gated on CAP-1's proceed decision; entry 6 retired, its remaining scope (branch reuse) folds into entry 7 (2026-10-02, see `change-pr-at-intake/change-pr-at-intake.md`).
- Dropped: entry 6 ("Deterministic PR-open step") — had no file and no plan, so removed from `tickets.toml` outright rather than marked `dropped`. Its capability (create branch, commit, open PR) is now entry 3's amendment; entry 7's `after` repoints from `[6]` to `[5]`, and entry 12's `after` list drops `6` (2026-10-02).
- Decision: entry 4 retitled "Clarification halt (single-pass, v1)" and simplified to no loop — any open question from entry 3's one analysis pass halts immediately (PR comment + close), rather than the originally-planned 2-round agent/human loop. The real bounded-loop design is deferred (see `deferred-work.md`); SPEC's CAP-2 and AD-13 amended to match (user's call, 2026-10-02).
- Entry 12's disposition of the `deferred-work.md` entries accumulated across entries 1–11 (2026-10-02); the evidence for each is in `deferred-work.md`:
  1. **Resolved** — entry 3's live-dispatch verification.
  2. **Fixed by entry 12** — the architecture doc's file tree and CAP-6/CAP-7 map rows (docs only).
  3. **Re-parked, externally blocked** — entry 1's required-reviewers protection (resolved 2026-10-10) and entry 5's reject-closes-PR.
  4. **Re-parked, SPEC-level** — entry 4's real bounded-clarification mechanism.
  5. **Re-parked, new behavior** — entry 3's AD-15 supersession-closing and entry 8's real lint/security tooling.
- Decision: entry 13 (closing end-to-end suite) held off (user's call, 2026-10-10) — a real run today would reach both gate boundaries but not actually pause at either, since required-reviewers protection is still inactive (deferred-work.md's first entry); running it now would just auto-merge to `main` with no human in the loop, not demonstrate the gate behavior the ticket's verify text asks for. Story already chosen for whenever it does unblock: wire real `ruff` lint tooling (deferred-work.md's sixth entry) as the real story the pipeline builds.
- Decision/discovery (2026-10-10): the project's remote moved from `DAICST/software-factory` (private, Free org) to `senacor3/software-factory-demo`. Along the way, confirmed live that GitHub Team does *not* unlock required-reviewers Environment protection for a *private* repo — only Enterprise does; Free/Team both restrict it to public repos (this corrects the "Team/Enterprise" claim made on 2026-10-01/02, which was wrong). Resolved by making `senacor3/software-factory-demo` public (user's call) and attaching `required_reviewers` protection to both `plan-approval` and `evidence-approval` there, reviewer `leichtundkross`. This both resolves deferred-work.md's first entry and unblocks entry 13 — see `deferred-work.md` for the full disposition. `DAICST/software-factory` remains in its prior state; it is no longer the active development remote.
- **Entry 13 completed (2026-10-10): the epic's spec Success signal is proven live.** Run `38076319765` ran the `ruff`-lint story through the full pipeline for real — both gates genuinely paused and were approved by the human, review resolved clean with 0 fix cycles, Job 3 squash-merged `cfd3ca0`. Reaching that took 3 earlier failed attempts, each surfacing and fixing a real bug no unit test had caught: a Python-version-pinning gap (fresh runners could resolve an unsupported-by-PyO3 version), the hard GitHub restriction on `GITHUB_TOKEN` ever writing `.github/workflows/*` (kept as-is, not widened — doing so would let the implementation agent rewrite its own gates, an AD-5 regression; the story was narrowed instead), and two independent bugs in `run_checks.py` (no agent can self-establish a clean `ruff` baseline, since none have a Bash tool; the `detail` field preferred `stderr` over `stdout`, masking real failure output behind `uv`'s own install banner). All of CAP-1 through CAP-9 have now been exercised live, not just unit-tested. Full chain documented in `story-closing-end-to-end-suite-plan.md`'s Implementation Notes and `deferred-work.md`.
- Closing note (2026-10-11): this epic was marked done with three of its Done-when items delivered only in part. Done-when 1's clarification loop shipped here as a single-pass halt and became a real bounded loop in `epic-pipeline-open-issues` ticket 2.2; Done-when 2's "rejection ends it" gained its PR-closing in ticket 2.5; Done-when 6's supersession was built by ticket 2.4. The fix loop's first live engagement and the items still open in `deferred-work.md` are owned by `epic-pipeline-hardening`.

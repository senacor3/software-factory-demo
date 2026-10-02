---
id: CHANGE-pr-at-intake
initiative: initiative-light-factory
epic: epic-light-factory-pipeline
created: '2026-10-02'
status: 'approved'
scope: 'moderate'
---

# Sprint Change Proposal: Open the PR at Intake, Not at Implementation

## Section 1 — Issue Summary

**Problem statement.** AD-12 currently opens the isolated branch + PR at the start of Job 2 ("implementation"), immediately before the implementation agent runs. This leaves Job 1 ("analysis") with no PR to attach anything to — which is why AD-4 carries a "commit comment vs. PR comment" special case purely for timing reasons, and why only the `evidence-approval` gate has a PR available to hang a review off of.

**How this was discovered.** Not a defect in built code. It surfaced while evaluating deferred-work.md entry 1 (GitHub Environment required-reviewers protection rules are Enterprise-only for private repos — confirmed via GitHub docs and multiple first-hand community reports; Free/Pro/Team do not unlock it for private repos, only for public ones). The free workaround — branch-protection required-PR-review + auto-merge — only works for `evidence-approval` today, because `plan-approval` has no PR yet at that point. The user proposed opening the PR at intake instead, conditioned on the CAP-1 intake judgment deciding to proceed, so a halted/out-of-scope story never opens one.

**Evidence.** AD-12's own text ("Job 1, pre-branch, has no PR yet"); AD-4's temporal split; the empirically-confirmed GitHub Enterprise restriction from the prior session discussion; the current `.github/workflows/light-factory.yml` (`analysis` job has no git-write step; `implementation`/`merge` are still stubs); confirmed via `grep` that no commit/push logic exists anywhere in `factory/` yet.

**Scope decision (explicit, made with the user before analysis began):** this change is PR-timing only. It does **not** replace AD-2's gate mechanism (GitHub Environment + required-reviewers protection rules stays the canonical mechanism, still blocked per deferred-work.md entry 1) and does **not** touch the SPEC (`spec-light-factory.md`) — the SPEC's CAP-3/CAP-4 success criteria hold regardless of which job opens the PR.

## Section 2 — Impact Analysis

**Epic impact.** `epic-light-factory-pipeline` cannot proceed exactly as sequenced. The capability boundary for "who opens the PR" moves from ticket 1.6's territory into ticket 1.3's (already `built`). Epic-level success criterion #3 ("a PR opened before the implementation agent runs") still holds literally — the PR just opens earlier than strictly required — so no epic acceptance-criteria rewrite is needed, only a decision-log entry and ticket resequencing.

**Story impact.**
- Ticket 1 (`built`) — no functional change; one stale cross-reference.
- Ticket 2 (`built`) — unaffected (shared state library, orthogonal).
- Ticket 3 (`built`) — real functional amendment: add the conditional branch+PR-open step after a non-halted `run_analysis` result.
- Ticket 4, 5 (`planned`) — scope notes only, no code exists yet to amend.
- Ticket 6 (`planned`) — **retired**, capability absorbed into ticket 3.
- Ticket 7 (`planned`) — `after:` changes from `[6]` to `[5]`; Code Map gains a one-line "checkout existing branch" step.
- Ticket 12 (`planned`) — `after:` list drops the retired `6`.
- Tickets 8–11, 13 — unaffected.

**Artifact conflicts.**
- **SPEC:** none (confirmed by the scope decision above).
- **Architecture** (`architecture-light-factory.md`): AD-12 (retitled, retriggered, drops placeholder-commit workaround), AD-4 (drops commit-comment special case), AD-5 (notes Job 1's new token scope), AD-13 (cap-out posts/closes PR instead of commit comment), AD-2 (reject closes the PR), AD-15 (becomes the single source of truth for same-run PR-closing, not just cross-run supersession), the Consistency Conventions "Naming (PR/comment target)" row, the Capability→Architecture Map CAP-4 row, and the Structural Seed mermaid diagram + file-tree comment.
- **UI/UX:** N/A, no UI/UX docs exist for this project.

**Technical impact.** `.github/workflows/light-factory.yml`'s `analysis` job gains a new step and new `GITHUB_TOKEN` permissions (`contents: write`, `pull-requests: write`) it has none of today. `factory/graph/analysis_graph.py` gains the conditional script invocation. The existing 57 tests and the live-verified halt path (run `36970131400`, 2026-10-02) must be re-run after the amendment to confirm no regression — this is the same halt path that was just manually exercised, so re-verification is cheap and already has a known-good baseline to compare against. `deferred-work.md` entry 1 gets a cross-reference note (not resolved).

## Section 3 — Recommended Approach

**Selected: Option 1, Direct Adjustment.** Amend ticket 3 (built) with new, additive logic; update tickets 4/5 (planned, no code yet, free to adjust); retire ticket 6; adjust ticket 7's dependency. Stays entirely within the current epic — no new epic, no PRD/MVP change.

- **Rollback (Option 2) — rejected.** Nothing about tickets 1–3 is wrong; their CAP-1/CAP-2 logic, schemas, and tests all remain valid. This is additive, not a failed approach to undo.
- **PRD/Spec MVP review (Option 3) — rejected.** Already settled by the scope decision: spec and MVP goals are untouched.

**Effort: Medium** — one built ticket gets real new logic; three planned tickets get scope edits before any code exists for them; one ticket retires cleanly since nothing was ever built against it.

**Risk: Medium** — amending built ticket 3 risks regressing its 57 passing tests and the live-verified halt path (both have known-good baselines to re-check against, which bounds the risk); Job 1 gains new GitHub token permissions, a new AD-5 scoping surface that needs to be exactly as narrow as AD-5 already requires (script-only, never the agent's own tool-allowlist).

**Design decision made during analysis:** on a clarification cap-out (AD-13) or a `plan-approval` reject (AD-2), the PR that's been open since intake is closed immediately with a comment explaining why — not left open to accumulate. This keeps "an open PR" meaning "still awaiting a decision" at all times, consistent with AD-15's existing closed-not-deleted, audit-trail posture for superseded PRs (same pattern, new trigger).

## Section 4 — Detailed Change Proposals

### 4.1 Architecture (`architecture-light-factory.md`)

**AD-12** — retitle *"PR opened by a deterministic pipeline step, once intake decides to proceed."*
- OLD: triggers "before the implementation agent is invoked" (start of Job 2); makes a placeholder commit; "Makes AD-4's split temporal."
- NEW: triggers once Job 1's CAP-1 judgment says proceed (not on a halt); the script commits the analysis stage's own `plan.md`/`decisions.md` as the real first commit (no placeholder commit needed); Job 2 reuses this branch via the propagated name instead of creating its own; a halted run never reaches this script — no branch/PR for it.

**AD-4** — drop the commit-comment special case.
- OLD: "posts a concise human-readable summary as a PR/commit comment."
- NEW: "posts... as a PR comment" — flat rule, both gates alike, since AD-12 now guarantees a PR exists by either gate.

**AD-5** — note the new credential surface.
- ADD: "Job 1's token permissions now include `contents: write` and `pull-requests: write` (previously none) to run AD-12's script — scoped to that script alone, never to the analysis agent's own read-only tool-allowlist."

**AD-13** — cap-out posts to the PR, not a commit.
- OLD: "posts the remaining open question(s) as a commit comment on the triggering story-file commit."
- NEW: "posts the remaining open question(s) as a comment on the PR AD-12 opened at intake, and closes that PR per AD-15."

**AD-2** — reject closes the PR.
- ADD: "The PR AD-12 opened at intake for this run is closed at reject time, per AD-15."

**AD-15** — becomes the single source of truth for PR-closing on same-run termination, not only cross-run supersession.
- ADD: "AD-2's `plan-approval` reject and AD-13's clarification cap-out each close their own run's PR at that moment too — with a comment stating why — not only when a later retrigger supersedes it. An open PR therefore always means 'still awaiting a decision,' never 'already resolved one way or the other.'"

**Consistency Conventions**, row "Naming (PR/comment target)":
- NEW: "The PR exists from the moment Job 1's CAP-1 judgment decides to proceed (AD-12) — both gates post as PR comments on it (AD-4). A cap-out or reject closes that PR with a comment (AD-15); a retrigger's new PR closes and links to any PR it supersedes (AD-15)."

**Capability → Architecture Map**, CAP-4 row:
- OLD: `Lives in: Job 2, isolated branch + PR`
- NEW: `Lives in: Job 1 opens the isolated branch + PR once CAP-1 proceeds; Job 2 reuses it for code`

**Structural Seed** — `Job1_Analysis` mermaid state gains an `OpenPR1` step between intake/analysis and the clarification loop, with a `Halted` branch that skips it; `open_implementation_pr.py`'s file-tree comment updated to describe the new trigger point and real first commit (optional rename to `open_story_pr.py`, left to implementation-time judgment).

### 4.2 Epic & ticket board (`epic-light-factory-pipeline.md` + ticket board)

| Ticket | Change |
|---|---|
| 3 (`built`, CAP-1/CAP-2) | Add CAP-4 to covers (the "open PR" sub-capability only). |
| 4 (`planned`, CAP-2) | Scope note: rounds commit to the existing branch/PR; cap-out posts + closes per AD-13/AD-15. |
| 5 (`planned`, CAP-3) | Scope note: gate summary posts as PR comment; reject closes the PR. |
| 6 (`planned`, CAP-4) | **Retire** — capability absorbed into ticket 3. |
| 7 (`planned`, CAP-4) | `after:` `[6]` → `[5]`; Code Map gains "checkout existing branch" line. |
| 12 (`planned`) | `after:` list drops `6`. |

Decision-log entry: *"Decision: branch+PR creation moves from Job 2 (ticket 6) into Job 1's intake (ticket 3 amendment), gated on CAP-1's proceed decision; ticket 6 retired, its remaining scope (branch reuse) folds into ticket 7 (2026-10-02)."*

`deferred-work.md` entry 1 cross-reference (not a resolution): once a PR exists at intake, `plan-approval` could in principle use the same free branch-protection-review alternative `evidence-approval` already had access to — the gate-mechanism swap itself remains out of scope / undecided.

### 4.3 Ticket plan amendments

**Ticket 1** (`story-pipeline-skeleton-gates-plan.md`) — no code change. Plan Change Log entry: the "no PR/branch creation" `Never` bullet's forward-reference to "entry 6" is stale (entry 6 retired); that capability now lives in entry 3's amendment. No functional change to this ticket's own built code.

**Ticket 3** (`story-job-1-intake-analysis-plan.md`) — real functional amendment. Plan Change Log entry: triggering finding is this sprint change proposal; amended to add the conditional deterministic script call after a non-halted `run_analysis` result (commit `plan.md`/`decisions.md` as the real first commit, open the PR); on `AnalysisHalted`, behavior is unchanged. Job 1's workflow step gains `contents: write`/`pull-requests: write` token scope. KEEP: all 57 currently-passing tests, the schema, the skill prompt, and the live-verified halt path (run `36970131400`) must still pass/behave identically — re-verify both as part of the amendment.

## Section 5 — Implementation Handoff

**Scope classification: Moderate** — backlog reorganization (ticket retirement/resequencing) plus architecture-doc edits and one built-ticket amendment; no PRD/MVP replan, no new epic.

**Handoff plan** (single-session project — one developer applies all of the below, in this order):
1. Apply the architecture-doc edits (Section 4.1) directly to `architecture-light-factory.md`.
2. Apply the epic/ticket-board changes (Section 4.2) via `bmad-ticket` (retire ticket 6, adjust ticket 7's `after:` and ticket 12's `after:` list, update covers, add the decision-log entry).
3. Append the Plan Change Log entries to tickets 1 and 3 (Section 4.3).
4. Re-enter `bmad-build` on ticket 3 to implement the conditional branch+PR-open step, re-run the existing 57 tests, and re-run the live halt-path dispatch to confirm no regression before marking the amendment built.
5. Add the cross-reference note to `deferred-work.md` entry 1.

**Success criteria:** architecture doc is internally consistent (no remaining Job-2-only PR-timing references); ticket board reflects ticket 6's retirement and the resequencing; ticket 3's amendment is implemented, tested, and the live halt path re-verified unchanged; both Plan Change Logs are updated; `deferred-work.md` carries the cross-reference.

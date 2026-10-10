---
title: 'Clarification loop: bounded rounds via re-trigger (Option C)'
type: change-proposal
initiative: initiative-light-factory
created: '2026-10-10'
status: approved
---

# Sprint Change Proposal: Clarification loop — bounded rounds via re-trigger

## Section 1: Issue Summary

AD-13 ships v1's clarification handling as single-pass-halt-immediately: Job 1's analysis makes exactly one pass; any open question halts the run, posts a PR comment, and closes the PR, with the developer re-triggering as a new run. This was always a deliberate placeholder, not a final design — the real bounded-clarification mechanism was deferred on 2026-10-02 (`deferred-work.md`, source: `story-clarification-halt-single-pass-v1-plan.md`) without deciding which of two named options to build, and one of them (a live human-reply exchange) has a known, never-resolved conflict with AD-2's "only two long human-wait gates own job boundaries" rule.

Discovered/revisited: ticket 2.1 (`epic-pipeline-open-issues`, a spike whose whole job is this decision), 2026-10-10. Evidence: AD-13's own text documents the deferral; `deferred-work.md`'s entry documents the AD-2 conflict; this session's code investigation confirmed `analysis_graph.py`'s exact single-pass implementation (`run_analysis`) and `fix_loop_graph.py`'s bounded-counter precedent (`MAX_FIX_CYCLES = 2`) as concrete reference points. Investigation also surfaced that `run_analysis`'s only input is ever the story file — there is no mechanism today, even implicitly, for a human's answer to reach a re-triggered run except by editing that file.

## Section 2: Impact Analysis

**Epic Impact:** `epic-pipeline-open-issues` stays completable as planned — entry 2.2 ("Build the real clarification-loop mechanism") already carries an `unknown` field anticipating this decision ("Implementation shape depends entirely on entry 1's decision"). `epic-light-factory-pipeline` (built, live-proven) needs no rework — its ticket 1.4 built today's single-pass-halt behavior explicitly labeled as the v1 interim, not a final design. No new epics needed, no resequencing.

**Story Impact:** Entry 2.2 will build the decided mechanism (Option C, below). Its own description/`unknown` field is a `bmad-ticket` follow-up to refine once this proposal is applied — not part of this change.

**Artifact Conflicts:**
- `spec-light-factory.md` — CAP-2's success criterion describes v1 as a dead-end placeholder; needs to describe the real, decided mechanism.
- `architecture-light-factory.md` — AD-13 (title + Rule, central), AD-10 (status enum needs one new value), Structural Seed diagram (hard-codes single-pass with no loop), Consistency Conventions table (two rows).
- No UI/UX docs exist for this initiative — N/A.
- `deferred-work.md` — the corresponding entry needs marking resolved.

**Technical Impact:** None yet — this proposal is doc-only. The actual mechanism (round-counting logic, the new PR label, the new status value's handling) is entry 2.2's build, not this change.

## Section 3: Recommended Approach

**Recommended: Option C — Bounded rounds via re-trigger, no live mid-job pause.**

Three options were evaluated (full comparison discussed interactively with the user):

- **Option A — Bounded agent-retry** (mirrors AD-11's fix-loop pattern: agent re-attempts with accumulated context, graph-owned counter, within Job 1's existing lifetime). No AD-2 conflict, but doesn't help the class of question only a human can answer — extra agent rounds burn tokens without resolving a genuine judgment call, still halts to a human eventually.
- **Option B — Live human-reply exchange** (a new mid-job pause inside Job 1, reusing AD-2's gate pattern). Resolves genuine human-judgment questions directly, but requires amending AD-2's "only two long human-wait gates" rule — the highest effort and risk of the three, rippling into AD-2, AD-4, and AD-15.
- **Option C — Bounded rounds via re-trigger** (chosen): keep today's halt→PR-comment→close→re-trigger mechanism exactly as-is operationally; count rounds using AD-15's *existing* superseded-PR chain (a `clarification-round` label on each clarification-closed PR — zero new state); at the cap (2, matching AD-11's), change the signal from a repeated halt to an explicit "clarification budget spent, reconsider the story" notice.

**Rationale:** Option C is the only one requiring zero change to AD-2, needs no new state beyond a PR label, and still gets a genuine human answer every time (just asynchronously, as today) — the human edits the story file and re-triggers. This is the lowest-effort, lowest-risk option, and the most consistent with this epic's own Boundaries (finish existing CAP-1..CAP-9 coverage, not invent new architecture). Effort: Low. Risk: Low.

Options 2 (Rollback) and 3 (MVP Review) from the standard checklist were **not viable/not applicable** — this is a forward design decision on a capability the spec already names, not a question of reverting completed work or reducing MVP scope.

## Section 4: Detailed Change Proposals

All four approved by the user (incremental review), 2026-10-10.

### 4.1 — `spec-light-factory.md`, CAP-2 success criterion

**OLD:**
> `plan.md` and `decisions.md` exist with no unresolved open question before the `plan-approval` gate is reached. For v1, intake makes exactly one analysis pass; if it produces any open question, intake halts immediately and surfaces the question(s) directly to the developer instead of looping — a bounded multi-round retry or live human-reply exchange is deferred post-v1 (see deferred-work.md).

**NEW:**
> `plan.md` and `decisions.md` exist with no unresolved open question before the `plan-approval` gate is reached. Each analysis pass that returns an open question halts that run (no live mid-job wait) and surfaces the question(s) on the PR comment; the developer answers by editing the story file and re-triggering. Capped at 2 consecutive clarification rounds per story-slug, counted from the existing supersession-PR chain (AD-15) — on the 2nd unresolved pass, the run halts with a distinct "clarification cap reached" signal instead of repeating the same halt, flagging that the story likely needs rescoping rather than another answer attempt (decided 2026-10-10, `epic-pipeline-open-issues`/2.1).

### 4.2 — `architecture-light-factory.md`, AD-13 (title, Prevents, Rule)

**OLD title:** `AD-13 — Clarification: single-pass for v1, halt immediately on any open question`
**NEW title:** `AD-13 — Clarification: bounded rounds via re-trigger, no live mid-job wait (cap 2, counted from the PR chain)`

**OLD Prevents:** `ambiguity about what happens when analysis can't fully resolve the story alone — without this, intake would either guess (undermining CAP-1/CAP-2) or silently stall`
**NEW Prevents:** `ambiguity about what happens when analysis can't fully resolve the story alone — without this, intake would either guess (undermining CAP-1/CAP-2) or silently stall; unbounded repetition of the same halt-and-re-trigger cycle with no signal that the story itself, not just a missing answer, may be the problem`

**OLD Rule:**
> for v1, Job 1 makes exactly one analysis invocation (entry 3). If it returns any `open_questions`, the graph halts intake immediately — no retry, no loop — writes `plan.md`/`decisions.md` with `status: awaiting-clarification` (AD-10's existing enum — no new status needed), posts the open question(s) as a comment on the PR AD-12 opened at intake, and closes that PR per AD-15 (this path ends the run without reaching a gate, so AD-4's Rule doesn't itself cover the comment step — the convention is shared, the authority is this AD). The developer answers out-of-band and re-triggers the pipeline as a new run, consistent with AD-2's reject-is-terminal/re-trigger pattern and v1's manual-trigger-only model. **Deferred post-v1** (see `deferred-work.md`): a real bounded multi-round mechanism — either the agent re-attempting resolution with accumulated context across rounds (mirrors AD-11's fix-loop pattern), or a live human-reply exchange reusing AD-2's Environment-gate pattern — was the original design intent for this AD and the SPEC's CAP-2 criterion before being simplified for v1 (user's call, 2026-10-02).

**NEW Rule:**
> Job 1 makes one analysis invocation per run (entry 3). If it returns any `open_questions`, the graph halts intake for that run — writes `plan.md`/`decisions.md` with `status: awaiting-clarification` (below cap) or `status: clarification-cap-reached` (at cap, AD-10's enum, new value), posts the open question(s) (or the cap-reached notice) as a comment on the PR AD-12 opened at intake, and closes that PR per AD-15, tagged with a `clarification-round` label so this round counts toward the cap (this path ends the run without reaching a gate, so AD-4's Rule doesn't itself cover the comment step — the convention is shared, the authority is this AD). Before closing, a deterministic step (never the agent) counts how many of this story-slug's prior PRs (AD-15's branch-prefix search, `light-factory/<story-slug>/*`) carry the `clarification-round` label — consecutive clarification closes only, distinct from a reject-closed or ordinary-supersession-closed PR. If this round's count would be the 2nd (the hard cap, matching AD-11's), the status and comment become `clarification-cap-reached`: the developer is told the budget is spent and the story likely needs rescoping or splitting, not another answer attempt — the run still ends without a gate, same as any halt. Below the cap, behavior is unchanged from today: the developer answers by editing the story file itself (the only input `run_analysis` ever reads — this AD now names that explicitly, since nothing else carries an answer across a re-trigger) and re-triggers the pipeline as a new run, consistent with AD-2's reject-is-terminal/re-trigger pattern and v1's manual-trigger-only model. No live mid-job wait is introduced — AD-2's two-gate model (`plan-approval`, `evidence-approval`) is unchanged by this AD.

### 4.3 — `architecture-light-factory.md`, AD-10 (status enum)

**OLD:**
> Canonical `status` values: `plan.md`/`decisions.md` — `drafted`, `awaiting-clarification`, `ready-for-review`; `review.md` — `in-review`, `findings-open`, `fix-in-progress`, `resolved`, `unresolved-after-cap`. No other status strings are valid.

**NEW:**
> Canonical `status` values: `plan.md`/`decisions.md` — `drafted`, `awaiting-clarification`, `clarification-cap-reached`, `ready-for-review`; `review.md` — `in-review`, `findings-open`, `fix-in-progress`, `resolved`, `unresolved-after-cap`. No other status strings are valid.

### 4.4 — `architecture-light-factory.md`, Structural Seed diagram + Consistency Conventions table

**Diagram:** `LG1a`'s label gains "one pass per run, bounded via re-trigger"; the `NeedsClarification` transition gains a round-count condition (`open_questions AND round < cap`); a new `ClarificationCapped` state/transition is added alongside it for the `round == cap` case, flowing to its own PR-comment-and-end path; `RunEndsClarify`'s note is updated to mention the 2-round cap, that answers go via editing the story file, and that past the cap the story needs rescoping.

**Consistency Conventions table — "bounded loops" row:**

**OLD:**
> Fix loop (Job 2): hard-capped at 2 cycles, counted by a counter owned solely by the orchestration graph's loop-control node, never by the agent; `status: unresolved-after-cap` on cap-out (AD-11). Clarification (Job 1): no loop for v1 — a single analysis pass halts immediately on any open question, `status: awaiting-clarification` (AD-13); the real bounded/counted mechanism is deferred post-v1

**NEW:**
> Fix loop (Job 2): hard-capped at 2 cycles, counted by a counter owned solely by the orchestration graph's loop-control node, never by the agent; `status: unresolved-after-cap` on cap-out (AD-11). Clarification (Job 1): hard-capped at 2 rounds, counted from AD-15's existing PR-chain `clarification-round` labels (no new state, no live mid-job wait) — `status: awaiting-clarification` below the cap, `status: clarification-cap-reached` at it (AD-13)

**New row — "Naming (clarification rounds)":**
> Each PR closed for an unresolved open question is tagged `clarification-round` — AD-13 counts these (via AD-15's branch-prefix search) to enforce the 2-round cap; no separate counter file.

## Section 5: Implementation Handoff

**Scope classification: Minor** — doc-only amendment to `spec-light-factory.md` and `architecture-light-factory.md`; no code changes (the mechanism's implementation is entry 2.2, a separate, already-planned ticket).

**Route:** Developer agent (this session, continuing ticket 2.1's build) — applies all four edits above directly to the two documents, then marks `deferred-work.md`'s corresponding entry (source: `story-clarification-halt-single-pass-v1-plan.md`) resolved with a pointer to this proposal.

**Epic/story changes for `bmad-ticket` to apply separately (not this change's own scope):**
- `epic-pipeline-open-issues`'s entry 2.2 ("Build the real clarification-loop mechanism") can have its `description`/`unknown` fields refined now that the shape is known — recommended but not required before entry 2.2 starts, since its current `unknown` field already correctly defers to "entry 1's decision."

**Success criteria:** `spec-light-factory.md`'s CAP-2 and `architecture-light-factory.md`'s AD-13/AD-10/Structural-Seed/Consistency-Conventions all describe Option C consistently; `deferred-work.md`'s entry is marked resolved with a pointer here.

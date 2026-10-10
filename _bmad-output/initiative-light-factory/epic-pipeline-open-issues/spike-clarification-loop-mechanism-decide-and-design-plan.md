---
title: 'Clarification-loop mechanism: decide and design'
type: 'chore'
ticket: '1'
created: '2026-10-10'
status: 'built'
baseline_revision: '0fb562c837a1e6448c9dca43bb93af8a7c8559d7'
route: 'oneshot'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['_bmad-output/initiative-light-factory/deferred-work.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** AD-13 ships v1 as single-pass-halt-immediately on any open question. The real bounded-clarification mechanism — either the analysis agent re-attempting resolution with accumulated context across rounds (mirroring AD-11's fix-loop pattern: a graph-owned counter, hard-capped), or a live human-reply exchange reusing AD-2's Environment-gate pattern — was deferred on 2026-10-02 and never decided. A true live-human-reply-per-question model also directly conflicts with AD-2's "only two long human-wait gates own job boundaries" rule, which was never resolved either. Entry 2.2 (building the real mechanism) can't be planned until this is settled.

**Approach:** Run `bmad-correct-course` with the user to decide between the two options already named in AD-13/`deferred-work.md` — surfacing the AD-2 conflict explicitly if the live-human-reply option is in play — and amend `spec-light-factory.md` (CAP-2) and `architecture-light-factory.md` (AD-13, and AD-2 if the decision touches it) to record and reflect whichever is decided.

## Boundaries & Constraints

**Always:** every decision in the resulting Sprint Change Proposal is the user's explicit choice, never mine — I present the two options already named in AD-13/`deferred-work.md` (and any new one `bmad-correct-course`'s own checklist surfaces) with their tradeoffs, not a pre-picked answer. Any spec/architecture edit reflects exactly what the approved proposal says, with a dated Decision line. If the live-human-reply option is chosen, the AD-2 two-gate-model conflict must be explicitly addressed in the proposal, not glossed over.

**Never:** this ticket does not implement the clarification mechanism itself — that is entry 2.2's job. This ticket only decides which to build and updates the spec/architecture docs to match.

</frozen-after-approval>

## Implementation Notes

Oneshot: this ticket's deliverable is a decision plus a doc amendment, not new code — well under the oneshot threshold regardless of which option is chosen, since either choice only touches `spec-light-factory.md`/`architecture-light-factory.md` here. The mechanism's actual implementation code lands in entry 2.2, not this ticket.

Ran `bmad-correct-course` interactively with the user. Investigation (this session) confirmed `analysis_graph.py`'s `run_analysis` takes the story file as its only input — there is no existing mechanism, even implicit, for a human's clarification answer to reach a re-triggered run except by editing that file; this became an explicit part of the decided design rather than staying an unstated assumption. Three options were compared (not the originally-named two): bounded agent-retry (mirrors AD-11), live human-reply (new mid-job gate, breaks AD-2's two-gate rule), and a third option surfaced during analysis — bounded rounds via re-trigger, counted from AD-15's existing superseded-PR chain via a new `clarification-round` label, zero new state, zero AD-2 impact. The user chose the third option ("Option C") after an elaboration exchange on exactly how human feedback reaches a re-triggered run.

Applied to `spec-light-factory.md` (CAP-2) and `architecture-light-factory.md` (AD-13 title/Prevents/Rule, AD-10's status enum, the Structural Seed diagram's Job1_Analysis state and RunEndsClarify/RunEndsClarifyCap notes, and two Consistency Conventions table rows). `deferred-work.md`'s corresponding entry marked resolved with a pointer to the full proposal at `change-clarification-loop-bounded-rounds/change-clarification-loop-bounded-rounds.md`. No code touched — entry 2.2 builds the mechanism itself.

## Plan Change Log

## Review Triage Log

Quick lens, 1 run. 4 findings, all `high` (patch) — the diff itself introduced each inconsistency; all four had simple, non-speculative fixes.

- AD-15's Rule still said only "clarification cap-out" closes a PR, now stale since every clarification halt (below cap or at it) closes one under the new design. **Patch:** reworded AD-15's sentence to cover both cases, and added a clause distinguishing AD-13's new closed-PR counting query from AD-15's existing open-PR search.
- AD-13's Rule and the new Consistency Conventions row claimed round-counting reuses "AD-15's branch-prefix search" — but that search only ever finds the single open PR to supersede; counting closed, labeled PRs is a different query AD-15 never defines. **Patch:** AD-13's Rule now describes this explicitly as a distinct query over closed PRs, same prefix, different filter.
- Structural Seed's file-tree annotation for `analysis_graph.py` (line ~250) still read "single-pass clarification halt (AD-13)," contradicting the updated AD-13 title and diagram in the same document section. **Patch:** updated the comment to match.
- AD-13's Rule and the diagram's branch conditions (`round == cap`) left undefined behavior for a 3rd+ re-trigger past the cap, since neither "would be the 2nd" nor `== cap` matches a prior count of 2+. **Patch:** changed the condition to "at or above the cap" (`>= cap`) in both the Rule and the two diagram transitions, so repeated re-triggers past the cap stay in the capped state instead of falling through undefined.

## Verification

**Manual checks (if no CLI):**
- `spec-light-factory.md`'s CAP-2 and `architecture-light-factory.md`'s AD-13 (and AD-2 if touched) carry a dated Decision line reflecting the approved Sprint Change Proposal.
- `deferred-work.md`'s corresponding entry (source: `story-clarification-halt-single-pass-v1-plan.md`) is marked resolved with a pointer to the decision.

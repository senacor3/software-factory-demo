---
tracker_id: ""
key: ""
type: epic
title: "Closing the pipeline's open issues"
parent: initiative-light-factory
covers: [CAP-1, CAP-2, CAP-3, CAP-7, CAP-8]
after: ["epic-light-factory-pipeline"]
assignee: ""
risk: medium
estimate: ""
estimate_basis: "envelope"
---

# Closing the pipeline's open issues

## Description

`epic-light-factory-pipeline` proved the spec's Success signal live on 2026-10-10 (run `38076319765`) — but that same run, and the gaps it surfaced or left standing, left concrete items open against capabilities that epic already claims to cover. This epic closes three of them: the real bounded-clarification mechanism (with loops actually exercised, not just staying at 0-of-cap), AD-15's supersession-closing, and the reject-closes-PR path for both gates.

## Outcome

`initiative-light-factory`'s own Done-when criteria 3 and 5 — currently only partially or trivially satisfied — are genuinely met, and a rejected or capped-out run behaves cleanly without manual cleanup. Done-when 2 stays partially satisfied (`security` is still a placeholder) — see Notes.

## Requirements

- CAP-2 (reused): An agent can analyze the story, propose a solution, run a clarification loop on open questions, and document decisions. — v1 shipped as single-pass-halt-immediately (no real bounded loop); the real mechanism is deferred and conflicts with AD-2's two-gate model as written.
- CAP-7 (reused): Review findings route back to the implementation agent for a bounded number of fix cycles. — mechanically capped at 2, but never demonstrated engaging even once on a live run (0 of 2 used).
- CAP-3 (reused): The requesting developer can review and confirm the proposed plan before any code is written; a reject is terminal. — reject does not yet close the `plan-approval` PR; was deferred twice (protection was inactive, and the deployment-review-API query was unbuilt). Protection is now active.
- CAP-8 (reused): The requesting developer approves `evidence-approval` from a concise summary; a change-request decision is terminal. — same reject-closes-PR gap as CAP-3, for `evidence-approval`.
- CAP-1 / initiative Done-when 5 (reused): a re-triggered run of a rejected or capped-out story supersedes its predecessor's PR cleanly. — AD-15's supersession-closing is unbuilt; two abandoned PRs from ticket 1.13's failed live attempts had to be closed by hand.

## Done when

1. A documented decision exists (via `bmad-correct-course`, since it is SPEC-level, not ticket-level) for the real bounded-clarification mechanism, and a live run demonstrates either the clarification loop or the fix loop actually engaging at least once.
2. Re-triggering a run for a story-slug with an existing open PR closes that PR automatically with a "superseded by #N" comment, and posts "retry of #M" on the new one — verified via two sequential dispatches.
3. A real reviewer reject at `plan-approval` closes its PR automatically with an explanatory comment, correctly distinguished from an ordinary job failure via the GitHub deployment-review API; the same holds for `evidence-approval`.

## Boundaries

The pipeline itself (`.github/workflows/`, `factory/`, `.claude/skills/`, `.factory/`) — same boundary as `epic-light-factory-pipeline`. This epic finishes capabilities the spec already claims (CAP-1..CAP-9), it does not add new ones; any new capability discovered along the way is a separate `deferred-work.md` entry or a follow-up epic, not smuggled in here.

## References

- parent — _bmad-output/initiative-light-factory/initiative-light-factory.md
- spec — _bmad-output/initiative-light-factory/spec-light-factory/spec-light-factory.md, section Capabilities
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-2, AD-13, AD-15 specifically
- source — _bmad-output/initiative-light-factory/deferred-work.md, three of its still-open entries (clarification mechanism, AD-15 supersession-closing, reject-closes-PR blocker 2)
- sibling — _bmad-output/initiative-light-factory/epic-light-factory-pipeline/epic-light-factory-pipeline.md, Notes' 2026-10-10 live-run findings

## Notes

- Decision: the clarification-mechanism `bmad-correct-course` pass is this epic's first entry, not a prerequisite run before inception starts (user's call, 2026-10-10).
- Decision: inception complete (2026-10-10) — 7 entries in `tickets.toml`, tracer bullet entry 1 (nothing else is fully plannable until it resolves, though entries 3/4/5 can start in parallel), closing refactor sweep (entry 6) and closing end-to-end suite (entry 7), mirroring epic 1's structure. Validated against `checks.dependencies`/`checks.set`/`checks.ticket` via independent review.
- Note: entry 5 introduces a new detection mechanism (a GitHub deployment-review-API query) with no architecture decision documenting it yet, unlike AD-15's fully-written rule backing entry 4. Expect entry 5's build to author an AD addendum, mirroring how AD-14 was settled during epic 1's entry 11 rather than decided up front.
- Parked: blueprint update-propagation across multiple adopting repos (light-factory is copied per AD-1, not a shared dependency, so a repo that already copied it never sees later fixes) is explicitly out of this epic's scope — it's a new distribution-model capability, not a CAP-1..CAP-9 gap this epic exists to close. Surfaced 2026-10-10 when `initiative-demo-app` became a second adopting repo; full detail in `deferred-work.md`.
- Decision: `initiative-demo-app` (a separate initiative, created the same day) depends on this epic's output — its `epic-demo-app`'s blueprint copy sequences after this epic is built, not after epic 1 alone, so it inherits the fixed `.github/workflows/light-factory.yml` rather than one with these four gaps still open. No formal `after` exists across initiatives; this is the documented handoff both sides carry (2026-10-10).
- Decision: this epic's "production delivery" equivalent is each Done-when item being demonstrated live and merged, not just coded — consistent with the precedent `epic-light-factory-pipeline` set (every entry's real behavior was proven on a live run before being called done) (2026-10-10).
- Source: all four gaps traced to `deferred-work.md` entries dated 2026-10-02 and 2026-10-10, and to `epic-light-factory-pipeline.md`'s "Entry 13 completed" note.
- Dropped: entry 3 ("Real security tooling", CAP-5) removed from this epic and moved back to `deferred-work.md` (user's call, 2026-10-11). It had no file and no plan, so it is dropped by deleting it from `tickets.toml`; id 3 is not reused and entries 4-7 keep their ids. Consequences: CAP-5 leaves this epic's `covers`, the former Done-when 1 is gone (the rest renumbered 1-3), `security` stays a `"skipped"` placeholder, and initiative Done-when 2 is no longer something this epic closes. Earlier dated notes that say "four gaps" or "7 entries" are left as written — read them as three gaps and six entries from this date on, including what `initiative-demo-app` inherits.
- Decision: entry 8, "Explicit job naming and QS sub-jobs", added to this epic's breakdown and placed before entry 6 (user's call, 2026-10-11). No new capability — `covers = []`, same as entries 6 and 7 — so it does not touch this epic's `covers`, Requirements, or Done when; it is a no-new-behavior clarity/structure pass over the pipeline itself, dropping the generic "Job N:" prefix in favor of explicit names and extracting the Implementation job's QS steps (checks + bounded review/fix-loop) into their own job(s). Entry 6 now also depends on it and its description/verify were updated to mention it, since the sweep is defined as blocked by every other entry. Entry 8's own open question (how evidence state crosses the new job boundary, today only persisted via git when a fix cycle commits it, AD-10) is expected to be settled by an AD-10 addendum authored during its build, mirroring how AD-14 was settled during epic 1's entry 11 and how entry 5 is expected to add its own addendum — not a reason to spike it first.

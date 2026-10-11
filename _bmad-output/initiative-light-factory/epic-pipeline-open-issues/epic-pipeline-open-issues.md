---
tracker_id: ""
key: ""
type: epic
title: "Closing the pipeline's open issues"
parent: initiative-light-factory
covers: [CAP-1, CAP-2, CAP-3, CAP-8]
after: ["epic-light-factory-pipeline"]
assignee: ""
risk: medium
estimate: ""
estimate_basis: "envelope"
status: done
---

# Closing the pipeline's open issues

> **Status:** done (2026-10-11). Shown live: the clarification loop, supersession, and a reject closing its PR at both gates. Not shown: the fix loop engaging, the clarification cap being reached, and a merge through the six-job pipeline — The merge was shown by `epic-pipeline-hardening` ticket 3; the fix loop is now `epic-demo-app` entry 10.

## Description

`epic-light-factory-pipeline` proved the spec's Success signal live on 2026-10-10 (run `38076319765`) — but that same run, and the gaps it surfaced or left standing, left concrete items open against capabilities that epic already claims to cover. This epic closes three of them: the real bounded-clarification mechanism (with loops actually exercised, not just staying at 0-of-cap), AD-15's supersession-closing, and the reject-closes-PR path for both gates.

## Outcome

`initiative-light-factory`'s Done-when 5 is met, Done-when 3 is met for the clarification loop, and a rejected or capped-out run behaves cleanly without manual cleanup. The fix-loop half of Done-when 3 moved to `epic-pipeline-hardening` (CAP-7), and `security` stays a placeholder by decision — see Notes.

## Requirements

Each line gives the capability, then the gap as it stood at inception (2026-10-10), then the ticket that closed it.

- CAP-2 (reused): An agent can analyze the story, propose a solution, run a clarification loop on open questions, and document decisions. — v1 shipped as single-pass-halt-immediately (no real bounded loop); the real mechanism is deferred and conflicts with AD-2's two-gate model as written. Closed by tickets 2.1 and 2.2.
- CAP-7 (reused): Review findings route back to the implementation agent for a bounded number of fix cycles. — mechanically capped at 2, but never demonstrated engaging even once on a live run (0 of 2 used). Not closed here: moved to `epic-pipeline-hardening` entry 4 (2026-10-11), and from there to `epic-demo-app` entry 10 the same day.
- CAP-3 (reused): The requesting developer can review and confirm the proposed plan before any code is written; a reject is terminal. — reject does not yet close the `plan-approval` PR; was deferred twice (protection was inactive, and the deployment-review-API query was unbuilt). Protection is now active. Closed by ticket 2.5.
- CAP-8 (reused): The requesting developer approves `evidence-approval` from a concise summary; a change-request decision is terminal. — same reject-closes-PR gap as CAP-3, for `evidence-approval`. Closed by ticket 2.5.
- CAP-1 / initiative Done-when 5 (reused): a re-triggered run of a rejected or capped-out story supersedes its predecessor's PR cleanly. — AD-15's supersession-closing is unbuilt; two abandoned PRs from ticket 1.13's failed live attempts had to be closed by hand. Closed by ticket 2.4.

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
- Decision: inception complete (2026-10-10) — 7 entries in `tickets.toml` [2026-10-11: entry 3 dropped, entry 8 added], tracer bullet entry 1 (nothing else is fully plannable until it resolves, though entries 3/4/5 can start in parallel), closing refactor sweep (entry 6) and closing end-to-end suite (entry 7), mirroring epic 1's structure. Validated against `checks.dependencies`/`checks.set`/`checks.ticket` via independent review.
- Note: entry 5 introduces a new detection mechanism (a GitHub deployment-review-API query) with no architecture decision documenting it yet, unlike AD-15's fully-written rule backing entry 4. Expect entry 5's build to author an AD addendum, mirroring how AD-14 was settled during epic 1's entry 11 rather than decided up front.
- Parked: blueprint update-propagation across multiple adopting repos (light-factory is copied per AD-1, not a shared dependency, so a repo that already copied it never sees later fixes) is explicitly out of this epic's scope — it's a new distribution-model capability, not a CAP-1..CAP-9 gap this epic exists to close. Surfaced 2026-10-10 when `initiative-demo-app` became a second adopting repo; full detail in `deferred-work.md`.
- Decision: `initiative-demo-app` (a separate initiative, created the same day) depends on this epic's output — its `epic-demo-app`'s blueprint copy sequences after this epic is built, not after epic 1 alone, so it inherits the fixed `.github/workflows/light-factory.yml` rather than one with these four gaps [three since 2026-10-11] still open. Superseded 2026-10-11: the demo app now lives in this repo and waits on `epic-pipeline-hardening` entry 1 instead. No formal `after` exists across initiatives; this is the documented handoff both sides carry (2026-10-10).
- Decision: this epic's "production delivery" equivalent is each Done-when item being demonstrated live and merged, not just coded — consistent with the precedent `epic-light-factory-pipeline` set (every entry's real behavior was proven on a live run before being called done) (2026-10-10).
- Source: all four gaps [three since 2026-10-11] traced to `deferred-work.md` entries dated 2026-10-02 and 2026-10-10, and to `epic-light-factory-pipeline.md`'s "Entry 13 completed" note.
- Dropped: entry 3 ("Real security tooling", CAP-5) removed from this epic and moved back to `deferred-work.md` (user's call, 2026-10-11). It had no file and no plan, so it is dropped by deleting it from `tickets.toml`; id 3 is not reused and entries 4-7 keep their ids. Consequences: CAP-5 leaves this epic's `covers`, the former Done-when 1 is gone (the rest renumbered 1-3), `security` stays a `"skipped"` placeholder, and initiative Done-when 2 is no longer something this epic closes. Earlier notes that say "four gaps" or "7 entries" carry a dated inline amendment.
- Decision: entry 8, "Explicit job naming and QS sub-jobs", added to this epic's breakdown and placed before entry 6 (user's call, 2026-10-11). No new capability — `covers = []`, same as entries 6 and 7 — so it does not touch this epic's `covers`, Requirements, or Done when; it is a no-new-behavior clarity/structure pass over the pipeline itself, dropping the generic "Job N:" prefix in favor of explicit names and extracting the Implementation job's QS steps (checks + bounded review/fix-loop) into their own job(s). Entry 6 now also depends on it and its description/verify were updated to mention it, since the sweep is defined as blocked by every other entry. Entry 8's own open question (how evidence state crosses the new job boundary, today only persisted via git when a fix cycle commits it, AD-10) is expected to be settled by an AD-10 addendum authored during its build, mirroring how AD-14 was settled during epic 1's entry 11 and how entry 5 is expected to add its own addendum — not a reason to spike it first.
- Entry 6's disposition of the findings deferred across entries 1, 2, 4, 5, and 8 (2026-10-11); entries 1 and 2 deferred nothing, and the evidence for each item is in `deferred-work.md` and `story-refactor-sweep-plan.md`:
  1. **Fixed by entry 6** — entry 5's doc drift: the architecture said a clarification cap-out closes the PR (docs only).
  2. **Fixed by entry 6** — entry 8's deferred half: "Job 1/2/3" wording replaced by the six named jobs, plus the AD-10 addendum on evidence crossing the `checks`/`review` job boundaries (always committed to the run branch).
  3. **Re-parked, new behavior** — entry 4's finding that `concurrency` is keyed on the raw `story_file` input, not the story-slug. Now `epic-pipeline-hardening` entry 3.
  4. **Re-parked, new behavior** — entry 5's finding that a clarification-halted run still pauses at `plan-approval`. Now `epic-pipeline-hardening` entry 2.
  5. **Carried to entry 7** — the live proofs entries 4, 5, and 8 left out by the user's call, plus two findings only a live `gh` call could settle.
- Entry 7 completed (2026-10-11): four live dispatches on `senacor3/software-factory-demo` for `stories/validate-story-file-location.md` (runs `38140686643`, `38140757607`, `38140846697`, `38141347400`), every gate decision taken by the human. Done-when 1: the clarification loop engaged live — one round halted and closed PR #4 with the `clarification-round` label, the answered re-trigger resolved. Done-when 2: a re-trigger closed PR #5 with "Superseded by #6" and posted "Retry of #5" on #6. Done-when 3: a real reject closed its PR with an explanatory comment at `plan-approval` (#6) and at `evidence-approval` (#7), told apart from a failure via the run's review history. Entry 8's separate `checks`/`review` evidence commits were also seen live. Not shown: the fix loop engaging, the cap being reached, and a merge through the six-job pipeline (no final merge run, user's call) — detail in `story-closing-end-to-end-suite-plan.md`.
- Decision (2026-10-11): CAP-7 removed from this epic's `covers` — no entry covered it and the fix loop never engaged live. `epic-pipeline-hardening` entry 4 owns it (user's call, from the ticket-tree review).
- Decision (2026-10-11): `security` is a permanent `"skipped"` placeholder in the light-factory repo, not a deferred item (user's call). Initiative Done-when 2 was reworded to match.

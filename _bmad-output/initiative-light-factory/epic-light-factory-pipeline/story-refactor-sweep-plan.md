---
title: 'Refactor sweep'
type: 'chore'
ticket: '12'
created: '2026-10-02'
status: 'built'
baseline_revision: 'e6ed71c0f57a43360bfcdf2c483289bd3108f846'
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

**Problem:** `deferred-work.md` has accumulated 7 entries across entries 1–11. One (architecture-doc drift, logged during entry 10's review) is a trivial, zero-behavior-change fix that was correctly deferred rather than built mid-ticket, but was never actually applied. The epic's own Notes section has no consolidated accounting of every deferred item's disposition, which this entry's own verify text requires ("every review finding deferred during entries 1-11 is either resolved or explicitly re-parked in Notes with a reason").

**Approach:** No new behavior (per this entry's own description — distinguishing it from the two deferred items that are genuine features, not cleanup). (1) Fix `architecture-light-factory.md`'s Structural Seed file-tree comment and Capability→Architecture Map CAP-6/CAP-7 rows, which still attribute review/fix-loop to `implementation_graph.py` instead of the now-separate `review_graph.py`/`fix_loop_graph.py` (entries 9/10). (2) Append one consolidated decision-log entry to `epic-light-factory-pipeline.md`'s Notes, dispositioning all 7 `deferred-work.md` entries explicitly: 1 already resolved, 1 fixed here, and the remaining 5 re-parked with a one-line reason each — 2 blocked on GitHub plan tier (Team/Enterprise required for private-repo Environment required-reviewers), 1 blocked on a SPEC-level decision needing `bmad-correct-course`, 2 are genuine new features (AD-15 supersession-closing, real lint/security tooling) correctly out of scope for a no-new-behavior sweep, not abandoned. `deferred-work.md`'s own entries are left untouched (append-only convention, established since entry 1) — this entry only adds the epic-level accounting on top. (3) Confirm the full checks suite still passes (this entry's own verify text).

</frozen-after-approval>

## Implementation Notes

- Fixed `architecture-light-factory.md`'s Structural Seed file tree: brought the `factory/graph/`/`factory/scripts/` listing up to date with every script that actually exists today (`review_graph.py`, `fix_loop_graph.py`, `checkout_branch.py`, `commit_push_implementation.py`, `run_checks.py`, `post_evidence_summary.py`, `merge_story.py`) rather than narrowly touching only the one mis-attributed line — same category of fix, all docs-only.
- Fixed the Capability→Architecture Map: CAP-6 now points to `review_graph.py`, CAP-7 to `fix_loop_graph.py` (previously both said `implementation_graph.py`).
- Did not touch CAP-5/CAP-8/CAP-9's map rows (terse but not wrong) or `deferred-work.md` itself (append-only; its 7 entries are untouched) — only added the consolidated disposition entry to the epic's own Notes, per the Intent.
- Verified: full test suite 154/154, `python3 -m compileall factory -q` clean.

## Plan Change Log

## Review Triage Log

- **Quick lens, 2026-10-02: 1 finding, `patch` — fixed.** The new Structural Seed line for `post_summary.py` said `-- plan-approval`, mis-narrowing a module its own docstring and `post_evidence_summary.py`'s actual `import`/call confirm is shared by both gates — recreating the exact category of drift this ticket exists to fix. Corrected to state it's shared by both gates, reused directly by `analysis_graph.py` (plan-approval) and `post_evidence_summary.py` (evidence-approval); `post_evidence_summary.py`'s own line reworded to describe it as evidence-approval's gathering/rendering layer that posts *through* `post_summary.py`, not a parallel poster. No other findings — the rest of the file-tree additions, the CAP-6/CAP-7 fixes, and the epic Notes' full 7-entry disposition were all verified accurate.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass
- `python3 -m compileall factory -q` -- expected: exits 0

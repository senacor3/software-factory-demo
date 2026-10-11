---
title: 'Refactor sweep'
type: 'chore'
ticket: '6'
created: '2026-10-11'
status: 'built'
baseline_revision: '7322dd3e60bdb1abc7fed60ad41c9faf9c68398c'
route: 'oneshot'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Entries 1, 2, 3, and 5 of `epic-pipeline-hardening`, and the two stories merged through the pipeline along the way (PR #9, PR #10), left doc drift and deferred findings behind; AD-15 still describes a concurrency key the workflow has never used.

**Approach:** Close out what is cleanup — wording in the architecture doc, two workflow comments, one docstring — and give every deferred finding a disposition: resolved, or re-parked in `deferred-work.md` with a reason. No new behavior; anything that needs a behavior change is re-parked, not built.

</frozen-after-approval>

## Implementation Notes

Oneshot: comments and documents only, no executable line changed.

- `architecture-light-factory.md` — AD-15's Rule and the "concurrency" conventions row now state the real key (`light-factory-<story_file input>`), why it cannot be the slug, and that the guard therefore holds per input path, not per slug. The capability map's CAP-5 row names the checks config and where it is read from.
- `.github/workflows/light-factory.yml` — the concurrency comment and the `checks` comment. Comments only.
- `factory/scripts/run_checks.py` — two docstrings written by PR #9 claimed a story "cannot weaken its own checks"; they now say only the config is protected. Docstrings only.
- `factory/graph/fix_loop_graph.py` — the docstring no longer calls `security` "still a placeholder"; it is a check with no command in this repo.
- `deferred-work.md` — three new low, unowned entries (the PR left open when `analysis` fails after opening it; the two holes left in the checks guard; the concurrency guard holding per input path only).
- The epic's Notes carry the full disposition list.
- Not swept, on purpose: ticket 2's `deferred-work.md` entry has no `resolved:` line because its live proof is still open.

## Plan Change Log

## Review Triage Log

Pass 1 (2026-10-11, lens `quick`):

- medium, patched -- AD-15's new wording claimed the input path "stands for the slug". False: `derive_story_slug` accepts any directory named `stories` and any spelling, so several paths give one slug (verified by the reviewer). Reworded in AD-15, the conventions row, and the workflow comment to "per input path, not per slug".
- medium, patched -- the reworded Rule contradicted the text after it ("for a story-slug that still has a run in flight"). That clause now reads per `story_file`; the conventions row likewise.
- medium, patched -- the same-slug-different-path hole had no disposition. Now a `deferred-work.md` entry, which also corrects the overstated `resolved:` line ticket 3 added, and item 4 of the epic's Notes.
- medium, patched -- "so a story cannot weaken its own checks" overstated PR #9: `run_checks.py` itself still runs from the story branch. Corrected in the workflow comment, AD-6's addendum, and `run_checks.py`'s two docstrings; the remaining hole is in `deferred-work.md` and the epic's Notes item 3 no longer says "already resolved".
- low, patched -- the new entry on the PR left open after an `analysis` failure was imprecise about exit 4 and about when a later dispatch closes it. Reworded from `analysis_graph.py`.
- low, patched -- entry 2's open live proof was labelled "not a sweep item"; relabelled "re-parked, needs a live run", which is what the verify text asks for.
- false -- `lenses_ran` recorded before the triage log was written: an ordering artefact of the reviewer reading the plan mid-review; the log is this section.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass
- `uv run --with ruff ruff check factory/` -- expected: no findings

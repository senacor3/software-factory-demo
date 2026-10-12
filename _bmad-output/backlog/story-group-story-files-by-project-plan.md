---
title: 'Story files live in one sub-folder per project, and the pipeline accepts them there'
type: 'feature'
ticket: '3'
created: '2026-10-12'
status: done
route: 'oneshot'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: []
review_loop_iteration: 0
baseline_revision: '6490dffabcd6e2ad01239ce799d66f0b9745eaa1'
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** All story files sit side by side in `stories/`, whether they change the pipeline or the demo app, and intake accepts only `stories/<story-slug>.md`, so they cannot be grouped.

**Approach:** Move each story file into `stories/light-factory/` or `stories/freight-tenders/`. Intake accepts only `stories/<project>/<story-slug>.md` with those two project names, keeps the slug as the bare file name, and refuses a file name that exists in both project folders at dispatch time. AD-8, AD-15 and the workflow's `story_file` description state the new rule. Built by hand, not through the pipeline; records of past runs and the text of the two stories that set the earlier rule stay as written.

</frozen-after-approval>

## Implementation Notes

Oneshot: one function, its tests, a file move and three documentation passages; well under 100 changed lines.

- `factory/scripts/state_io.py`: `STORY_PROJECTS` names the two folders; `derive_story_slug` requires `stories/<project>/<name>.md` and refuses a name that exists in the other project folder. The given file still need not exist.
- `factory/scripts/tests/test_state_io.py`: accept/reject cases moved to the new form; added the same-name refusal (both directions) and the one-folder-only accept. The kebab and extension tests now also match on their message, so they cannot pass on the location error.
- `factory/graph/tests/test_analysis_graph.py`: the story path literal only; these tests pass the slug explicitly.
- `.github/workflows/light-factory.yml`: the `story_file` description only.
- Architecture AD-8 and AD-15 state the new form; AD-15 carries the dated reversal note.
- Nine story files moved with `git mv`; `validate-remark-and-offer-input` now cites its sibling at the new path.
- Left as written: `one-input-path-per-story-slug` still cites `stories/validate-story-file-location.md`. The ticket's criterion 5 and its boundary on that file's text disagree here; the boundary was followed.
- Surprise: another session is changing this working tree at the same time (the `static_analysis` check: `run_checks.py`, `post_evidence_summary.py`, and a new step in `light-factory.yml`). None of it was touched. `light-factory.yml` therefore holds two unrelated changes.
- Verified: 305 tests pass, ruff clean, the real `derive` command gives each of the nine moved stories its previous slug and exits 2 on `stories/trivial-test-story.md`.
- Not committed, at the user's request.

## Review Triage Log

Pass 1 (2026-10-12). Run inline in the building session at the user's request, not by a context-free subagent, so `lenses_ran` stays empty. Counts: high 0, medium 1, low 2, false 2.

- medium, left for the user: `STORY_PROJECTS` in `factory/scripts/state_io.py` names `freight-tenders`, so the generic pipeline script now knows the demo app's name. AD-6's addenda keep such per-repo facts in `.github/post-implementation-checks.yml`. The ticket fixed the two names but not where they are kept; moving them is a change of intent, not a patch.
- low, patched: three CLI test calls in `test_state_io.py` ran past 100 columns after the path grew; rewrapped.
- low, rejected: `one-input-path-per-story-slug` still cites its sibling at the old path. Left by the ticket's boundary on that file's text; see Implementation Notes.
- false: a run in flight on an old path would not be cancelled by a dispatch on the new path (different concurrency group). No run is in progress or waiting and no PR is open (`gh run list`, `gh pr list`, 2026-10-12).
- false: the new `story_file` description might break the workflow's YAML. It parses and reads back whole.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass
- `uv run --with ruff ruff check factory/` -- expected: no findings
- `uv run factory/scripts/state_io.py derive --story-file stories/<project>/<slug>.md --github-run-id 1` for each moved story -- expected: its previous slug

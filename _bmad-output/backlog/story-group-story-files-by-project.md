---
id: 3
type: story
title: "Story files live in one sub-folder per project, and the pipeline accepts them there"
parent: none
covers: []
after: []
assignee: ""
refined: true
hitl: false
risk: medium
estimate: ""
---

# Story files live in one sub-folder per project, and the pipeline accepts them there

## Description

All story files sit side by side in `stories/`, whether they change the pipeline
or the demo app. The pipeline's intake accepts only `stories/<story-slug>.md`, so
they cannot be grouped today. When this is done, each story file lives in
`stories/light-factory/` or `stories/freight-tenders/`, the pipeline accepts a
story file only in one of those two folders, and the story-slug is still the file
name alone. Because the slug no longer includes everything that tells two files
apart, intake also refuses a file name that exists in both folders. The
architecture document and the workflow's input description state the new rule.

## Acceptance Criteria

1. **A story file in a project folder is accepted**
   **Given** a kebab-case story file directly in `stories/light-factory/` or
   `stories/freight-tenders/`
   **When** the pipeline is dispatched with its path
   **Then** intake derives the story-slug as the file name without `.md`, the
   same slug the file had before it moved

2. **Other spellings of an accepted file give the same slug**
   **Given** an accepted story file
   **When** its path is given with a leading `./`, a doubled separator, or as an
   absolute path
   **Then** intake derives the same story-slug as for the plain relative path

3. **Any other location is refused at intake**
   **Given** a story file directly in `stories/`, in any other sub-folder of
   `stories/`, nested deeper than one project folder, or outside `stories/` or
   the repository
   **When** the pipeline is dispatched with its path
   **Then** intake fails before any branch or PR exists, with an error that
   names the path as given and states the accepted form

4. **A file name present in both project folders is refused**
   **Given** two story files with the same file name, one in each project folder
   **When** the pipeline is dispatched with either path
   **Then** intake fails before any branch or PR exists, with an error that
   names both files

5. **The existing story files are grouped**
   **Given** the nine story files that exist today
   **When** this ticket is done
   **Then** each lives in the project folder listed in Notes, none remains
   directly in `stories/`, and every path one story file gives for another
   points at the new location

6. **Earlier runs still belong to their story**
   **Given** a story that already has state directories, branches, or PRs from
   earlier runs
   **When** it is dispatched from its new path
   **Then** the new run uses the same story-slug, so supersession of its open PR
   and the clarification-round count work as they did before the move

7. **The documentation states the new rule**
   **Given** the architecture document's AD-8 and AD-15 and the workflow's
   `story_file` input description
   **When** this ticket is done
   **Then** each gives the accepted form as
   `stories/<project>/<story-slug>.md` with the two project names, AD-15 states
   the same-name refusal and why it is needed, no example in them shows a path
   that intake now refuses as accepted, and AD-15 carries a dated note that
   this reverses the earlier "no sub-folders" rule

## Boundaries

- Must not change: the kebab-case and `.md` rules for a story file name and
  their error messages; how the story-slug names the state directory, the
  branch, and the PR; the concurrency group being keyed on the raw `story_file`
  input; that the story file need not exist for a slug to be derived.
- Must not change: records of past runs. Committed state under `.factory/`, and
  dated entries in `deferred-work.md` and the initiative files that cite a story
  by its old path, stay as written.
- Must not change: the text of the two story files that set the earlier rule
  (`validate-story-file-location`, `one-input-path-per-story-slug`), apart from
  their move.

## References

- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-8 (story-slug derivation and the state directory) and AD-15 (the one-path-per-slug rule and the concurrency group)
- prior decision — stories/validate-story-file-location.md, Sub-folders (decided 2026-10-11): "grouping stories in folders is given up" to keep one story file mapped to one slug
- prior decision — stories/one-input-path-per-story-slug.md, Other spellings of the right file (decided 2026-10-11): other spellings of the accepted file are normalised and accepted
- deferred work — _bmad-output/initiative-light-factory/deferred-work.md, the entries resolved by `epic-pipeline-hardening` tickets 3 and 6 on the slug rule

## Notes

- Decision (2026-10-12): group under `stories/`, not inside `freight-tenders/`.
  One intake location stays, and `freight-tenders/` holds app code only.
- Decision (2026-10-12): the project folders are exactly `light-factory` and
  `freight-tenders`. A story file directly in `stories/` is refused, not kept as
  a third accepted form.
- Decision (2026-10-12): the story-slug stays the bare file name, with no
  project prefix. This keeps every existing state directory, branch, and PR
  attached to its story. The cost is criterion 4.
- The split. `freight-tenders`: `close-tender-from-detail-page`,
  `validate-remark-and-offer-input`, `validate-tender-creation-input`.
  `light-factory`: `distinct-exit-code-for-status-output-failure`,
  `one-input-path-per-story-slug`, `read-checks-config-from-target-branch`,
  `trivial-test-story`, `validate-story-file-location`, `wire-ruff-lint`.
- The intake rule and the file move must reach `main` in the same commit. A
  dispatch between the two fails at intake for every story.
- Paths the change touches: `factory/scripts/state_io.py` (`derive_story_slug`),
  `factory/scripts/tests/test_state_io.py`, `.github/workflows/light-factory.yml`
  (the `story_file` description only), and the story path used throughout
  `factory/graph/tests/test_analysis_graph.py`.
- Decision (2026-10-12): the same-name check looks only at the two project
  folders on disk at dispatch time. A file name that existed in the other folder
  in the past but was deleted does not count.
- Assumption: `AGENTS.md` and the READMEs need no change. None of them states
  where story files live today.
- Decision (2026-10-12): this ticket is built by hand, not dispatched through
  the pipeline. It needs no story file of its own under `stories/`.

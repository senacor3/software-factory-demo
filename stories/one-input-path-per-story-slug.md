# Accept exactly one input path per story-slug

## Problem

`derive_story_slug` in `factory/scripts/state_io.py` accepts any story file whose
immediate parent directory is named `stories`. Several input paths therefore give
the same slug: `stories/foo.md`, `./stories/foo.md`, `stories//foo.md` and
`docs/stories/foo.md` all give `foo`.

The workflow's `concurrency` group is keyed on the raw `story_file` input, so each
of those spellings is its own group. Two runs for the same slug can then be in
flight together, and each closes the other's PR when it opens its own (AD-15's
supersession works on the `light-factory/<story-slug>/` branch prefix).

## What to build

Make `derive_story_slug` accept a story file only when it is `stories/<slug>.md`
relative to the repository root, whatever spelling the path was given in.

- Resolve the given path against the working directory (the repository root when
  the pipeline runs), then express it relative to that directory. The result must
  be exactly `stories/<name>.md`.
- `stories/foo.md`, `./stories/foo.md`, `stories//foo.md` and an absolute path to
  that same file all give `foo`.
- `docs/stories/foo.md`, `stories/billing/foo.md`, `other/foo.md`, a bare `foo.md`,
  and a path that resolves outside the repository are rejected with a `ValueError`
  naming the path as given.
- The existing checks (`.md` extension, kebab-case name) stay as they are and keep
  their messages.
- Add tests to `factory/scripts/tests/test_state_io.py` in the style already used
  there, covering each spelling above. Existing tests must keep passing; adjust
  only those that pass a path the new rule rejects.
- Update AD-15 in
  `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md`:
  its Rule currently lists `docs/stories/foo.md` among the paths that still derive
  one slug. After this change only different spellings of the one accepted file do,
  each still in its own concurrency group (see the decision below).
- Do not edit `.github/workflows/light-factory.yml` — a commit touching that
  directory cannot be pushed by the pipeline's token.

## Other spellings of the right file (decided 2026-10-11)

A path that names the right file with a different spelling — `./stories/foo.md`,
`stories//foo.md`, or an absolute path to it — is **normalised and accepted**, not
rejected. This keeps the earlier decision in
`stories/validate-story-file-location.md`, which accepted `./stories/foo.md` and
an absolute path; nothing there is superseded or needs annotating.

Known and accepted: the workflow's concurrency group is taken from the raw input
before any code runs, so two spellings of one file are still two groups, and two
such runs in flight together can still close each other's PRs. This story removes
the other half of the finding — a different file under another `stories/`
directory sharing the slug — and leaves that one.

## Why

Recorded as an open finding in
`_bmad-output/initiative-light-factory/deferred-work.md` (the concurrency guard
holds per input path only), found in the review of ticket 6 of
`epic-pipeline-hardening`.

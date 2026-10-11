# Reject story files that are not under `stories/`

## Problem

`derive_story_slug` in `factory/scripts/state_io.py` builds the story-slug from the
story file's base name only. `stories/foo.md` and `other/foo.md` therefore both give
the slug `foo`. Since the pipeline closes every other open PR on the
`light-factory/<story-slug>/` branch prefix when it opens a new one, two such files
dispatched together can close each other's PRs. The architecture (AD-8) already says
a story file is `stories/<story-slug>.md`; the code just never checks it.

## What to build

Make `derive_story_slug` raise `ValueError`, with a message naming the offending
path, when the story file is not under a `stories/` directory. The existing checks
(`.md` extension, kebab-case name) stay as they are and keep their messages.

- `stories/foo.md` keeps working and still gives `foo`.
- `other/foo.md` and a bare `foo.md` are rejected.
- Add tests to `factory/scripts/tests/test_state_io.py` in the style already used
  there. Existing tests must keep passing; adjust only those that pass a path the
  new rule rejects.
- Do not edit `.github/workflows/light-factory.yml` — a commit touching that
  directory cannot be pushed by the pipeline's token.

## Sub-folders (decided 2026-10-11)

A story file in a sub-folder of `stories/` — for example `stories/billing/foo.md` —
is **rejected**. Only a file whose immediate parent directory is named `stories`
is accepted (`stories/foo.md`, also when given with a leading path such as
`./stories/foo.md` or `/repo/stories/foo.md`). Rejecting sub-folders is what keeps
one story file mapped to one slug; grouping stories in folders is given up for that.
Cover the sub-folder case with a test.

## Why

Recorded as an open finding in
`_bmad-output/initiative-light-factory/deferred-work.md` (concurrency key vs.
story-slug). Rejecting misplaced files at intake makes one story file map to one
slug, which closes the collision without touching the workflow's concurrency key.

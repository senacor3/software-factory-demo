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

Make one story-slug reachable through exactly one accepted input path, so the
concurrency group and the slug always correspond.

- `stories/foo.md` — relative to the repository root, no leading `./`, no doubled
  separators, no other directory in front — keeps working and gives `foo`.
- `docs/stories/foo.md` and any other path with a directory in front of `stories/`
  is rejected with a `ValueError` naming the path.
- The existing checks (`.md` extension, kebab-case name) stay as they are and keep
  their messages.
- Add tests to `factory/scripts/tests/test_state_io.py` in the style already used
  there. Existing tests must keep passing; adjust only those that pass a path the
  new rule rejects.
- Update AD-15 in
  `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md`:
  its Rule currently says the guard holds per input path, not per slug, and points
  at `deferred-work.md`. Once this is built, it holds per slug.
- Do not edit `.github/workflows/light-factory.yml` — a commit touching that
  directory cannot be pushed by the pipeline's token.

## Not decided

What should happen to a path that names the right file with a different spelling —
`./stories/foo.md`, `stories//foo.md`, or an absolute path such as
`/repo/stories/foo.md`?

- **Reject it**, with a message that shows the accepted spelling. Simple, and the
  concurrency group can never differ from the slug. It reverses an earlier
  decision: `stories/validate-story-file-location.md` (2026-10-11) explicitly
  accepted `./stories/foo.md` and `/repo/stories/foo.md`.
- **Normalise it** to `stories/foo.md` and accept it. Friendlier, but the workflow's
  concurrency group is taken from the raw input before any code runs, so two
  spellings would still land in two groups — the collision would remain.

This story does not choose. Do not pick one on the developer's behalf.

## Why

Recorded as an open finding in
`_bmad-output/initiative-light-factory/deferred-work.md` (the concurrency guard
holds per input path only), found in the review of ticket 6 of
`epic-pipeline-hardening`.

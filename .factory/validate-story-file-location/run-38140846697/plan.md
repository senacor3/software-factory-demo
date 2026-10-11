---
schema_version: 1
story_slug: validate-story-file-location
stage: analysis
status: ready-for-review
updated: 2026-10-11T12:51:42Z
---

## Proposal

Add a parent-directory check to `derive_story_slug` in `factory/scripts/state_io.py`. After the existing `.md` extension and kebab-case checks, require `Path(story_file).parent.name == "stories"`. If not, raise `ValueError` with a message naming the offending path. Because only the immediate parent is inspected, `stories/foo.md`, `./stories/foo.md` and `/repo/stories/foo.md` pass. `other/foo.md`, a bare `foo.md` (parent name is empty) and `stories/billing/foo.md` (parent is `billing`) are rejected. This matches the sub-folder decision recorded in the story. The extension and kebab-case checks keep their order and messages, so existing error behaviour is unchanged. The docstring is updated to say the file must be `stories/<slug>.md`. The `derive` CLI at state_io.py:252 calls this function, so it picks up the rule automatically. `.github/workflows/light-factory.yml` is not touched. Every existing test in test_state_io.py already uses a `stories/` path, so none should need adjusting.

## Subtasks

- In factory/scripts/state_io.py, add the immediate-parent-is-`stories` check to derive_story_slug, after the existing extension and kebab-case checks. Raise ValueError with a message that includes the path.
- Update the derive_story_slug docstring to state the `stories/<story-slug>.md` requirement and the sub-folder rejection.
- Add tests to factory/scripts/tests/test_state_io.py in the existing style (pytest.raises(ValueError) and plain asserts).
- Grep other tests and callers (factory/graph/tests, factory/scripts/tests, CLI usages) for story-file paths outside `stories/` and adjust only those the new rule rejects.
- Run the factory test suite (uv run --with pytest pytest factory/) to confirm everything passes.

## Tests

- derive_story_slug('other/foo.md') raises ValueError and the message contains 'other/foo.md'.
- derive_story_slug('foo.md') (bare file) raises ValueError.
- derive_story_slug('stories/billing/foo.md') raises ValueError (sub-folder case).
- derive_story_slug('./stories/foo.md') == 'foo'.
- derive_story_slug('/repo/stories/foo.md') == 'foo'.
- derive_story_slug('stories/foo.md') == 'foo' (existing valid test keeps passing).
- Existing .md-extension and kebab-case tests still pass with their original messages.
- CLI `derive --story-file other/foo.md` exits non-zero with an error naming the path, like the existing Not_Kebab CLI test.
- Full existing suite under factory/ still passes.

---
schema_version: 1
story_slug: validate-story-file-location
stage: analysis
status: awaiting-clarification
updated: 2026-10-11T12:49:11Z
---

## Proposal

Add a location check to `derive_story_slug` in `factory/scripts/state_io.py`. Keep the existing `.md` and kebab-case checks and their messages unchanged. After them, inspect the parent directory of the path: if no `stories` component is present in the right place, raise `ValueError(f"story file {str(story_file)!r} must be under a 'stories/' directory")`. `stories/foo.md` still returns `foo`. `other/foo.md` and a bare `foo.md` raise. Update the docstring, which currently says `<anything>/<story-slug>.md`, to say `stories/<story-slug>.md` (AD-8). The CLI `cmd_derive` already turns ValueError into exit code 2, so it needs no change. The workflow file is not touched.

The story leaves open whether sub-folders such as `stories/billing/foo.md` are allowed, and says to ask rather than choose. The check has two forms:
- Strict: `Path(story_file).parent.name == "stories"`. This rejects sub-folders and removes the same-base-name collision.
- Permissive: `"stories" in Path(story_file).parent.parts`. This accepts sub-folders but brings the collision back.

Implementation should wait for the answer. Neither form affects the other rules or the tests for the already-decided cases.

Existing tests all use `stories/...` paths, so none should need adjusting.

## Subtasks

- Get the human's decision on sub-folders of `stories/` (see open_questions) before writing the check.
- In `factory/scripts/state_io.py`, add the `stories/` location check to `derive_story_slug` after the existing `.md` and kebab-case checks, raising ValueError with a message that names the offending path.
- Update the `derive_story_slug` docstring to describe `stories/<story-slug>.md` instead of `<anything>/<story-slug>.md`.
- Add tests to `factory/scripts/tests/test_state_io.py` in the existing style (`pytest.raises(ValueError, match=...)` and direct asserts), including a sub-folder test that matches the decision.
- Add a CLI-level test that `derive --story-file other/foo.md` exits 2 with an error on stderr, mirroring the existing Not_Kebab test around line 278.
- Run the factory test suite and confirm the existing tests still pass unchanged.

## Tests

- `derive_story_slug('stories/foo.md') == 'foo'` (still works).
- `derive_story_slug('other/foo.md')` raises ValueError, and the message contains the path.
- `derive_story_slug('foo.md')` (bare file name) raises ValueError.
- A path like `other/stories-extra/foo.md` or `notstories/foo.md` is rejected, so only a real `stories` directory component counts.
- The sub-folder case `stories/billing/foo.md` behaves per the human's decision: it raises under the strict rule, or returns `foo` under the permissive rule.
- A `.txt` file outside `stories/` still raises the existing .md-extension message, and `other/Not_Kebab.md` still raises the kebab-case message, so the existing checks keep their messages.
- CLI: `state_io derive --story-file other/foo.md --github-run-id 999` exits 2 and prints `error:` to stderr.
- All existing tests in `test_state_io.py` pass unchanged.

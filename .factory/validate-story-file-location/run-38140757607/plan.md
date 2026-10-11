---
schema_version: 1
story_slug: validate-story-file-location
stage: analysis
status: ready-for-review
updated: 2026-10-11T12:50:27Z
---

## Proposal

Add a location check to `derive_story_slug` in `factory/scripts/state_io.py`. It will require `Path(story_file).parent.name == "stories"`, so only a file whose immediate parent directory is named `stories` is accepted. `stories/foo.md`, `./stories/foo.md` and `/repo/stories/foo.md` pass. `other/foo.md`, a bare `foo.md` (empty parent name) and `stories/billing/foo.md` (parent is `billing`) raise `ValueError`. The message names the offending path, in the same style as the existing messages (`{str(story_file)!r}`). The existing `.md` extension and kebab-case checks keep their messages. The new check runs after the extension check and before the kebab check, so inputs like `stories/Not_Kebab.md` still get their current error. The docstring is updated to say `stories/<story-slug>.md`. The CLI `derive` command already catches `ValueError` and exits 2, so it needs no change. `.github/workflows/light-factory.yml` is not touched. Existing tests, including `factory/graph/tests/test_analysis_graph.py`, already pass `stories/...` paths and should keep passing. A final grep for other callers or fixtures that pass non-`stories/` paths will confirm that.

## Subtasks

- In factory/scripts/state_io.py, update the derive_story_slug docstring to say the file must be stories/<story-slug>.md, with immediate parent directory named `stories`.
- Add the check Path(story_file).parent.name != 'stories' raising ValueError with a message naming the offending path (str(story_file)!r). Place it after the .md extension check and before the kebab-case check.
- Add tests to factory/scripts/tests/test_state_io.py in the existing style: other/foo.md rejected, bare foo.md rejected, stories/billing/foo.md rejected, ./stories/foo.md and /repo/stories/foo.md accepted giving 'foo'. Also assert the error message contains the offending path.
- Add a CLI test that `derive --story-file other/foo.md` exits 2 with the error on stderr, mirroring the existing Not_Kebab CLI test.
- Grep the repo for other derive_story_slug callers or fixtures using non-stories/ paths and adjust only those the new rule rejects.
- Run uv run --with pytest pytest factory/scripts/tests/test_state_io.py and the factory/graph tests.

## Tests

- derive_story_slug('stories/foo.md') == 'foo' (existing tests still pass).
- derive_story_slug('./stories/foo.md') == 'foo' and derive_story_slug('/repo/stories/foo.md') == 'foo'.
- derive_story_slug('other/foo.md') raises ValueError whose message contains 'other/foo.md'.
- derive_story_slug('foo.md') raises ValueError.
- derive_story_slug('stories/billing/foo.md') raises ValueError (sub-folder case).
- Existing extension/kebab-case rejections for stories/ paths keep their current messages.
- CLI: `state_io.py derive --story-file other/foo.md --github-run-id 999` returns exit code 2 and prints the error to stderr.

---
schema_version: 1
story_slug: validate-story-file-location
stage: analysis
status: ready-for-review
updated: 2026-10-11T14:11:57Z
---

## Proposal

Add a location check to `derive_story_slug` in `factory/scripts/state_io.py`. After the existing `.md` extension and kebab-case checks, require that the story file's immediate parent directory is named `stories`. Use `Path(story_file).parent.name != "stories"` to detect a violation. This accepts `stories/foo.md`, `./stories/foo.md` and `/repo/stories/foo.md`. It rejects `other/foo.md`, a bare `foo.md` (parent name is empty) and `stories/billing/foo.md` (parent is `billing`), as the story's sub-folder decision requires. A failure raises `ValueError` with a message that names the offending path, in the same style as the existing messages. The existing checks and their messages stay unchanged. The check goes last so that a file with a bad extension or name still gets its current error message. The CLI `derive` command already turns `ValueError` into a stderr message and exit code 2, so it needs no change. Update the docstring ("Expects `<anything>/<story-slug>.md`") to describe the new rule. No workflow file is touched (`.github/workflows/light-factory.yml` stays as is), and the concurrency key is left alone. All existing tests and callers already pass `stories/...` paths, so none should need adjusting. Other callers (the analysis graph tests) pass the slug explicitly or use `stories/foo.md`.

## Subtasks

- In `factory/scripts/state_io.py`, extend `derive_story_slug` to raise `ValueError` naming the path when `Path(story_file).parent.name != 'stories'`. Place the check after the extension and kebab-case checks so their messages are unchanged.
- Update the `derive_story_slug` docstring (and the nearby comments if needed) to state that the file must live directly in a `stories/` directory.
- Add tests to `factory/scripts/tests/test_state_io.py` in the existing style: accepted paths (`stories/foo.md`, `./stories/foo.md`, `/repo/stories/foo.md`), and rejected paths (`other/foo.md`, bare `foo.md`, `stories/billing/foo.md`). Assert that the error message contains the offending path.
- Add a CLI test that `derive --story-file other/foo.md --github-run-id 999` exits 2 with an error on stderr, modelled on the existing `Not_Kebab` CLI test.
- Run the full `factory/scripts/tests` and `factory/graph/tests` suites to confirm nothing else passes a path the new rule rejects. Adjust only the tests that do.

## Tests

- `derive_story_slug('stories/foo.md') == 'foo'`, and the same for `./stories/foo.md` and `/repo/stories/foo.md`.
- `derive_story_slug('other/foo.md')` raises `ValueError`, and the message contains `other/foo.md`.
- `derive_story_slug('foo.md')` raises `ValueError`.
- `derive_story_slug('stories/billing/foo.md')` raises `ValueError` (sub-folder case).
- A bad extension or non-kebab name in a wrong folder still gives the original extension or kebab-case message (check order is preserved).
- CLI `derive --story-file other/foo.md --github-run-id 999` exits 2 and prints an error to stderr.
- The existing `test_state_io.py` and `factory/graph/tests` suites still pass unchanged.

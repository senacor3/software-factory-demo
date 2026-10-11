---
schema_version: 1
story_slug: one-input-path-per-story-slug
stage: analysis
status: awaiting-clarification
updated: 2026-10-11T15:01:30Z
---

## Proposal

Tighten `derive_story_slug` in `factory/scripts/state_io.py` so a slug has one accepted input path: `stories/<slug>.md`, relative to the repo root. Today it only checks `Path(story_file).parent.name == "stories"`, which accepts `docs/stories/foo.md`, `./stories/foo.md`, `stories//foo.md` and absolute paths. The `.md` and kebab-case checks stay first and keep their messages. After them, the location check changes from "parent is named stories" to "the path is exactly `stories/<slug>.md`".

This part of the story is decided. `docs/stories/foo.md` and any other path with a directory in front of `stories/` raises a `ValueError` naming the path. `stories/foo.md` still returns `foo`.

The story deliberately leaves one thing undecided, and I have not chosen it. It is what to do with a path that names the right file under a different spelling (`./stories/foo.md`, `stories//foo.md`, `/repo/stories/foo.md`). The two options, rejecting or normalising to `stories/foo.md`, change the code, the error messages and the tests. The design therefore depends on the answer. The plan below is the shared work. The spelling-variant branch, its tests and the exact AD-15 wording wait for the human's answer.

The change to AD-15 in `architecture-light-factory.md` is also needed under either option. Its Rule says the guard holds per input path, not per slug, and points at `deferred-work.md`. It should say the guard now holds per slug. If normalising is chosen, the text must be honest that the workflow concurrency group is keyed on the raw `story_file` input. Two spellings would still land in two groups, so the collision would remain. `.github/workflows/light-factory.yml` must not be edited.

## Subtasks

- Get the human's decision on the spelling-variant question (reject or normalise) before implementing the variant branch.
- In `derive_story_slug` (`factory/scripts/state_io.py`), keep the `.md` and kebab-case checks first with their existing messages.
- Replace the `parent.name == "stories"` check with a check that the path is exactly `stories/<slug>.md`. Raise a `ValueError` naming the path for `docs/stories/foo.md` and any other path with a directory in front of `stories/`.
- Implement the decided handling of `./stories/foo.md`, `stories//foo.md` and absolute paths. If rejecting, the message shows the accepted spelling. If normalising, they are accepted and mapped to `stories/foo.md`.
- Update the `derive_story_slug` docstring, and check the `derive` CLI path in `state_io.py` for any wording that assumes `<anything>/stories/`.
- Check the other callers of `derive_story_slug` (`factory/graph/*`, `factory/scripts/*`) for call sites that pass paths the new rule rejects.
- In `factory/scripts/tests/test_state_io.py`, update `test_derive_story_slug_accepts_stories_directory`, which currently accepts `./stories/foo.md` and `/repo/stories/foo.md`. Add new tests in the same parametrized, `pytest.raises(..., match=...)` style.
- Update AD-15 in `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` so the Rule says the guard holds per slug. Remove or adjust the pointer to `deferred-work.md`, and mark the open finding in `deferred-work.md` as resolved if that is the convention.
- Leave `.github/workflows/light-factory.yml` untouched.

## Tests

- `derive_story_slug("stories/foo.md") == "foo"`, and `stories/story-v2.md` still gives `story-v2`.
- `docs/stories/foo.md`, `a/b/stories/foo.md` and `other/stories/foo.md` each raise `ValueError`, and the message contains the offending path.
- Existing wrong-location cases still raise: `other/foo.md`, `foo.md` and `stories/billing/foo.md`.
- The extension and kebab-case checks still run before the location check and keep their messages, e.g. `other/foo.txt` raises the `.md` error and `other/Not_Kebab.md` raises the kebab-case error.
- Spelling variants `./stories/foo.md`, `stories//foo.md` and `/repo/stories/foo.md` behave as the human decides: either `ValueError` with a message showing `stories/foo.md`, or all return `foo`.
- The `derive` CLI test for `stories/trivial-test-story.md` still passes, and the `Not_Kebab` CLI failure test is unchanged.
- The full `factory/scripts/tests` and `factory/graph/tests` suites still pass, which catches any caller that passed a now-rejected path.

---
schema_version: 1
story_slug: one-input-path-per-story-slug
stage: analysis
status: ready-for-review
updated: 2026-10-11T15:10:54Z
---

## Proposal

Replace the "parent directory is named stories" check in derive_story_slug (factory/scripts/state_io.py) with a repo-root-relative check. The existing .md extension and kebab-case checks stay first, with their current messages. After them, resolve the given path against the current working directory (Path(story_file).resolve()) and express it relative to Path.cwd().resolve(). Require the result to be exactly two parts: "stories" and "<name>.md". Resolving collapses ./, // and absolute spellings of the same file into one answer, so stories/foo.md, ./stories/foo.md, stories//foo.md and an absolute path to that file all give "foo". Anything else is rejected: docs/stories/foo.md, stories/billing/foo.md, other/foo.md, a bare foo.md, and a path outside the cwd (relative_to raises ValueError, which is caught and re-raised). The rejection is a ValueError naming the path as originally given (str(story_file)!r) and still mentioning 'stories/', so the existing match="stories" test pattern keeps working. The file need not exist. Update the docstring accordingly. Then update AD-15's Rule in architecture-light-factory.md. Drop docs/stories/foo.md from the list of paths that still derive one slug. State that only different spellings of the one accepted file (stories/foo.md, ./stories/foo.md, stories//foo.md, absolute path) still do, each in its own concurrency group because the group is taken from the raw input before any code runs. Do not edit .github/workflows/light-factory.yml, and do not annotate stories/validate-story-file-location.md. In tests, use monkeypatch.chdir(tmp_path) so the cwd-relative rule is deterministic. The existing parametrized test that passes the fixed absolute path /repo/stories/foo.md must be adjusted to build its absolute path from tmp_path.

## Subtasks

- In factory/scripts/state_io.py, rewrite the location check in derive_story_slug: resolve the path and the cwd, take relative_to(cwd), require parts == ('stories', name); on any mismatch or relative_to failure raise ValueError naming str(story_file) and requiring 'stories/<slug>.md' relative to the repository root. Keep the extension and kebab checks first and unchanged.
- Update derive_story_slug's docstring (and any module docstring mention) to describe the repo-root-relative rule and path normalisation.
- In factory/scripts/tests/test_state_io.py, adjust test_derive_story_slug_accepts_stories_directory: use monkeypatch.chdir(tmp_path) and replace '/repo/stories/foo.md' with str(tmp_path / 'stories' / 'foo.md'); add 'stories//foo.md'.
- Extend test_derive_story_slug_rejects_wrong_location with docs/stories/foo.md and a path resolving outside the cwd (e.g. '../stories/foo.md' or an absolute path under a different tmp dir), running under chdir(tmp_path) and asserting the given path appears in the message.
- Check other tests and callers (e.g. test_cli_derive_*, factory/graph tests, workflow-invoked scripts) for paths the new rule rejects, e.g. tests that call derive with absolute tmp paths or run from another cwd; adjust only those.
- Update AD-15's Rule in _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md as described, removing the docs/stories/foo.md example and the stale 'parent directory named stories' wording.
- Run the factory test suite (uv run --with pytest pytest factory/) and ruff to confirm nothing else regressed.

## Tests

- Accepts (cwd=tmp_path): stories/foo.md, ./stories/foo.md, stories//foo.md, and the absolute path str(tmp_path/'stories'/'foo.md') all return 'foo'.
- Rejects with ValueError whose message contains the path as given: docs/stories/foo.md, stories/billing/foo.md, other/foo.md, foo.md, and a path resolving outside the repo root (../stories/foo.md and an absolute path in another directory).
- Extension and kebab-case checks still run before the location check and keep their messages (existing test_derive_story_slug_extension_and_kebab_checks_run_before_location passes unchanged).
- Existing kebab-case, empty-slug, hyphen and digit tests still pass (they use stories/<name> relative to the repo root, so the test must run with cwd at a dir where that resolves; add an autouse chdir fixture if the test runner's cwd isn't the repo root).
- CLI: state_io.py derive with --story-file docs/stories/foo.md exits 2 with the error on stderr; with ./stories/foo.md prints story-slug=foo.

---
schema_version: 1
story_slug: validate-story-file-location
stage: analysis
status: ready-for-review
updated: 2026-10-11T12:59:29Z
---

## Proposal

Add a location check to derive_story_slug in factory/scripts/state_io.py. After the existing .md extension and kebab-case checks (so their messages are unchanged), require that Path(story_file).parent.name == "stories". If it isn't, raise ValueError with a message that names the offending path and says story files must be stories/<story-slug>.md. This uses the immediate-parent rule from the story's sub-folder decision. stories/foo.md, ./stories/foo.md and /repo/stories/foo.md all pass. other/foo.md, a bare foo.md (empty parent name) and stories/billing/foo.md (parent is billing) are rejected. The CLI derive command already catches ValueError, so a misplaced file fails intake with a clear error and no other code changes. Update the docstring, which currently says <anything>/<story-slug>.md. I checked the existing tests: every derive_story_slug and derive CLI call already uses a stories/... path, so none need adjusting. .github/workflows/light-factory.yml is not touched.

## Subtasks

- In factory/scripts/state_io.py derive_story_slug, add the parent-directory check (Path(story_file).parent.name == 'stories') after the existing extension and kebab-case checks, raising ValueError with a message that includes the offending path.
- Update the derive_story_slug docstring to say the file must be stories/<story-slug>.md, that sub-folders are rejected, and that leading path prefixes are fine.
- Add tests to factory/scripts/tests/test_state_io.py in the existing style (pytest.raises(ValueError), one small test per case).
- Run the full factory test suite to confirm the existing tests still pass.

## Tests

- test_derive_story_slug_rejects_file_outside_stories_dir: other/foo.md raises ValueError and the message contains the path.
- test_derive_story_slug_rejects_bare_filename: foo.md raises ValueError.
- test_derive_story_slug_rejects_stories_subfolder: stories/billing/foo.md raises ValueError.
- test_derive_story_slug_accepts_leading_path: ./stories/foo.md and /repo/stories/foo.md both give foo.
- CLI test: derive --story-file other/foo.md exits non-zero with an error on stderr, mirroring the existing Not_Kebab CLI test.
- Existing derive_story_slug tests (valid kebab-case, non-kebab, .md extension, hyphen rules, digits) keep passing unchanged.

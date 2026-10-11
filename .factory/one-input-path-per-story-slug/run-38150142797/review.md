---
schema_version: 1
story_slug: one-input-path-per-story-slug
stage: review
status: findings-open
updated: 2026-10-11T15:14:35Z
---

## Findings

- **factory/scripts/tests/test_state_io.py (CLI section, ~line 324)**: The plan's Tests list calls for CLI coverage: `state_io.py derive --story-file docs/stories/foo.md` exits 2 with the error on stderr, and `./stories/foo.md` prints `story-slug=foo`. Neither test was added. The only CLI location test still uses `other/foo.md`. The new rule is therefore not checked end to end through `main`. This is minor, because the function-level tests cover the same inputs.

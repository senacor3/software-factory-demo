---
schema_version: 1
story_slug: validate-story-file-location
stage: analysis
status: awaiting-clarification
updated: 2026-10-11T12:49:11Z
---

## Open Questions

- Should a story file in a sub-folder of `stories/` (e.g. `stories/billing/foo.md`) be accepted or rejected? Rejecting it forbids grouping stories in folders. Accepting it brings back the same-base-name collision between `stories/a/foo.md` and `stories/b/foo.md`. The story says not to choose without asking.

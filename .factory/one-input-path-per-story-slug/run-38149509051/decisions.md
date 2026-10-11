---
schema_version: 1
story_slug: one-input-path-per-story-slug
stage: analysis
status: awaiting-clarification
updated: 2026-10-11T15:01:30Z
---

## Open Questions

- What should happen to a path that names the right file under a different spelling (`./stories/foo.md`, `stories//foo.md`, `/repo/stories/foo.md`)? Option A: reject it, with a message showing the accepted spelling. This keeps the concurrency group equal to the slug, but it reverses the 2026-10-11 decision in `stories/validate-story-file-location.md`, which accepted `./stories/foo.md` and `/repo/stories/foo.md`. Option B: normalise it to `stories/foo.md` and accept it. This is friendlier, but the workflow's concurrency group is taken from the raw input before any code runs, so two spellings would still land in two groups and the collision would remain.
- If Option A is chosen, may the earlier decision in `stories/validate-story-file-location.md` be formally superseded, and should that story or its decision record be annotated?

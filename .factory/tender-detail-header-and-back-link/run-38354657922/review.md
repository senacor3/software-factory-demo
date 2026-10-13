---
schema_version: 1
story_slug: tender-detail-header-and-back-link
stage: review
status: findings-open
updated: 2026-10-13T06:15:16Z
---

## Findings

- **freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts**: The plan's tests list requires the back link to be present in the invalid-id state (non-numeric route id, which takes the NaN early-return path in ngOnInit). No spec navigates to a non-numeric id, so that state has no back-link coverage. The load-error (404) state is covered.

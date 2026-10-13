---
schema_version: 1
story_slug: seed-demo-tenders
stage: review
status: unresolved-after-cap
updated: 2026-10-13T14:45:52Z
fix_cycle: 2
---

## Findings

- **freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoProfileGatingTest.java:62-69**: The 409 test is meant to prove that seeded tender 5 rejects offers with BidDeadlinePassedException. It picks the first tender whose bidDeadline is before today, and seeded tenders 7 (AWARDED) and 8 (CLOSED) also have past deadlines. findAll() has no ordering guarantee, so the test can select tender 7 or 8. It would still pass there, because a non-open tender rejects offers with a 409 too, so it would not show that tender 5 is rejected for its passed deadline. Select the tender by status OPEN plus a past deadline, or by the seeded commodity or position, so it targets tender 5.

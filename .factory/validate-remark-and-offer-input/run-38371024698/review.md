---
schema_version: 1
story_slug: validate-remark-and-offer-input
stage: review
status: findings-open
updated: 2026-10-13T08:47:54Z
---

## Findings

- **freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/TenderControllerTest.java (invalidRemarkOrOfferOnClosedTenderReturns400NotConflict)**: The test is named and planned as proving that an invalid request to a closed tender returns 400 rather than 409. It never stubs the service to throw the closed-tender exception, and it never sets up a closed tender. It is effectively a duplicate of the other 400 tests. verifyNoInteractions does show the service isn't called. But the 400-over-409 precedence the plan asked for is never exercised against a service that would actually return 409.

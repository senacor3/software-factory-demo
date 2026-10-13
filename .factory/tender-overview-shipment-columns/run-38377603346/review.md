---
schema_version: 1
story_slug: tender-overview-shipment-columns
stage: review
status: findings-open
updated: 2026-10-13T09:56:04Z
---

## Findings

- **freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/TenderServicePersistenceTest.java**: The plan's tests list requires a @DataJpaTest asserting that listing N tenders with offers issues a constant number of queries (no N+1). No such test exists (no Hibernate statistics or statement counting anywhere in the backend tests). The @EntityGraph on findAll/findByStatus in TenderRepository is therefore unverified, and the main performance requirement of the backend subtasks could regress silently.

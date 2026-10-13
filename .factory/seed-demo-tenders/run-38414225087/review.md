---
schema_version: 1
story_slug: seed-demo-tenders
stage: review
status: findings-open
updated: 2026-10-13T14:44:45Z
---

## Findings

- **freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoDataSeederTest.java**: The plan's profile-gating test is missing. It called for a @SpringBootTest without the `demo` profile that has no DemoDataSeeder bean and returns an empty list from GET /api/tenders, and a second one with @ActiveProfiles("demo") that returns the eight tenders. The only test class is a @DataJpaTest with `demo` forced on and the seeder imported by hand. Nothing checks that @Profile("demo") keeps the seeder out of the default run, which is the main safety property of the change.
- **freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoDataSeederTest.java:119-128**: The plan said seeded tender 5 must reject a new offer with BidDeadlinePassedException, and that this surfaces as HTTP 409 through the API via MockMvc. The test only checks the service-level exception. The 409 mapping is not exercised, so that part of the acceptance criteria is unverified.

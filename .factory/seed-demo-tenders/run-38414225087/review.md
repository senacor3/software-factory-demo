---
schema_version: 1
story_slug: seed-demo-tenders
stage: review
status: findings-open
updated: 2026-10-13T14:43:11Z
---

## Findings

- **freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoDataSeederTest.java**: The plan's profile-gating test is missing. It called for a @SpringBootTest without the `demo` profile (no DemoDataSeeder bean, GET /api/tenders returns an empty list) and one with @ActiveProfiles("demo") (returns eight tenders). The only test class is a @DataJpaTest that forces the profile on and imports the seeder directly. Nothing checks that the @Profile("demo") gating keeps the default, test and CI runs empty.
- **freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/DemoDataSeederTest.java:119**: The plan asked for the seeded tender 5 to reject a new offer with HTTP 409 through the API (MockMvc). The test only calls TenderService.addOffer and asserts BidDeadlinePassedException. It does not check the exception-handler mapping to 409, so the planned end-to-end check is not covered.

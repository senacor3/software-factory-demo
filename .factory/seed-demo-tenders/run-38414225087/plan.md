---
schema_version: 1
story_slug: seed-demo-tenders
stage: analysis
status: ready-for-review
updated: 2026-10-13T14:33:24Z
---

## Proposal

Add one backend component, DemoDataSeeder, in the flat `tender` package. It is annotated @Profile("demo") and @Component, takes TenderRepository, TenderService and Clock by constructor injection, and implements ApplicationRunner so it runs once at startup. Without the `demo` profile the bean does not exist, so tests, CI and the default run stay empty. No endpoint and no new config property are added.

On run() it returns immediately if tenderRepository.count() > 0. Otherwise it computes today = LocalDate.now(clock) (the Europe/Berlin Clock bean from ClockConfiguration) and builds the eight tenders from the story table with the public Tender and Offer constructors. Postal codes, weights, loading meters, supplier names, amounts and German commodity, remark and note texts are fixed values chosen by the implementer. Offers and remarks are attached with Tender.addOffer and Tender.addRemark (plain mutators that do not enforce API rules), then each tender is saved through TenderRepository.

Building data through the domain model and repository is what lets tender 5 carry a bid deadline of yesterday and an already-expired offer, without touching the API validators, TenderService.addOffer or ClockConfiguration. No validation rule is weakened or made profile-conditional. Everything else is chosen to satisfy the API rules: pickup before delivery, offer delivery not before pickup, validUntil in the future except the one deliberately expired offer. Tender 1 has one offer delivering after the requested delivery date. Tender 2 is temperature-controlled (2 to 8 C) with a reefer. Tender 3 has dangerousGoods and ADR class 3. Tender 4 has a null pallet count. Tender 6 uses Currency.CHF. At least three tenders get a remark and at least two offers get a note.

Tender 7 and 8 are saved with their offers and remarks first (the story requires that order). The seeder then calls tenderService.awardTender(tender7Id, idOfLowerAmountOffer), reading the id from the saved entity, and tenderService.closeTender(tender8Id), so their state matches what the application itself produces.

Finally, update freight-tenders/README.md: document `mvn spring-boot:run -Dspring-boot.run.profiles=demo` in the backend section and use it in "Running both together".

## Subtasks

- Read the existing tender package (Tender, Offer, Remark, TenderService, validators, EquipmentType, Currency, Address) to confirm constructor signatures and which field combinations the API validators accept.
- Create DemoDataSeeder (@Component, @Profile("demo"), ApplicationRunner) in freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/ with constructor-injected TenderRepository, TenderService and Clock (private final fields only).
- Implement the guard: do nothing if tenderRepository.count() > 0.
- Build tenders 1-6 with deadlines today+3, +5, today, +7, yesterday, +4, with the loads, equipment, ADR, temperature, pallet and currency values from the story table. Add offers (including the late-delivering one on tender 1 and the expired one on tender 5) and at least three remarks and two offer notes, in German, and save via the repository.
- Build and save tenders 7 and 8 with their offers and remark, then call TenderService.awardTender with the lower-amount offer's id for tender 7 and TenderService.closeTender for tender 8.
- Update freight-tenders/README.md: document the `demo` profile command in the backend section and use it in 'Running both together'.
- Write DemoDataSeederTest, run `mvn -B verify`, `mvn spotless:apply` then `mvn spotless:check`, and `mvn spotbugs:check`, and fix any findings.

## Tests

- DemoDataSeederTest (@DataJpaTest, importing TenderService, DemoDataSeeder and FixedClockConfiguration): after run(), findAll returns 8 tenders, with 6 OPEN, 1 AWARDED and 1 CLOSED.
- With the fixed clock, bid deadlines of tenders 1-6 equal today+3, +5, today, +7, yesterday, +4, and tender 5 has exactly one offer with validUntil before today.
- Tender field checks: tender 2 temperature-controlled with a reefer, tender 3 dangerous goods with ADR class 3, tender 4 with null palletCount, tender 6 with currency CHF, and tender 1 has one offer whose delivery date is after the tender's requested delivery date.
- Tender 7 is AWARDED and its awardedOffer is the lower-amount of its two offers. Tender 8 is CLOSED, has a null awardedOffer, one offer and one remark.
- At least three tenders have remarks and at least two offers have notes.
- Idempotence: calling run() when tenders already exist leaves the count unchanged and adds nothing.
- Profile gating: a @SpringBootTest without the `demo` profile has no DemoDataSeeder bean and GET /api/tenders returns an empty list. With @ActiveProfiles("demo") it returns the eight tenders.
- Seeded tender 5 rejects a new offer via TenderService.addOffer with BidDeadlinePassedException (HTTP 409 through the API, MockMvc).
- Existing test suite still passes with `mvn -B verify`, and `mvn spotless:check` and `mvn spotbugs:check` pass.

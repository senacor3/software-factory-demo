---
title: 'Tender domain model & persistence'
type: 'feature'
ticket: 2
created: '2026-10-12'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: 'a6e61042c137e22798cdf7d8ea2ad31253712179'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The backend scaffold (entry 1) has no domain model yet — there's nowhere to record a tender, its remarks, or supplier offers.

**Approach:** Add JPA entities for `Tender` (with `origin`/`destination`/`status`), `Remark`, and `Offer` as child records, persisted via Spring Data JPA, with a repository and a unit test proving the create → add remark/offer → close → reload lifecycle round-trips correctly.

## Boundaries & Constraints

**Always:** Lives under `com.senacor.freighttenders.tender`, atop entry 1's scaffold; persisted via Spring Data JPA; English identifiers/docs throughout.

**Never:** Do not enforce the open/closed rule here — ticket 1.3 owns that at the service layer (its own description: "enforcing that remarks/offers can only be added to an open tender"). No REST endpoints, no service layer, no controller — those are entries 3/4. No migration tooling (Flyway/Liquibase) — `ddl-auto` is enough for a demo excluded from production deployment per the epic's Boundaries. Do not touch `freight-tenders/frontend/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Full lifecycle | New `Tender`, a remark and an offer added, then closed | Reloading via the repository shows `status=CLOSED` with the remark and offer both present and linked back to the tender | No error expected |
| Empty collections | New open `Tender`, no remarks/offers, saved | Reloading shows `status=OPEN` with empty remark/offer collections | No error expected |

</frozen-after-approval>

## Code Map

- `freight-tenders/backend/pom.xml` -- Spring Boot `4.1.1` parent already set; add `spring-boot-starter-data-jpa` (unaffected by the 4.1.1 web-stack starter split that renamed `-web`/`-test`, confirmed live against Maven Central) and `com.h2database:h2` (runtime).
- `freight-tenders/backend/src/main/java/com/senacor/freighttenders/health/HealthController.java` -- existing feature-package precedent (`com.senacor.freighttenders.<feature>`); the tender domain follows the same shape under `.tender`.
- `freight-tenders/backend/src/test/java/com/senacor/freighttenders/health/HealthControllerTest.java` -- existing JUnit 5 + Spring Boot Test precedent (`spring-boot-starter-webmvc-test` already pulls in generic `spring-boot-starter-test`, so `@DataJpaTest` needs no new test dependency beyond H2 on the classpath).
- No `application.yml`/`.properties` exists yet in `backend/src/main/resources/` -- needs creating for the datasource/ddl config.

## Tasks & Acceptance

**Execution:**
- [x] `freight-tenders/backend/pom.xml` -- add `spring-boot-starter-data-jpa` + `com.h2database:h2` (runtime scope) -- gives the domain model somewhere to persist to
- [x] `freight-tenders/backend/src/main/resources/application.yml` -- `spring.datasource.url: jdbc:h2:mem:freighttenders;DB_CLOSE_DELAY=-1`, `spring.jpa.hibernate.ddl-auto: update` -- stable in-memory datasource, schema generated from entities
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/TenderStatus.java` -- enum `OPEN`, `CLOSED`
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/Tender.java` -- JPA entity: `id`, `origin`, `destination`, `status` (defaults to `OPEN`), `remarks`/`offers` (`@OneToMany(mappedBy = "tender", cascade = ALL, orphanRemoval = true)`); `addRemark(Remark)`/`addOffer(Offer)` maintain the bidirectional link, `close()` sets `status = CLOSED` -- plain state mutators, no rule guard (see Never)
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/Remark.java` -- JPA entity: `id`, `text`, `tender` (`@ManyToOne`)
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/Offer.java` -- JPA entity: `id`, `supplierName`, `amount` (`BigDecimal`), `tender` (`@ManyToOne`)
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/TenderRepository.java` -- `interface TenderRepository extends JpaRepository<Tender, Long>`
- [x] `freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/TenderRepositoryTest.java` -- `@DataJpaTest`: covers both I/O matrix rows -- full lifecycle (create, add remark + offer, close, save, reload via the repository, assert status + children) and the empty-collections case

**Acceptance Criteria:**
- Given a new `Tender` with a remark and an offer added and then closed, when reloaded via `TenderRepository`, then its `status` is `CLOSED` and both the remark and offer are present, each linked back to the tender.
- Given a new `Tender` with no remarks or offers, when saved and reloaded, then it loads with `status=OPEN` and empty remark/offer collections.

## Implementation Notes

The Code Map's assumption that `spring-boot-starter-webmvc-test` already covered `@DataJpaTest` didn't hold: Spring Boot 4.1.1 split the JPA test slice into its own `spring-boot-starter-data-jpa-test` module (package moved to `org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest`), the same split pattern entry 1 hit for `-web`/`-test`. Added that one extra test-scoped dependency to `pom.xml`; everything else matches the plan as written.

Verified: `mvn -B verify` -- `BUILD SUCCESS`, 3/3 tests pass (`TenderRepositoryTest` both matrix rows + the existing `HealthControllerTest`). `mvn spotless:check` -- clean after one `spotless:apply` pass for formatting.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 1, medium: 0, low: 1, false: 0, maybe-false: 0

- `TenderRepositoryTest.java` (both test methods) -- fake reload: `save()` then `findById()` run inside the same persistence context with `GenerationType.IDENTITY`, so Hibernate returns the cached in-session object instead of issuing a `SELECT` (confirmed via SQL logging: no `select` statement for either `findById` call). The identity-equality assertions (`.isEqualTo(reloaded)`) only pass because of this, not because the mapping is correct. **high**, route: **patch** -- the plan's own Intent and both I/O-matrix rows explicitly require a genuine reload; a real mapping defect could ship undetected.
- `Tender.java` `getRemarks()`/`getOffers()` -- return the live internal `List` by reference, so a caller can bypass `addRemark`/`addOffer` and leave a child's back-reference unset, breaking the "linked back to the tender" invariant. Not triggered by the current diff, but named harm: ticket 1.3's upcoming service layer will hold references to these same entities. **low**, route: **patch** -- trivial, no public surface added (an unmodifiable view is a narrower surface, not a wider one).

Both patches applied by the implementer: `TenderRepositoryTest` now autowires `TestEntityManager` and calls `flush()`+`clear()` between `save()` and `findById()` (confirmed via Hibernate SQL log: real `SELECT`s now fire), with back-reference assertions changed from object identity to id comparison; `Tender.getRemarks()`/`getOffers()` now return `Collections.unmodifiableList(...)`. Full re-verification after patching: `mvn -B verify` -- `BUILD SUCCESS`, 3/3 tests pass; `mvn spotless:check` -- clean.

## Design Notes

`Tender.close()`/`addRemark()`/`addOffer()` are plain state mutators that keep the bidirectional JPA association consistent -- they deliberately do not guard the open/closed invariant. Ticket 1.3's own description assigns that enforcement to the service layer it introduces, so gating it here would duplicate (and risk diverging from) that ticket's design.

H2 in-memory with a fixed URL (`DB_CLOSE_DELAY=-1`) rather than Spring Boot's default anonymous embedded DB -- keeps the connection alive across the app's lifetime without needing a real external database, consistent with this app never being deployed to production (epic Boundaries).

## Verification

**Commands:**
- `cd freight-tenders/backend && mvn -B verify` -- expected: `BUILD SUCCESS`, `TenderRepositoryTest` passes (both matrix rows) alongside the existing `HealthControllerTest`
- `cd freight-tenders/backend && mvn spotless:check` -- expected: no formatting violations

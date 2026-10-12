---
title: 'Create/close-tender API + enforce the open/closed rule'
type: 'feature'
ticket: 3
created: '2026-10-12'
status: done
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '97cf2ce7a2bd9fb5543ae04215ee87095c21b593'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Entry 2's `Tender`/`Remark`/`Offer` entities exist but are unreachable from outside the codebase, and nothing yet enforces the epic's one non-trivial rule: remarks/offers can only be added to an open tender.

**Approach:** Add `POST /api/tenders` and `POST /api/tenders/{id}/close`, backed by a `TenderService` that also gains `addRemark`/`addOffer` methods enforcing the open/closed rule (rejecting with a clear error on a closed tender) — the service layer owns this guard, not the entity (entry 2's own Design Notes already assign it here).

## Boundaries & Constraints

**Always:** Builds on entry 2's `Tender`/`Remark`/`Offer`/`TenderRepository`; the open/closed guard lives in `TenderService`, raised as a dedicated exception; English identifiers/docs throughout.

**Never:** No `GET` endpoints and no remark/offer REST endpoints — that's entry 4 ("Tender overview + detail API"), which also re-enforces this rule at the HTTP layer once those endpoints exist. No bean-validation framework — not required by this ticket's scope. Do not touch `freight-tenders/frontend/`.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Create tender via API | `POST /api/tenders` with origin + destination | `201 Created`, body has `id`/`origin`/`destination`/`status=OPEN` | No error expected |
| Close tender via API | `POST /api/tenders/{id}/close` on an open tender | `200 OK`, body `status=CLOSED` | No error expected |
| Add remark/offer, open tender (service) | `TenderService.addRemark`/`addOffer` on an open tender | Remark/offer added and the tender saved | No error expected |
| Add remark/offer, closed tender (service) | `TenderService.addRemark`/`addOffer` on a closed tender | Call rejected, tender left unchanged | `TenderClosedException` naming the tender id, with a clear message |

</frozen-after-approval>

## Code Map

- `Tender.java` -- `addRemark`/`addOffer`/`close()` are plain mutators with no guard (entry 2's own design); getters return unmodifiable views.
- `TenderRepository.java` -- `JpaRepository<Tender, Long>`, reused as-is.
- `health/HealthController.java` + `HealthControllerTest.java` -- precedent for the `/api/...` prefix and the `@WebMvcTest`-style controller test shape.
- Confirmed in the local Maven cache (matches Spring Boot `4.1.1`): Boot's own `@MockBean` is gone; `spring-test-7.0.9.jar` only has `org.springframework.test.context.bean.override.mockito.MockitoBean` -- use that for the controller test's mocked service.

## Tasks & Acceptance

**Execution:**
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/TenderClosedException.java` -- `RuntimeException` with a message naming the tender id -- the epic's one non-trivial rule, as a dedicated, catchable type
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/TenderService.java` -- `createTender(origin, destination)`, `closeTender(id)`, `addRemark(id, text)`, `addOffer(id, supplierName, amount)`; the latter two load the tender, throw `TenderClosedException` if `status == CLOSED`, otherwise delegate to `Tender.addRemark`/`addOffer` and save
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/CreateTenderRequest.java` -- request record: `origin`, `destination`
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/TenderResponse.java` -- response record: `id`, `origin`, `destination`, `status`, with a `from(Tender)` factory -- avoids serializing the entity directly (its children's back-reference to the parent would recurse infinitely over JSON)
- [x] `freight-tenders/backend/src/main/java/com/senacor/freighttenders/tender/TenderController.java` -- `@RestController` at `/api/tenders`: `POST ""` (create, `201`) and `POST "/{id}/close"` (`200`), both returning `TenderResponse`
- [x] `freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/TenderServiceTest.java` -- Mockito-mocked `TenderRepository`: covers the two service-layer matrix rows (open-tender add succeeds; closed-tender add rejected with `TenderClosedException`)
- [x] `freight-tenders/backend/src/test/java/com/senacor/freighttenders/tender/TenderControllerTest.java` -- `@WebMvcTest(TenderController.class)` with `@MockitoBean TenderService`: covers the two API matrix rows (create, close)

**Acceptance Criteria:**
- Given a `POST /api/tenders` request with an origin and destination, when it completes, then the response is `201` with the created tender's `id`/`origin`/`destination` and `status=OPEN`.
- Given an open tender, when `POST /api/tenders/{id}/close` is called, then the response is `200` with `status=CLOSED`.
- Given a closed tender, when `TenderService.addRemark` or `addOffer` is called against it, then it throws `TenderClosedException` and the tender's remarks/offers are unchanged.

## Implementation Notes

Implemented exactly as planned, with all seven files new (no existing files modified -- `Tender.java` and the frontend are untouched). `TenderService.addRemark`/`addOffer` first load the tender via `tenderRepository.findById`, throwing a plain `IllegalArgumentException` for an unknown id (not part of this ticket's matrix, but needed since `findById` returns `Optional`) before checking `status == CLOSED` and throwing `TenderClosedException(tender.getId())`; the guard runs before any mutation, so a closed tender's remarks/offers are provably left unchanged (asserted directly in `TenderServiceTest`, not just via the exception type).

One implementation wrinkle not called out in the Code Map: with Mockito's `@ExtendWith(MockitoExtension.class)` + field-level `@Mock`, a field initializer on another field (`tenderService = new TenderService(tenderRepository)`) runs during instance construction, before the extension injects the mock -- `tenderRepository` is still `null` at that point, causing a `NullPointerException` in all four `TenderServiceTest` methods. Fixed by moving the `TenderService` construction into a `@BeforeEach` method, which runs after Mockito's injection.

Verified: `cd freight-tenders/backend && mvn -B verify` -- `BUILD SUCCESS`, 9/9 tests pass (`TenderServiceTest` 4, `TenderControllerTest` 2, plus the existing `TenderRepositoryTest` 2 and `HealthControllerTest` 1). `mvn spotless:check` -- clean (after one `spotless:apply` pass for formatting).

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 1, medium: 0, low: 1, false: 0, maybe-false: 0

- `TenderService.createTender`/`closeTender` -- never exercised by any test with real logic: `TenderControllerTest` mocks `TenderService` entirely (only checks controller wiring), and `TenderServiceTest` only covers `addRemark`/`addOffer`. A regression (swapped fields, a dropped `save()` call) would pass `mvn verify` undetected, despite AC1/AC2 both describing this exact behavior. **high**, route: **patch** -- the same category of gap as ticket 1.2's "fake reload" finding; fix is adding direct `TenderServiceTest` coverage for both methods against the existing mocked `TenderRepository`.
- `TenderControllerTest.createTenderReturns201WithOpenTender` -- doesn't assert `$.id`, though AC1 names it as part of the response contract. **low**, route: **patch** -- trivial: give the mocked `Tender` an id and add the assertion.

Both patches applied: `TenderServiceTest` gained `createTenderBuildsOpenTenderAndSavesIt` (asserts the built `Tender` + the exact instance passed to `save()` via `ArgumentCaptor`) and `closeTenderClosesAndSavesTheLoadedTender`; `TenderControllerTest` now sets the mocked `Tender`'s id via `ReflectionTestUtils.setField` (no setter exists -- JPA-generated) and asserts `$.id`. Full re-verification after patching: `mvn -B verify` -- `BUILD SUCCESS`, 11/11 tests pass; `mvn spotless:check` -- clean.

## Design Notes

DTOs, not the JPA entity, cross the HTTP boundary -- `Remark`/`Offer` hold a back-reference to their parent, so serializing the entity graph directly would recurse infinitely. Remarks/offers in the response body are entry 4's job ("detail API").

The guard lives in `TenderService`, not `Tender` -- entry 2's Design Notes already assigned it here.

`TenderServiceTest` mocks `TenderRepository` rather than hitting a real database -- the guard is pure business logic, and entry 2 already proved the persistence mapping is correct.

## Verification

**Commands:**
- `cd freight-tenders/backend && mvn -B verify` -- expected: `BUILD SUCCESS`, `TenderServiceTest` + `TenderControllerTest` pass alongside the existing suite
- `cd freight-tenders/backend && mvn spotless:check` -- expected: no formatting violations

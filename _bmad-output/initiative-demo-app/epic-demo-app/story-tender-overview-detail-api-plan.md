---
title: 'Tender overview + detail API'
type: 'feature'
ticket: 4
created: '2026-10-12'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '81eeaf1ad412f71a0959cc5123678dc442b349ba'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Tenders created via entry 3's API can't be listed or inspected, and entry 3's `addRemark`/`addOffer` service methods are unreachable from HTTP — nor is their rejection of a closed tender yet mapped to a client-meaningful status.

**Approach:** Add `GET /api/tenders` (optionally filtered by status), `GET /api/tenders/{id}` (full detail with remarks/offers), and `POST /api/tenders/{id}/remarks`/`/offers` exposing entry 3's existing service methods — plus a `@RestControllerAdvice` mapping `TenderClosedException` to `409` and a new `TenderNotFoundException` to `404`, re-enforcing entry 3's rule at the HTTP layer.

## Boundaries & Constraints

**Always:** Reuses entry 3's `TenderService.addRemark`/`addOffer` unchanged (already enforce the rule); DTOs cross the HTTP boundary, never the entities; English identifiers/docs throughout.

**Never:** No frontend changes. No new business rules beyond re-enforcing entry 3's existing one at the HTTP layer. No pagination/sorting on the list endpoint — not required by this ticket's scope.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| List tenders, filtered | `GET /api/tenders?status=OPEN` with both open and closed tenders existing | `200`, only open tenders returned | No error expected |
| Tender detail | `GET /api/tenders/{id}` on a tender with a remark and an offer | `200`, body nests both under the tender's fields | No error expected |
| Add remark/offer, open tender, via API | `POST /api/tenders/{id}/remarks` or `/offers` on an open tender | `201` with the created remark/offer | No error expected |
| Add remark/offer, closed tender, via API | Same, on a closed tender | Rejected, nothing added | `409`, body names the closed tender |
| Unknown tender id | `GET /api/tenders/{id}`, or either `POST .../remarks`/`/offers`, for a nonexistent id | Rejected | `404`, body names the missing id |

</frozen-after-approval>

## Code Map

- `TenderController.java` -- existing create/close endpoints at `/api/tenders`; this ticket adds `GET ""`, `GET "/{id}"`, `POST "/{id}/remarks"`, `POST "/{id}/offers"` to the same controller.
- `TenderService.java` -- `addRemark`/`addOffer` already enforce the guard (entry 3), reused as-is; `getTenderOrThrow` currently throws `IllegalArgumentException` -- swap for the new `TenderNotFoundException` so the advice below can map it safely (a generic `IllegalArgumentException` can't be mapped globally without risking unrelated catches); add `listTenders(Optional<TenderStatus>)`.
- `TenderRepository.java` -- add `findByStatus(TenderStatus)` (Spring Data derived query).
- `TenderResponse.java` -- reused as-is for the list endpoint (its `id`/`origin`/`destination`/`status` shape is already the overview).
- `Tender.java`/`Remark.java`/`Offer.java` -- reused as-is (entry 2).

## Tasks & Acceptance

**Execution:**
- [x] `tender/TenderNotFoundException.java` -- `RuntimeException` naming the missing tender id
- [x] `tender/TenderService.java` -- `getTenderOrThrow` throws `TenderNotFoundException`; add `listTenders(Optional<TenderStatus> status)` delegating to `findByStatus`/`findAll`
- [x] `tender/TenderRepository.java` -- add `List<Tender> findByStatus(TenderStatus status)`
- [x] `tender/RemarkResponse.java` + `tender/OfferResponse.java` -- response records: `(id, text)` / `(id, supplierName, amount)`
- [x] `tender/AddRemarkRequest.java` + `tender/AddOfferRequest.java` -- request records: `(text)` / `(supplierName, amount)`
- [x] `tender/TenderDetailResponse.java` -- `id`/`origin`/`destination`/`status` + `remarks`/`offers` lists, `from(Tender)` factory
- [x] `tender/TenderExceptionHandler.java` -- `@RestControllerAdvice`: `TenderClosedException` -> `409`, `TenderNotFoundException` -> `404`, both with a small `{message}` body
- [x] `tender/TenderController.java` -- `GET ""` (optional `status` query param), `GET "/{id}"` (detail), `POST "/{id}/remarks"` + `POST "/{id}/offers"` (`201`, returning the created child)
- [x] `tender/TenderServiceTest.java` -- add `listTenders` coverage (filtered + unfiltered), covering a gap this plan introduces rather than inherits
- [x] `tender/TenderControllerTest.java` -- add coverage for all five matrix rows

**Acceptance Criteria:**
- Given both open and closed tenders exist, when `GET /api/tenders` is called with no filter, then both come back, and with `status=OPEN` only the open ones do.
- Given a tender with one remark and one offer, when `GET /api/tenders/{id}` is called, then the response nests both under the tender's own fields.
- Given an unknown tender id, when `GET /api/tenders/{id}`, `POST .../remarks`, or `POST .../offers` is called, then the response is `404`.

## Implementation Notes

Added `TenderService.getTender(Long id)` as a thin public wrapper around the existing private `getTenderOrThrow` -- not spelled out verbatim in the plan's task list, but necessary plumbing for the `GET /{id}` endpoint; one-line delegation, no new logic.

Verified: `mvn -B verify` -- `BUILD SUCCESS`, 23 tests pass (12 controller, 8 service, 2 repository, 1 health). `mvn spotless:check` -- clean after one `spotless:apply` pass.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 0, medium: 1, low: 0, false: 0, maybe-false: 0

- `TenderController.addRemark`/`addOffer`'s "last element = newly created child" logic -- relies on `findById` and `save` inside `TenderService` sharing one persistence context (true today only because of Spring Boot's `spring.jpa.open-in-view=true` default; confirmed via `grep -rn Transactional` returning nothing in `TenderService.java` and a real app startup showing the open-in-view warning). No test exercises this against the real `TenderRepository` with an already-persisted tender gaining a second remark/offer -- every existing test either mocks `TenderRepository` (trivially preserves list order, proves nothing about real Hibernate merge/collection behavior) or never calls `addRemark`/`addOffer` after a save+reload. If `open-in-view` is ever disabled -- a common hardening step Spring Boot's own startup log nudges toward -- this would silently regress. **medium**, route: **patch** -- not broken today, but the same category of "mocked tests mask real-persistence-dependent behavior" gap already flagged (and fixed) in tickets 1.2 and 1.3; fix is a real-repository-backed test, not a design change.

Patch applied: new `TenderServicePersistenceTest` (`@DataJpaTest` + `@Import(TenderService.class)`, a real `TenderRepository`/Hibernate context, not mocked) proves `addRemark`/`addOffer` append the new child as the last element after real persistence. Full re-verification after patching: `mvn -B verify` -- `BUILD SUCCESS`, 25/25 tests pass; `mvn spotless:check` -- clean.

## Design Notes

The controller builds the created-remark/offer response from the last element of the `Tender` returned by `addRemark`/`addOffer` (unchanged from entry 3), rather than changing those methods to return the child directly -- avoids touching already-reviewed, tested service methods. Safe because it's the same in-memory list just mutated, not a fresh DB reload, so the newly-added child is reliably last.

A single `@RestControllerAdvice` maps both domain exceptions to HTTP status, rather than a per-endpoint try/catch -- one place doing exactly this ticket's job ("re-enforcing entry 3's rule at the HTTP layer").

## Verification

**Commands:**
- `cd freight-tenders/backend && mvn -B verify` -- expected: `BUILD SUCCESS`, all tests (existing + new) pass
- `cd freight-tenders/backend && mvn spotless:check` -- expected: no formatting violations

---
schema_version: 1
story_slug: validate-remark-and-offer-input
stage: analysis
status: ready-for-review
updated: 2026-10-13T08:42:46Z
---

## Proposal

Extend the Bean Validation already wired for CreateTenderRequest to the two remaining request records. In AddRemarkRequest, annotate `text` with `@NotBlank`. In AddOfferRequest, annotate `supplierName` with `@NotBlank`, and `amount` with `@NotNull` and `@DecimalMin("0.01")`. `@DecimalMin` is inclusive by default, which gives the "at least 0.01" bound, and it treats null as valid, so a missing amount fails only `@NotNull`. In TenderController, add `@Valid` to the `@RequestBody` parameter of `addRemark` and `addOffer`, as `createTender` already does. Spring then raises MethodArgumentNotValidException before the controller body runs, so TenderService is never called. The open/closed check lives in the service, so an invalid request to a closed tender returns 400 with no side effect. The existing TenderExceptionHandler mapping already produces `{error, message, path, timestamp, violations}`, so no new handler or error shape is needed. Valid requests are unaffected: they still return 201, and a valid request to a closed tender still returns 409. The frontend is unchanged. Documentation: `freight-tenders/README.md` has no error paragraph today, only an endpoint table. Add a short paragraph after the table saying that the three POST endpoints that take a body (create tender, add remark, add offer) return `400` with `{error, message, path, timestamp, violations}` on invalid input, alongside the existing 404 (unknown tender) and 409 (closed tender) cases. Also update the stale policy line in `freight-tenders/backend/AGENTS.md` ("Wired for CreateTenderRequest only ... don't have it yet") and the matching note in the frontend AGENTS.md, which says client-side validation covers what the backend does not yet. Both sit inside managed bmad blocks that a refresh may overwrite, so treat those edits as best-effort.

## Subtasks

- Add `@NotBlank` to `text` in AddRemarkRequest.java (import jakarta.validation.constraints.NotBlank).
- Add `@NotBlank` to `supplierName`, and `@NotNull` plus `@DecimalMin("0.01")` to `amount`, in AddOfferRequest.java (imports from jakarta.validation.constraints).
- Add `@Valid` to the `@RequestBody` parameters of `addRemark` and `addOffer` in TenderController.java.
- Add controller tests to TenderControllerTest for the 400 cases and the closed-tender cases (see tests).
- Add a paragraph after the endpoint table in freight-tenders/README.md describing the 400/404/409 error responses and the `violations` array, covering all three request types.
- Update the stale validation notes in freight-tenders/backend/AGENTS.md (Policy) and freight-tenders/frontend/AGENTS.md (Forms convention).
- Run `mvn -B verify`, `mvn spotless:check` (apply with `spotless:apply` if needed) and `mvn spotbugs:check` in freight-tenders/backend.

## Tests

- TenderControllerTest: POST /api/tenders/{id}/remarks with blank text, whitespace-only text, and a missing text field ({}) each return 400. The body has error/message/path/timestamp, `violations` contains field `text`, and verifyNoInteractions(tenderService).
- TenderControllerTest: POST /api/tenders/{id}/offers with blank supplierName returns 400 with a violation for `supplierName`, and the service is never called.
- TenderControllerTest: POST offers with a missing amount, zero amount, negative amount, and 0.00 each return 400 with a violation for `amount`.
- TenderControllerTest: POST offers with `{}` returns 400 with violations for both `supplierName` and `amount`.
- TenderControllerTest: POST offers with amount exactly 0.01 and a non-blank supplier returns 201, to prove the inclusive boundary.
- TenderControllerTest: an invalid remark or offer to a closed tender returns 400 (not 409) and the service is never invoked.
- Regression: the existing valid remark and offer 201 tests and the 404/409 tests (including their absence of a `violations` key) keep passing unchanged, and the TenderService tests are untouched.
- Build gates: `mvn -B verify`, `mvn spotless:check`, `mvn spotbugs:check` pass.

---
schema_version: 1
story_slug: validate-tender-creation-input
stage: analysis
status: ready-for-review
updated: 2026-10-12T13:50:32Z
---

## Proposal

Add Bean Validation to the create-tender endpoint, all within the existing flat `tender/` package. (1) Add `spring-boot-starter-validation` to `freight-tenders/backend/pom.xml`. (2) Annotate the `origin` and `destination` components of `CreateTenderRequest` with `@NotBlank`. `@NotBlank` also rejects null, so a missing field and a blank field both fail validation. (3) Add `@Valid` to the `@RequestBody` parameter of `TenderController.createTender`, so an invalid request is rejected by Spring before `TenderService` is called. The controller stays free of try/catch. (4) In `TenderExceptionHandler`, add an `@ExceptionHandler(MethodArgumentNotValidException.class)` that returns 400 in the existing `{error, message, path, timestamp}` shape. Extend `ErrorResponse` with an optional `violations` list of `{field, message}` entries, one per failed field error. This matches the `violations` array that the backend AGENTS.md documents for 400s. Annotate `violations` with `@JsonInclude(NON_NULL)` so the existing 404/409 bodies stay unchanged. (5) Update the backend AGENTS.md policy line that says validation is "not yet wired anywhere" and that the starter isn't a dependency, since this change makes it stale. Scope is limited to `CreateTenderRequest`, as the story says. `AddOfferRequest` and `AddRemarkRequest` are left alone. A malformed or absent JSON body (`HttpMessageNotReadableException`) is outside this story.

## Subtasks

- Add the spring-boot-starter-validation dependency to freight-tenders/backend/pom.xml
- Add @NotBlank to origin and destination in CreateTenderRequest
- Add @Valid to the @RequestBody parameter of TenderController.createTender
- Extend TenderExceptionHandler.ErrorResponse with an optional violations list (field, message), omitted from JSON when null
- Add a MethodArgumentNotValidException handler to TenderExceptionHandler returning 400 with per-field violations
- Add controller tests for the new behavior in TenderControllerTest
- Update the stale validation policy line in freight-tenders/backend/AGENTS.md
- Run mvn -B verify and mvn spotless:check, and fix any formatting with mvn spotless:apply

## Tests

- TenderControllerTest: POST /api/tenders with a blank origin returns 400, the body has error/message/path/timestamp, violations lists field 'origin', and tenderService.createTender is never invoked (verifyNoInteractions)
- TenderControllerTest: POST with a blank destination returns 400 and violations lists field 'destination'
- TenderControllerTest: POST with origin and destination missing (empty JSON object {}) returns 400 with violations for both fields
- TenderControllerTest: POST with null or whitespace-only values returns 400
- TenderControllerTest: the existing createTenderReturns201WithOpenTender still passes, so a valid request creates a tender as before
- TenderControllerTest: existing 404 and 409 responses do not include a violations key
- Full mvn -B verify and mvn spotless:check pass

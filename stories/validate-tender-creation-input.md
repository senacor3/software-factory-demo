# Validate tender creation input

## Problem

`POST /api/tenders` accepts any `CreateTenderRequest` — `origin`/`destination` can
be blank, and there's no feedback to the caller beyond whatever an empty string or
downstream failure produces. The backend's own `AGENTS.md` already requires Bean
Validation at the API boundary for new or changed request DTOs, and none of the
three existing request records have it yet.

## What to build

Add Jakarta Bean Validation to `CreateTenderRequest` (`origin` and `destination`
must be non-blank) and wire it into `TenderController.createTender` so an invalid
request is rejected before it reaches `TenderService`. Add the
`spring-boot-starter-validation` dependency. A validation failure returns
`400 Bad Request`, using the same error-response shape the rest of the API already
uses (`{error, message, path, timestamp}` from `TenderExceptionHandler`), with
field-level detail for which constraint failed.

## Why

Closes a gap the backend's own `AGENTS.md` (Policy section) already names: Bean
Validation at the API boundary is required for new/changed request DTOs, and
`CreateTenderRequest` doesn't have it.

## Acceptance

- `POST /api/tenders` with a blank or missing `origin`/`destination` returns `400`,
  not `500` and not a tender created with blank fields.
- A valid request still creates a tender exactly as today.
- Existing tests keep passing; the new behavior has test coverage.

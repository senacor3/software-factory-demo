# Validate remark and offer input

## Problem

`POST /api/tenders/{id}/remarks` and `POST /api/tenders/{id}/offers` accept any
request body. A remark can be blank; an offer can have a blank supplier name, or
a missing, zero, or negative amount. The Angular forms block these cases, but
the API is the boundary, and anything that calls it directly can store them.
`CreateTenderRequest` was given Bean Validation in an earlier story
(`stories/validate-tender-creation-input.md`); `AddRemarkRequest` and
`AddOfferRequest` were not, and the backend's own `AGENTS.md` notes validation
is "wired for `CreateTenderRequest` only".

## What to build

Add Jakarta Bean Validation to the two remaining request records and enforce it
in `TenderController`:

- `AddRemarkRequest.text` must be non-blank.
- `AddOfferRequest.supplierName` must be non-blank.
- `AddOfferRequest.amount` must be present and at least `0.01` -- the same lower
  bound the frontend's offer form already applies.

An invalid request is rejected with `400 Bad Request` before it reaches
`TenderService`, using the response shape `TenderExceptionHandler` already
produces for an invalid create request: `{error, message, path, timestamp}` plus
a `violations` array naming each failed field. No new error shape and no new
handler -- the existing `MethodArgumentNotValidException` mapping covers it.

The frontend needs no change: its forms already prevent these submissions.
Update `freight-tenders/README.md`'s error paragraph so the `400` case covers
all three request types, not only tender creation.

## Why

Closes the gap the earlier validation story left open, so every write endpoint
of the tender API rejects bad input at the boundary instead of trusting the one
client that happens to check first.

## Acceptance

- A remark request with a blank or missing `text` returns `400` with a
  `violations` entry for `text`, and no remark is stored.
- An offer request with a blank or missing `supplierName`, or a missing, zero,
  or negative `amount`, returns `400` with a `violations` entry for each failed
  field, and no offer is stored.
- Validation runs before the open/closed check has any side effect: an invalid
  request to a closed tender never adds anything.
- Valid remark and offer requests behave exactly as today (`201`, same response
  body), and a valid request to a closed tender still returns `409`.
- Existing tests keep passing; the new behavior has test coverage, and
  `mvn -B verify` and `mvn spotless:check` pass.

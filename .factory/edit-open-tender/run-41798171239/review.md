---
schema_version: 1
story_slug: edit-open-tender
stage: review
status: findings-open
updated: 2026-11-04T08:28:45Z
---

## Findings

- **freight-tenders/backend/src/test**: The plan's tests list has about 10 backend PUT cases and none exist. These include 200 with the update persisted, a 400 per create rule, past-date handling, 404/409 ordering, locked fields (including currency), 13.60 vs 13.6 and absent vs null, expired-only offers, and extending a passed bidDeadline so addOffer works again. A grep for `updateTender`, `put(` and `TenderFieldsLocked` in the backend tests finds nothing. The check order, the locked-field comparison and the 'today' rules for changed dates are therefore unverified.
- **freight-tenders/frontend/src/app/tender-edit/ (no tender-edit.spec.ts)**: The plan requires a tender-edit.spec covering loading, load-error, non-numeric id, not-editable, prefill, Speichern gating, locked-fields notice and disabled controls, past-date validation, success navigation, 409 and generic error alerts, and Abbrechen/back link. No such spec file exists.
- **freight-tenders/frontend/src/app/tender-detail/tender-detail.spec.ts**: The plan calls for tests that the edit-tender link is present for an open tender with href /tenders/:id/edit and absent for awarded and closed tenders. A grep for `edit-tender` finds it only in tender-detail.html, so the spec has no such tests.
- **freight-tenders/frontend/src/app/tender-api.spec.ts**: The plan requires a test that update() sends PUT /api/tenders/{id} with the full body. A grep found only 2 matches for PUT-related terms in this file, so its coverage of update() should be confirmed against the plan.

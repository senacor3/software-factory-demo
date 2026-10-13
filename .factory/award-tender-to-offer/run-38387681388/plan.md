---
schema_version: 1
story_slug: award-tender-to-offer
stage: analysis
status: ready-for-review
updated: 2026-10-13T11:05:25Z
---

## Proposal

Add an AWARDED lifecycle state across backend, frontend and docs, following existing patterns.

Backend: add AWARDED to TenderStatus and an awarded-offer reference to Tender (ManyToOne or offer id column) with an award(Offer) mutator. TenderService.awardTender(tenderId, offerId) checks in the story's order: tender exists (TenderNotFoundException, 404), offer exists in that tender (new OfferNotFoundException, 404), tender is OPEN (409), offer validUntil not before LocalDate.now(clock) (new OfferExpiredException, 409). rejectIfClosed becomes a "not OPEN" check so remarks and offers on awarded tenders return 409. closeTender rejects only AWARDED with 409 and keeps closed-to-closed as today. TenderController gets POST /api/tenders/{id}/offers/{offerId}/award returning TenderDetailResponse (200). TenderExceptionHandler maps the new exceptions to the existing error shape. TenderDetailResponse gains awardedOfferId; TenderResponse gains awardedSupplierName and awardedAmount (null unless awarded). The status filter already works via findByStatus.

Frontend: extend the status type and tender-api with awardTender(). In tender-detail, add a last "Vergeben" column on open tenders (compact modifier class beside btn-secondary; hidden for offers whose validUntil is before the local date), a single-row in-place confirm state ("Zuschlag bestätigen"/"Abbrechen") held in a signal, in-flight disabling, a role="alert" German error under the offers table on failure, and on success update without reload: pill "Vergeben", awarded row first and labelled "Zuschlag", other rows empty, close button removed, add-forms disabled, new explanation line with focus moved to it. In tender-overview, rename the second table "Abgeschlossene Ausschreibungen", feed it AWARDED+CLOSED tenders, add a sortable "Status" column (sorted by German label), and show "Zuschlag: supplier amount" on the Angebote cell's second line for awarded tenders. Add status-pill-awarded styling.

Docs: update freight-tenders/README.md, EXPERIENCE.md and DESIGN.md (pill token, Colors section amended to allow a third status pill, Do's and Don'ts) as listed in the story.

## Subtasks

- Backend: add AWARDED to TenderStatus; add awarded offer reference to Tender plus award(Offer) mutator
- Backend: add OfferNotFoundException, a 409 not-open/expired exception(s), and map them in TenderExceptionHandler
- Backend: implement TenderService.awardTender with the specified check order; make rejectIfClosed reject any non-OPEN tender; make closeTender reject AWARDED with 409
- Backend: add POST /api/tenders/{id}/offers/{offerId}/award to TenderController returning TenderDetailResponse
- Backend: add awardedOfferId to TenderDetailResponse and awardedSupplierName/awardedAmount to TenderResponse (null unless awarded)
- Frontend: add AWARDED to the status type, awarded fields to models/test data, and awardTender() to tender-api
- Frontend: add compact button modifier class and status-pill-awarded style next to existing styles
- Frontend detail: Vergeben column, in-place confirm state, in-flight disabling, error alert, awarded-state rendering (pill, Zuschlag row first, close button gone, forms disabled, explanation line with focus)
- Frontend overview: split OPEN vs AWARDED+CLOSED, rename second table, sortable Status column by German label, Zuschlag line in Angebote cell
- Update freight-tenders/README.md, EXPERIENCE.md and DESIGN.md as specified
- Add/update backend and frontend tests; run mvn verify, spotless:check, spotbugs:check and the frontend check commands

## Tests

- TenderServiceTest: awarding an offer of an open tender sets AWARDED and the awarded offer; unknown tender/offer and offer of another tender give not-found; closed or awarded tender gives conflict; expired offer (validUntil yesterday) gives conflict while validUntil today succeeds; tender unchanged in each failure case; award works after the bid deadline
- TenderServiceTest: addRemark, addOffer and closeTender on an awarded tender throw and leave it AWARDED; closing an already closed tender behaves as before
- TenderControllerTest: POST award returns 200 with awardedOfferId; 404 and 409 cases use the error shape; GET /api/tenders?status=AWARDED filters; list response carries awardedSupplierName/awardedAmount, null for non-awarded
- TenderServicePersistenceTest/TenderRepositoryTest: awarded offer persists and reloads
- tender-api.spec: awardTender POSTs to the correct URL
- tender-detail.spec: Vergeben shown only for non-expired offers on open tenders; confirm/Abbrechen flow with only one row in confirm state; buttons disabled in flight; failure shows role=alert German error and tender stays open; success shows Vergeben pill, Zuschlag row first, no close button, disabled forms, explanation text and focus on it; no actions on closed/awarded tenders
- tender-overview.spec: awarded and closed tenders in the second table with correct headline, Status column pills and sorting by German label; awarded Angebote cell shows Zuschlag supplier and amount; open table unchanged
- Existing specs updated for the extra column and renamed table heading

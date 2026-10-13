# Award a tender to one of its offers

Depends on `stories/freight-tenders/offer-terms-and-bid-deadline.md` and
`stories/freight-tenders/tender-overview-shipment-columns.md`.

## Problem

A tender ends by being closed, and that is all the app records. Whether a
carrier got the job, and which one at what price, is not stored: the dispatcher
writes it into a remark. The outcome of a tender is the one fact everybody
looks for afterwards, and it is free text.

## What to build

A third tender status, `AWARDED`, reached by awarding the tender to one of its
offers.

### Backend

- `POST /api/tenders/{id}/offers/{offerId}/award` sets the tender's status to
  `AWARDED`, records the awarded offer and returns the tender detail (`200`).
- Only an `OPEN` tender can be awarded; otherwise `409`. An offer that does not
  exist or belongs to another tender returns `404`. An offer whose `validUntil`
  is before today cannot be awarded and returns `409`.
- An awarded tender behaves like a closed one: adding a remark or an offer
  returns `409`. Closing an awarded tender returns `409` and leaves it
  `AWARDED`.
- `TenderDetailResponse` gains `awardedOfferId`. `TenderResponse` gains
  `awardedSupplierName` and `awardedAmount`. All three are `null` unless the
  tender is awarded.
- `GET /api/tenders?status=AWARDED` filters like the other two statuses.

### Frontend: detail page

- On an open tender, each offer row whose offer has not expired gets a
  "Vergeben" action (`btn-secondary`, compact) in a new last column.
- Awarding is not reversible and the app has no modals, so it is confirmed in
  place: selecting "Vergeben" replaces that row's action with "Zuschlag
  bestätigen" and "Abbrechen". Only one row can be in this state at a time.
  "Abbrechen" restores the row.
- While the request is in flight both buttons are disabled. A failure shows a
  German error below the offers table with `role="alert"` and the tender stays
  open.
- On success, without a reload: the status pill reads "Vergeben", the awarded
  row shows "Zuschlag" in the action column and every other row shows nothing
  there, the close button disappears, both add-forms are disabled, and the
  explanation line reads "Diese Ausschreibung wurde vergeben, daher können
  keine weiteren Bemerkungen oder Angebote hinzugefügt werden." Focus moves to
  that line, as it does after closing.
- The awarded row is the first row of the offers table regardless of sorting.

### Frontend: overview

- The second table is headed "Abgeschlossene Ausschreibungen" and lists
  awarded and closed tenders together. It gains a last column "Status" with
  the pill "Vergeben" or "Geschlossen", sortable. The open table is unchanged.
- For an awarded tender, the second line of the "Angebote" cell reads
  "Zuschlag:" plus supplier name and amount instead of the lowest amount.

### Status pill

`AWARDED` is labelled "Vergeben" and gets its own pill, `status-pill-awarded`:
`{colors.primary-container}` background, `{colors.on-primary-container}` text.
`DESIGN.md` currently allows blue for the primary action only and names two
status colors; both rules are amended to cover this third status pill and
nothing else.

### Documentation

- `freight-tenders/README.md`: the tender description, the endpoint table and
  both route rows.
- `EXPERIENCE.md`: Information Architecture, the "Status pill" row, a
  Component Patterns row for the in-place confirmation, State Patterns rows
  "Awarded tender" and "Award in flight / failed", and Flow 1's ending.
- `DESIGN.md`: the pill token, the Colors section and the Do's and Don'ts.

### Clarifications

- Awarding is allowed before and after the bid deadline. The deadline only
  stops new offers.
- Order of checks for the award endpoint: tender exists (`404`), offer exists
  and belongs to the tender (`404`), tender is `OPEN` (`409`), offer has not
  expired (`409`). An offer whose `validUntil` is today has not expired.
- Closing an already closed tender behaves as it does today; only closing an
  awarded tender is new and returns `409`.
- Which exception types back the new `409` and `404` responses is the
  implementer's choice, as long as they are mapped in `TenderExceptionHandler`
  to the existing error shape.
- The overview keeps loading all tenders in one call and splitting them in the
  frontend: `OPEN` goes to the first table, `AWARDED` and `CLOSED` to the
  second.
- Sorting the second table by "Status" orders by the German label.
- "Compact" for the row buttons means reduced padding so the row height does
  not grow; it is a shared modifier class next to `btn-secondary`.
- Whether an offer has expired is decided in the frontend from `validUntil`
  and the browser's local date; the backend's `409` stays authoritative.

### Implementation choices

Anything this story does not specify -- class and method names, how a rule or
query is implemented, how components and styles are split, test structure --
is the implementer's choice. Follow the conventions in
`freight-tenders/backend/AGENTS.md` and `freight-tenders/frontend/AGENTS.md`
and prefer the simplest option; none of it needs a decision from the story
author.

## Why

Awarding is what a tender is for. Recording it as data lets the app answer the
question every finished tender raises -- who got it, and for how much -- and
gives the status model a real lifecycle instead of a single switch.

## Acceptance

- Awarding an offer of an open tender returns `200`; the tender is `AWARDED`
  with that `awardedOfferId`, and the list response carries the supplier name
  and amount.
- Awarding on a closed or already awarded tender returns `409`; an offer id
  from another tender returns `404`; an expired offer returns `409`. In each
  case the tender is unchanged.
- Adding a remark or offer to an awarded tender, and closing it, return `409`.
- On the detail page, "Vergeben" followed by "Zuschlag bestätigen" awards the
  tender and switches the page to the awarded state without a reload;
  "Abbrechen" changes nothing.
- An expired offer has no "Vergeben" action, and closed or awarded tenders show
  none at all.
- A failed award shows a German error and leaves the tender open and usable.
- The overview lists the awarded tender under "Abgeschlossene Ausschreibungen"
  with the "Vergeben" pill and "Zuschlag:" plus supplier and amount.
- The pill text is real text in all three states; no state is conveyed by color
  alone.
- All new UI text is German; assertions go through `data-testid`.
- Existing tests keep passing or are updated; the new behavior has test
  coverage; the backend and frontend check commands pass.

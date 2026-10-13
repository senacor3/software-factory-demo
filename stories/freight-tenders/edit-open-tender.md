# Edit an open tender

Depends on `stories/freight-tenders/tender-shipment-data-and-create-form.md`,
`stories/freight-tenders/offer-terms-and-bid-deadline.md` and
`stories/freight-tenders/award-tender-to-offer.md`.

## Problem

A tender cannot be changed after it has been created. A typo in the weight, a
pickup that moves by a day or a bid deadline that needs two more days all end
the same way: the dispatcher closes the tender and types all sixteen fields
again, and any remarks recorded so far stay behind on the closed one.

## What to build

An open tender can be edited through the form it was created with. Backend and
frontend change together. Once a tender has offers, the data those offers were
priced on is locked and only the two dates that do not invalidate a price stay
editable.

### Backend

- `PUT /api/tenders/{id}` takes the same body as `POST /api/tenders` -- the
  complete shipment data, not a partial patch -- replaces the tender's data
  and returns the tender as `TenderResponse` (`200`).
- `id`, `status`, remarks, offers and `awardedOfferId` are not part of the
  body and are not changed by an edit.
- An unknown id returns `404`. A tender that is not `OPEN` returns `409` and
  is unchanged.
- Every field rule and cross-field rule of `POST /api/tenders` applies, with
  one difference for the two "today or later" rules:
  - `pickupDate` and `bidDeadline` must be today or later **only if the
    request changes them**. A date that equals the stored value is accepted
    even when it is in the past, so a tender whose bid deadline passed
    yesterday can still have its commodity corrected.
  - The relative rules always apply: `deliveryDate` not before `pickupDate`,
    `bidDeadline` not after `pickupDate`.
- Violations return `400` in the existing
  `{error, message, path, timestamp, violations}` shape, under the same field
  names as on create.

### Locked fields once offers exist

When the tender has at least one offer, an edit may change only
`deliveryDate` and `bidDeadline`. Every other field must equal the stored
value; otherwise the request returns `409` in the existing error shape and the
tender is unchanged. The message names the locked fields that differ.

| Tender has | Editable |
|---|---|
| no offers | every field |
| one or more offers | `deliveryDate`, `bidDeadline` |

- `deliveryDate` stays editable because each offer states its own delivery
  date; the detail page's "nach Wunschtermin" hint is recalculated against the
  new value.
- `bidDeadline` stays editable so bidding can be extended. Moving a passed
  deadline to today or later makes the tender accept offers again; moving it
  earlier than today is rejected by the "today or later" rule above.
- `pickupDate` is locked, so the rule that an offer's `deliveryDate` is not
  before the tender's `pickupDate` cannot be broken by an edit.

### Frontend: edit action on the detail page

- A "Bearbeiten" link in the header row's action group, directly to the left
  of "Ausschreibung schließen": a real `<a>` to `/tenders/:id/edit`, styled as
  `btn-secondary`, `data-testid="edit-tender"`.
- Shown only while the tender is open, like the close button. It stacks below
  the title together with the close button at 600px and narrower.

### Frontend: edit page

A new route, `/tenders/:id/edit`, using the create form -- same five field
groups, same fields, same order, same validation messages.

```
← Zurück zur Ausschreibung

Ausschreibung bearbeiten

┌──────────────────────────────────────────────────────────────────────────┐
│ Zu dieser Ausschreibung liegen bereits Angebote vor. Es können nur noch  │
│ Zustelltermin und Angebotsfrist geändert werden.                         │
└──────────────────────────────────────────────────────────────────────────┘

Strecke
  ...
[ Speichern ]  [ Abbrechen ]
```

- Heading "Ausschreibung bearbeiten", submit button "Speichern". The form is
  prefilled with the tender's stored values, including the conditional fields
  ("ADR-Klasse", temperature range) when they apply.
- A back link "Zurück zur Ausschreibung" in the shared back-link style leads
  to `/tenders/:id`; "Abbrechen" does the same. Neither asks for confirmation.
- "Speichern" is disabled while the form is invalid, while it is unchanged
  from the loaded values, and while the request is in flight.
- On success the page navigates to `/tenders/:id`, which shows the new data.
- When the tender has offers, the notice above is shown
  (`data-testid="locked-fields-notice"`) and every field except "Zustellung
  bis" and "Angebotsfrist" is disabled. The request still carries the complete
  data, with the locked fields at their stored values.
- The form applies the same date rule as the backend: "today or later" is
  only checked for a date the user has changed.
- Failures show a German message with `role="alert"` above the buttons and
  keep every entered value:
  - `409`: "Die Ausschreibung kann nicht mehr in dieser Form geändert werden.
    Bitte laden Sie die Seite neu."
  - anything else: "Die Ausschreibung konnte nicht gespeichert werden. Bitte
    versuchen Sie es später erneut."
- States before the form is shown:
  - Loading: "Ausschreibung wird geladen…".
  - Load error or a non-numeric id: the detail page's existing load-error
    message.
  - The tender is not open: "Diese Ausschreibung ist vergeben oder
    geschlossen und kann nicht mehr bearbeitet werden."
    (`data-testid="not-editable"`), no form.
  - The back link is rendered in all of these states.
- `TenderApiService` gains an `update(id, data)` method taking the same typed
  object as `create`.
- The create page (`/tenders/new`) looks and behaves as before.

### Documentation

- `freight-tenders/README.md`: the tender description, a `PUT /api/tenders/{id}`
  row in the endpoint table, the error paragraph (the new `409` cases), the
  `/tenders/:id` row and a new `/tenders/:id/edit` row.
- `EXPERIENCE.md`: an Information Architecture row for the edit page, the
  Component Patterns row for the form (create and edit mode, locked fields),
  a State Patterns row "Tender with offers: locked fields", and a flow for
  correcting a tender.

### Clarifications

- Order of checks for `PUT`: tender exists (`404`), body is valid (`400`),
  tender is `OPEN` (`409`), locked fields are unchanged (`409`). This keeps
  the existing convention that validation runs before state checks.
- "Has offers" counts every offer of the tender, expired or not.
- Locked fields are compared by value: `loadingMeters` `13.6` equals `13.60`,
  an absent `palletCount`, `adrClass` or temperature value equals a stored
  `null`, and addresses are compared field by field. Text is compared exactly,
  without trimming or case folding.
- Saving a request that changes nothing is valid and returns `200`.
- There is no change history and no "last edited" marker; an edit simply
  replaces the stored values.
- Concurrent edits are not detected: the last successful `PUT` wins. An offer
  that arrives between loading the edit page and saving is covered by the
  backend's locked-field `409`.
- Whether the tender has offers is decided on the edit page from the loaded
  tender; the backend's `409` stays authoritative.
- The currency is locked together with the other fields once offers exist;
  with no offers it can be changed freely.
- Editing does not touch remarks. They stay attached to the tender.
- "Today" is the backend's `Clock` (`Europe/Berlin`) on the server and the
  browser's local date in the form, as for the existing date rules.
- Whether create and edit share one component with two modes or a shared form
  component used by two pages is the implementer's choice, as long as the
  fields, groups and messages are defined once.

### Implementation choices

Anything this story does not specify -- class and method names, how a rule or
query is implemented, how components and styles are split, test structure --
is the implementer's choice. Follow the conventions in
`freight-tenders/backend/AGENTS.md` and `freight-tenders/frontend/AGENTS.md`
and prefer the simplest option; none of it needs a decision from the story
author.

## Why

Shipment details change between publishing a tender and awarding it, and a
tool that answers every change with "create it again" trains its users to keep
the truth somewhere else. Locking the priced data once offers exist keeps the
one promise a tender makes to carriers -- that the job they quoted is the job
that gets awarded -- while still allowing the two changes that happen most
often late in a tender: more time to bid and a moved delivery date.

## Acceptance

- `PUT /api/tenders/{id}` with valid data on an open tender without offers
  returns `200`; `GET /api/tenders/{id}` and `GET /api/tenders` return the new
  values, and the tender's id, status and remarks are unchanged.
- Each create rule has a rejecting case on `PUT`: `400` with a `violations`
  entry naming the field, tender unchanged.
- A tender whose stored `bidDeadline` is in the past can be edited when the
  request repeats that date; changing it to another past date returns `400`
  with a violation on `bidDeadline`. The same holds for `pickupDate`.
- `PUT` on an awarded or closed tender returns `409`; on an unknown id `404`.
- On a tender with an offer, changing `deliveryDate` or `bidDeadline` returns
  `200`; changing any other field returns `409` and leaves the tender
  unchanged. A request that only repeats the stored values with
  `loadingMeters` written as `13.60` is not treated as a change.
- Extending a passed `bidDeadline` to today or later makes
  `POST /api/tenders/{id}/offers` succeed again.
- An invalid request to a closed tender returns `400`, not `409`.
- The detail page shows "Bearbeiten" for an open tender and not for an awarded
  or closed one; it links to `/tenders/:id/edit`.
- The edit page shows the form prefilled with the tender's data, including
  the conditional fields; "Speichern" is disabled until something has changed
  and the form is valid.
- Saving sends the complete data with `PUT`, then shows the detail page with
  the new values; "Abbrechen" and the back link return to the detail page
  without a request.
- For a tender with offers the edit page shows the notice and only
  "Zustellung bis" and "Angebotsfrist" are enabled.
- A `409` and any other failed save each show their German message with
  `role="alert"` and keep the entered values.
- Opening `/tenders/:id/edit` for an awarded or closed tender shows the
  not-editable message and no form; an unknown id shows the load error.
- The create page's behavior and its existing `data-testid` values are
  unchanged.
- All new UI text is German; assertions go through `data-testid`.
- `EXPERIENCE.md` and `freight-tenders/README.md` are updated as described.
- Existing tests keep passing or are updated; the new behavior has test
  coverage; `mvn -B verify`, `mvn spotless:check`, `mvn spotbugs:check`,
  `npm run lint`, `npm run build` and `npm test -- --watch=false` pass.

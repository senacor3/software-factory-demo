# Record offer terms and enforce the bid deadline

Depends on `stories/freight-tenders/tender-shipment-data-and-create-form.md`;
run after `stories/freight-tenders/tender-detail-grouped-shipment-data.md`,
which touches the same page.

## Problem

An offer is a supplier name and an amount. Two offers with the same price are
not equal if one delivers two days late or is only valid until tomorrow, and
the app cannot tell them apart. A tender also has a bid deadline that nothing
enforces: offers can be added to an open tender forever.

## What to build

### Offer data

| Field | Type | Rule |
|---|---|---|
| `supplierName` | text | required, at most 100 characters |
| `amount` | decimal | required, at least `0.01`; quoted in the tender's currency |
| `deliveryDate` | date | required, not before the tender's `pickupDate` -- the date the carrier commits to deliver |
| `validUntil` | date | required, today or later -- how long the quoted price holds |
| `note` | text | optional, at most 500 characters -- conditions or deviations, for example "kein Palettentausch" |

### Backend

- `POST /api/tenders/{id}/offers` takes these fields and `OfferResponse`
  returns them.
- The rules are enforced with Bean Validation and rejected with `400` in the
  existing error shape. `deliveryDate` before the tender's `pickupDate` cannot
  be checked on the request alone; it is also rejected with `400` and a
  `violations` entry for `deliveryDate`.
- `supplierName` and `amount` are validated here even if
  `stories/freight-tenders/validate-remark-and-offer-input.md` has not been
  implemented yet; if it has, keep its behavior.
- An offer for a tender whose `bidDeadline` is before today is rejected with
  `409 Conflict` through a new domain exception, mapped in
  `TenderExceptionHandler` like `TenderClosedException`. An offer on the
  deadline day itself is accepted. The closed check comes first: a closed
  tender still answers with the existing closed error.
- Remarks are not affected by the deadline.
- "Today" comes from the injectable `java.time.Clock`.

### Frontend

The offers table on the detail page gets five columns:

```
Anbieter            Betrag         Zustellung           Gültig bis      Hinweis
-------------------------------------------------------------------------------------
Spedition Nord      1.450,00 €     22.10.2026           18.10.2026      kein Palettentausch
Trans Benelux       1.390,00 €     23.10.2026           15.10.2026
                                   nach Wunschtermin    abgelaufen
```

- "Zustellung" shows "nach Wunschtermin" on a second line when the offered
  delivery date is after the tender's delivery date. "Gültig bis" shows
  "abgelaufen" on a second line when the date has passed. Both are plain
  `{typography.caption}` text without a color of their own.
- Sortable: Anbieter, Betrag, Zustellung, Gültig bis. "Hinweis" is not.
- The add-offer form gains "Zustellung am", "Gültig bis" and "Hinweis
  (optional)", with the same rules as the backend and a German message under
  each invalid touched field.
- When an open tender's bid deadline has passed, the offer form is disabled
  (fields and button) and a notice above it reads "Die Angebotsfrist ist am
  16.10.2026 abgelaufen, daher können keine weiteren Angebote hinzugefügt
  werden." The remark form stays enabled. A closed tender keeps its existing
  single explanation and does not show this notice as well.
- A `409` from the backend shows the existing offer error message and keeps the
  entered values.

### Documentation

- `freight-tenders/README.md`: the offers endpoint row and the error paragraph.
- `EXPERIENCE.md`: the add-offer form row in Component Patterns, a State
  Patterns row "Bid deadline passed", and Flow 1.

## Why

Comparing offers is the point of a tender, and price is only one of the three
things a dispatcher compares: price, delivery date and how long the price
holds. The bid deadline is the rule that makes a tender a tender rather than an
open-ended list of quotes.

## Acceptance

- A valid offer returns `201` with all five fields and appears in the tender's
  detail response.
- A missing or past `validUntil`, a missing `deliveryDate`, a `deliveryDate`
  before the tender's pickup date, or a `note` over 500 characters returns
  `400` with a `violations` entry for that field, and no offer is stored.
- An offer on the bid deadline day is accepted; an offer the day after returns
  `409` and is not stored; a remark the day after is still accepted.
- An offer on a closed tender returns the existing closed `409`, whether or not
  the deadline has passed.
- The offers table shows the five columns, marks a late delivery with "nach
  Wunschtermin" and an expired offer with "abgelaufen", and sorts by the four
  sortable columns in both directions.
- Adding an offer through the form sends all fields and adds the row without a
  reload.
- On an open tender past its deadline the offer form is disabled with the
  notice above it and the remark form is enabled.
- All new UI text is German; assertions go through `data-testid`.
- Existing tests keep passing or are updated to the new offer shape; the new
  behavior has test coverage; the backend and frontend check commands pass.

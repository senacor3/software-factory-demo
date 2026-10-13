# Show the shipment's key facts in the tender overview

Depends on `stories/freight-tenders/tender-shipment-data-and-create-form.md`.

## Problem

The overview lists each tender as origin city, destination city and a status
pill. A dispatcher scanning the list cannot tell which tender is urgent, what
kind of load it is, or whether any carrier has answered yet without opening
every row. The status column adds nothing: each table already contains only
one status and says so in its heading.

## What to build

Redesign both overview tables around the questions a dispatcher asks of a list:
where, when, what, how urgent, and how far along.

### Columns

Both tables ("Offene Ausschreibungen", "Geschlossene Ausschreibungen") get the
same seven columns. The "Status" column is removed.

```
Von          Nach         Abholung     Ladung               Fahrzeug          Angebotsfrist   Angebote
----------------------------------------------------------------------------------------------------
Hamburg      Rotterdam    20.10.2026   18.500 kg · 13,6 ldm Planenauflieger   16.10.2026            3
DE 20457     NL 3011 AA                ADR 3                                  heute           ab 1.450,00 €
```

| Column | First line | Second line (`{typography.caption}`, `{colors.on-surface-variant}`) |
|---|---|---|
| Von | origin city (the row link) | country code and postal code |
| Nach | destination city | country code and postal code |
| Abholung | pickup date | -- |
| Ladung | weight and loading meters | "ADR" plus the class for dangerous goods, and the temperature range ("2 bis 8 °C") for temperature-controlled loads, joined by " · "; empty when neither applies |
| Fahrzeug | German vehicle type label | -- |
| Angebotsfrist | bid deadline | open tenders only: "heute" when the deadline is today, "abgelaufen" when it has passed |
| Angebote | number of offers, right-aligned | "ab" plus the lowest offer amount in the tender's currency; empty when there are no offers |

- Dates are formatted `dd.MM.yyyy`, numbers and amounts in German notation
  (`18.500 kg`, `13,6 ldm`, `1.450,00 €`).
- The deadline hints and the cargo hints are plain text. They carry no color of
  their own: green and grey stay reserved for tender status and red for errors
  (`DESIGN.md`, Colors).
- Sortable: Von, Nach, Abholung, Ladung (by weight), Angebotsfrist, Angebote
  (by count). Fahrzeug is not sortable. The default order stays newest first,
  and sort behavior and `aria-sort` stay as they are today.
- The whole row still opens the tender, and the row link stays in the first
  column.

### Layout

- Seven columns do not fit the current 960px content width with 24px cell
  padding. The overview page widens its content area to 1200px; the other two
  pages keep 960px.
- Below that width the table scrolls horizontally inside its own container.
  The page itself never scrolls sideways, and the table header stays aligned
  with its columns while scrolling.
- Cell contents do not wrap except between the first and second line.

### Backend

`TenderResponse` gains two fields so the overview does not have to load every
tender's detail:

- `offerCount` -- number of offers on the tender.
- `lowestOfferAmount` -- the smallest offer amount, `null` without offers.

Listing tenders must not run one extra query per tender to compute them.

### Documentation

- `freight-tenders/README.md`: the `GET /api/tenders` row and the `/` row.
- `EXPERIENCE.md`: the overview's Information Architecture row, the "Status
  pill" row of Component Patterns (the pill is no longer used on the overview),
  and Flow 1 steps 1-3.
- `DESIGN.md`: Components -> Tables gains the two-line cell and the scrolling
  container; Layout & Spacing notes the overview's wider content area.
- `mockups/tender-overview.html` is updated to the new columns.

### Clarifications

- "Today" for the "heute"/"abgelaufen" hints is the browser's local date. The
  hints are computed in the frontend; the backend returns no such flag.
- `lowestOfferAmount` and the "ab" amount are in the tender's `currency`.
- Sorting uses the first line's underlying value only: city name, date, weight
  in kg, offer count. Second-line content never affects the order.
- The overview keeps loading all tenders with one `GET /api/tenders` call and
  splitting them into the two tables in the frontend, as today.
- The first two columns keep their existing sort keys' behavior; existing
  `data-testid` values are kept where the element still exists, and tests for
  the removed status column are removed.

### Implementation choices

Anything this story does not specify -- class and method names, how a rule or
query is implemented, how components and styles are split, test structure --
is the implementer's choice. Follow the conventions in
`freight-tenders/backend/AGENTS.md` and `freight-tenders/frontend/AGENTS.md`
and prefer the simplest option; none of it needs a decision from the story
author.

## Why

The overview is the dispatcher's work queue. With pickup date, load, vehicle,
bid deadline and offer count in the row, they can pick the next tender to act
on from the list itself, which is the reason the list exists.

## Acceptance

- Both tables show the seven columns in the order above and no status column.
- A row shows city plus country code and postal code for both ends, the pickup
  date, weight and loading meters, the German vehicle type label, the bid
  deadline and the offer count.
- A dangerous-goods tender shows "ADR" and its class in the Ladung cell; a
  temperature-controlled tender shows its range; a tender with neither shows no
  second line there.
- An open tender whose bid deadline is today shows "heute", one whose deadline
  has passed shows "abgelaufen"; closed tenders show neither.
- A tender with offers shows the count and "ab" plus the lowest amount in the
  tender's currency; a tender without offers shows `0` and no amount.
- Sorting by each of the six sortable columns works in both directions and
  independently per table; sorting by Ladung orders by weight and sorting by
  Angebote by count.
- `GET /api/tenders` returns `offerCount` and `lowestOfferAmount` for every
  tender.
- At a viewport narrower than the table, the table scrolls horizontally and the
  page does not.
- All new UI text is German; assertions go through `data-testid`.
- Existing tests keep passing or are updated to the new columns; the new
  behavior has test coverage; the backend and frontend check commands pass.

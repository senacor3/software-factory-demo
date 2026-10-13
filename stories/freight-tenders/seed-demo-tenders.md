# Seed example tenders for demos

Depends on all five shipment-data stories; run it last:
`tender-shipment-data-and-create-form.md`, `tender-overview-shipment-columns.md`,
`tender-detail-grouped-shipment-data.md`, `offer-terms-and-bid-deadline.md` and
`award-tender-to-offer.md` (all under `stories/freight-tenders/`).

## Problem

The backend runs on an in-memory H2 database, so every start shows two empty
tables. Since a tender now has sixteen fields and an offer five, getting the
app into a state worth showing means filling in the create form several times
and adding offers by hand -- before every demo. Some states cannot be produced
through the UI at all on the same day: a tender whose bid deadline has passed,
or an offer that has expired.

## What to build

A backend-only seeder that fills the database with a fixed set of example
tenders when the application starts with the Spring profile `demo`.

### Activation

- The seeder is a component in the `tender` package that is only active under
  the `demo` profile. Without the profile the application starts empty,
  exactly as today, so tests and CI are unaffected.
- It runs once at startup and only when there are no tenders yet.
- `freight-tenders/README.md` documents the command,
  `mvn spring-boot:run -Dspring-boot.run.profiles=demo`, in the backend section
  and uses it in "Running both together".

### Data

All dates are computed relative to today, taken from the injectable
`java.time.Clock`, so the set shows the same states on whatever day it is
started. The set covers every state the UI distinguishes:

| # | Route | Load | State |
|---|---|---|---|
| 1 | Hamburg (DE) → Rotterdam (NL) | general cargo, curtain-sider, 33 pallets | open, deadline in 3 days, three offers; one delivers after the requested date |
| 2 | München (DE) → Milano (IT) | temperature-controlled 2 to 8 °C, reefer | open, deadline in 5 days, two offers |
| 3 | Ludwigshafen (DE) → Antwerpen (BE) | dangerous goods, ADR class 3, box trailer | open, deadline today, one offer |
| 4 | Bremen (DE) → Wien (AT) | steel coils, flatbed, no pallet count | open, deadline in 7 days, no offers |
| 5 | Stuttgart (DE) → Lyon (FR) | automotive parts, mega trailer | open, deadline passed yesterday, two offers; one has expired |
| 6 | Zürich (CH) → Hamburg (DE) | general cargo, currency `CHF` | open, deadline in 4 days, one offer |
| 7 | Berlin (DE) → Warszawa (PL) | general cargo, curtain-sider | awarded to the cheaper of two offers |
| 8 | Köln (DE) → København (DK) | general cargo, box trailer | closed without award, one offer and one remark |

- Postal codes, weights, loading meters, supplier names and amounts are
  plausible, fixed values chosen by the implementer; commodity texts, remarks
  and offer notes are German, like data a dispatcher would have typed.
- At least three tenders carry a remark, and at least two offers carry a note.
- Every seeded tender and offer satisfies the rules the API enforces, with two
  deliberate exceptions that the API would refuse on the day of creation:
  tender 5's bid deadline and its expired offer lie in the past. The seeder
  therefore creates its data through the domain model and repository, not by
  calling the controller.
- Tender 7 is awarded and tender 8 closed through the same service methods the
  API uses, so their state is consistent with what the application itself
  would produce.

### Clarifications

- "Today" is the date of the application's `Clock` bean (`Europe/Berlin`).
- How the two deliberately past-dated values get stored is the implementer's
  choice, but the validation rules of the API must not be weakened or made
  conditional on the profile to allow it.
- Tender 7 is awarded and tender 8 closed after their offers and remarks have
  been added.
- The seeder is not exposed through any endpoint and adds no configuration
  property beyond the profile.
- No frontend change.

### Implementation choices

Anything this story does not specify -- class and method names, how a rule or
query is implemented, how components and styles are split, test structure --
is the implementer's choice. Follow the conventions in
`freight-tenders/backend/AGENTS.md` and `freight-tenders/frontend/AGENTS.md`
and prefer the simplest option; none of it needs a decision from the story
author.

## Why

A demo should start with the overview already telling a story: urgent and
relaxed deadlines, special cargo, offers to compare, one finished tender with a
winner. Seeding it makes the app presentable in one command and makes the
time-dependent states visible without waiting for a day to pass.

## Acceptance

- Started with the `demo` profile, `GET /api/tenders` returns the eight
  tenders: six open, one awarded, one closed.
- Started without the profile, `GET /api/tenders` returns an empty list.
- The seeder does nothing when tenders already exist.
- With a fixed clock, the seeded bid deadlines are today + 3, + 5, today,
  + 7, yesterday and + 4 for tenders 1 to 6, and tender 5 has one offer whose
  `validUntil` is before today.
- Tender 2 is temperature-controlled with a reefer, tender 3 is dangerous
  goods with ADR class 3, tender 4 has no pallet count, tender 6 is in `CHF`.
- Tender 7 is `AWARDED` with the lower of its two offers as the awarded offer;
  tender 8 is `CLOSED` with no awarded offer.
- Adding an offer to seeded tender 5 through the API returns `409`.
- `freight-tenders/README.md` documents the `demo` profile.
- Existing tests keep passing; the seeder has test coverage; `mvn -B verify`,
  `mvn spotless:check` and `mvn spotbugs:check` pass.

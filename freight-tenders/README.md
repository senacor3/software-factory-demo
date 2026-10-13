# freight-tenders

The freight tender demo app: a Spring Boot backend and an Angular frontend,
each independently buildable/testable/lintable. A tender is a spot tender for
one European road shipment -- origin and destination address, pickup, delivery
and bid-deadline dates, the cargo (commodity, weight, loading meters, optional
pallet count, dangerous goods, temperature range), the vehicle type and the
currency offers are quoted in -- that is open, awarded or closed; while it is open, remarks and
offers can be recorded against it, and one offer can be awarded the contract. The frontend lists the tenders, creates new
ones, and shows one tender with its remarks and offers.

This directory is independent of software-factory's own Python tooling: nothing
here is built, tested, or linted with `uv`/pytest/ruff. It has its own CI
workflow, `.github/workflows/freight-tenders.yml`, running on every push/PR
touching `freight-tenders/**`. software-factory's own pipeline
(`.github/workflows/software-factory.yml`) also builds/tests/lints this app as
part of its `checks` job, via commands named in
`.github/post-implementation-checks.yml` — so a dispatched story touching
`freight-tenders/` is checked by both.

## Backend (`backend/`)

Spring Boot (Java 25) REST API over an in-memory H2 database, so all data is
gone on restart.

| Endpoint | Does | Success |
|---|---|---|
| `POST /api/tenders` | Creates an open tender from the shipment data (`origin`/`destination` as `{country, postalCode, city}`, `pickupDate`, `deliveryDate`, `bidDeadline`, `commodity`, `weightKg`, `loadingMeters`, optional `palletCount`, `equipmentType`, `dangerousGoods` with `adrClass`, `temperatureControlled` with `temperatureMinC`/`temperatureMaxC`, `currency`); invalid data returns `400` with `violations` | `201` |
| `GET /api/tenders` | Lists tenders, each with `offerCount` and `lowestOfferAmount` (`null` without offers); optional `?status=OPEN`, `?status=AWARDED` or `?status=CLOSED`; awarded tenders also carry `awardedSupplierName` and `awardedAmount` (`null` otherwise) | `200` |
| `GET /api/tenders/{id}` | Returns one tender with its remarks and offers | `200` |
| `POST /api/tenders/{id}/close` | Closes the tender (`409` for an awarded tender) | `200` |
| `POST /api/tenders/{id}/offers/{offerId}/award` | Awards the tender to one of its offers; returns the tender detail with `status` `AWARDED` and `awardedOfferId` | `200` |
| `POST /api/tenders/{id}/remarks` | Adds a remark (`text`) | `201` |
| `POST /api/tenders/{id}/offers` | Adds an offer (`supplierName` up to 100 characters, `amount`, `deliveryDate`, `validUntil` today or later, optional `note` up to 500 characters; a blank `note` is stored as `null`); rejected with `409` after the tender's `bidDeadline` has passed and with `400` if `deliveryDate` is before the tender's `pickupDate` | `201` |
| `GET /api/health` | Liveness check, `{"status":"UP"}` | `200` |

The three `POST` endpoints that take a body (create tender, add remark, add offer) return `400` with `{error, message, path, timestamp, violations}` on invalid input (blank `origin`/`destination`/`text`/`supplierName`, a missing or non-positive `amount` below `0.01`, a missing `deliveryDate` or `validUntil`, a `validUntil` in the past, or a `note` over 500 characters; an offer whose `deliveryDate` is before the tender's `pickupDate` is also a `400`, with a `violations` entry for `deliveryDate`); `violations` lists each offending `field` with a `message`. Other errors use the same shape without `violations`: `404` for an unknown tender (or, when awarding, an offer that is not part of the tender) and `409` for a closed or awarded tender, and for awarding an offer whose `validUntil` has passed (checked in the order tender, offer, tender open, offer not expired; awarding is still allowed after the bid deadline). A `409` also applies to a closed tender and `409` for an offer added after the tender's bid deadline (remarks stay allowed; a closed tender reports the closed error first). Validation runs first, so an invalid request to a closed tender returns `400`, not `409`.

```bash
cd backend
mvn -B verify        # build + test
mvn spotless:check   # lint (formatting)
mvn spotbugs:check   # static analysis (bug patterns)
mvn spring-boot:run  # run locally on :8080
mvn spring-boot:run -Dspring-boot.run.profiles=demo  # same, seeded with eight demo tenders
```

With the `demo` profile, `DemoDataSeeder` fills an empty database at startup with eight
tenders (six open, one awarded, one closed) whose dates are relative to today. Without
the profile, nothing is seeded.

## Frontend (`frontend/`)

Angular (standalone components, SCSS, Vitest for unit tests).

| Route | Page | Shows |
|---|---|---|
| `/` | `TenderOverview` | Two tables, "Offene Ausschreibungen" (open) and "Abgeschlossene Ausschreibungen" (awarded and closed, with a sortable "Status" column); each row shows the route, pickup date, load, vehicle, bid deadline and offer count with the lowest offer (or "Zuschlag: supplier amount" for an awarded tender); the tables scroll horizontally on narrow screens; a row opens that tender |
| `/tenders/new` | `TenderCreate` | A form with five field groups (route "Strecke", dates "Termine", cargo "Ladung", vehicle "Fahrzeug", tender "Ausschreibung") for the full shipment data, validated with the backend's rules; on success it returns to the overview |
| `/tenders/:id` | `TenderDetail` | A "Zurück zur Übersicht" back link, the tender's status, a one-line summary, the shipment data as four cards (Strecke, Termine, Ladung, Fahrzeug und Konditionen), its offers and remarks as two tables, a form to add each, a "Vergeben" button per non-expired offer with an in-place confirmation while the tender is open, and an "Ausschreibung schließen" button while the tender is open |

```bash
cd frontend
npm ci
npm run build          # production build
npm test -- --watch=false   # unit tests
npm run lint            # lint
npm run static-analysis # static analysis (bug patterns)
npm start                # run locally on :4200, proxying /api to localhost:8080
```

## Running both together

```bash
# terminal 1 (the demo profile seeds sample tenders)
cd backend && mvn spring-boot:run -Dspring-boot.run.profiles=demo

# terminal 2
cd frontend && npm start
```

Then open `http://localhost:4200`.

# Capture real shipment data when creating a tender

## Problem

A tender is two free-text strings, `origin` and `destination`. No carrier could
price that: an offer depends on what is moving, how much of it, when, in which
vehicle, and until when bids are accepted. The demo app therefore does not look
like a freight tender tool, and it has almost no business rules for the
pipeline to be proven against beyond "open or closed".

## What to build

Model a tender as a **spot tender for one European road shipment** and collect
that data in the create form. Backend and frontend change together, so the app
keeps working end to end after this story.

Out of scope here, each covered by its own follow-up story: the overview's new
columns, the detail page's grouped presentation, offer data, and awarding.

### Tender data

| Field | Type | Rule |
|---|---|---|
| `origin`, `destination` | object `{country, postalCode, city}` | all three required; `country` is two uppercase letters (ISO 3166-1 alpha-2); `postalCode` at most 10 characters; `city` at most 100 |
| `pickupDate` | date | required, today or later |
| `deliveryDate` | date | required, not before `pickupDate` |
| `bidDeadline` | date | required, today or later, not after `pickupDate` |
| `commodity` | text | required, at most 200 characters |
| `weightKg` | integer | required, 1 to 40000 |
| `loadingMeters` | decimal, one fraction digit | required, 0.1 to 13.6 |
| `palletCount` | integer | optional, 1 to 66 |
| `equipmentType` | enum | required: `CURTAIN_SIDER`, `BOX`, `REEFER`, `FLATBED`, `MEGA_TRAILER` |
| `dangerousGoods` | boolean | required |
| `adrClass` | text | required when `dangerousGoods` is true, otherwise must be absent; one of `1`, `2`, `3`, `4.1`, `4.2`, `4.3`, `5.1`, `5.2`, `6.1`, `6.2`, `7`, `8`, `9` |
| `temperatureControlled` | boolean | required; when true, `equipmentType` must be `REEFER` |
| `temperatureMinC`, `temperatureMaxC` | integer | both required when `temperatureControlled` is true, otherwise both absent; -30 to 30; min not above max |
| `currency` | enum | required: `EUR`, `CHF`, `GBP`, `PLN`, `CZK`, `DKK`, `SEK` -- the currency all offers on this tender are quoted in |

The old flat `origin`/`destination` strings are replaced, not kept alongside.
The database is in-memory H2 with `ddl-auto: update`, so there is no migration.

### Backend

- `POST /api/tenders` takes the fields above, for example:

  ```json
  {
    "origin": { "country": "DE", "postalCode": "20457", "city": "Hamburg" },
    "destination": { "country": "NL", "postalCode": "3011 AA", "city": "Rotterdam" },
    "pickupDate": "2026-10-20",
    "deliveryDate": "2026-10-22",
    "bidDeadline": "2026-10-16",
    "commodity": "Maschinenteile auf Europaletten",
    "weightKg": 18500,
    "loadingMeters": 13.6,
    "palletCount": 33,
    "equipmentType": "CURTAIN_SIDER",
    "dangerousGoods": false,
    "temperatureControlled": false,
    "currency": "EUR"
  }
  ```

- `TenderResponse` (create, list, close) and `TenderDetailResponse` return all
  of these fields in the same shape, next to `id` and `status`.
- Every rule in the table is enforced with Bean Validation at the API boundary
  (`freight-tenders/backend/AGENTS.md`, Policy). A violation returns `400` in
  the existing `{error, message, path, timestamp, violations}` shape.
- Cross-field rules must show up in `violations` under the name of the field
  the user has to fix (`deliveryDate`, `bidDeadline`, `adrClass`,
  `equipmentType`, `temperatureMinC`, `temperatureMaxC`). Note that
  `TenderExceptionHandler` currently reports field errors only, so a class-level
  constraint without a field name would be silently dropped.
- Nested address violations are named by path, for example `origin.postalCode`.
- An unknown enum value or a malformed date also returns `400` in the same
  error shape (`violations` may be empty), not Spring's default error body.
- "Today" comes from an injectable `java.time.Clock`, so date rules are testable
  without depending on the day the tests run. The production `Clock` bean is
  fixed to the zone `Europe/Berlin`, not the system default, so "today" does
  not depend on where the server runs.
- Postal codes are checked for presence and length only. There is no
  country-specific format check; spaces and letters are allowed ("3011 AA").
- The backend accepts any two uppercase letters as `country` and does not
  restrict it to a list. The 13 countries are only the choices the create form
  offers.
- `adrClass` is a string in the API and the database, not a Java enum, and is
  validated against the 13 listed values. Any other value is an ordinary
  validation failure: `400` with a `violations` entry for `adrClass`.
- All date comparisons are inclusive at the boundary: `pickupDate` and
  `bidDeadline` may be today, `deliveryDate` may equal `pickupDate`, and
  `bidDeadline` may equal `pickupDate`.

### Implementation choices

Anything this story does not specify -- class and method names, how a
constraint is implemented, how the form is split into components, test
structure -- is the implementer's choice. Follow the conventions in
`freight-tenders/backend/AGENTS.md` and `freight-tenders/frontend/AGENTS.md`
and prefer the simplest option; none of it needs a decision from the story
author.

### Frontend: create form

`/tenders/new` collects all fields, grouped into five labelled field groups
(`<fieldset>` with a `<legend>` in `{typography.title}`), in this order:

```
Neue Ausschreibung erstellen

Strecke
  Von    [Land v] [PLZ    ] [Ort            ]
  Nach   [Land v] [PLZ    ] [Ort            ]

Termine
  [Abholung am    ] [Zustellung bis    ]

Ladung
  [Warenbeschreibung                        ]
  [Gewicht (kg)   ] [Lademeter ] [Anzahl Paletten (optional)]
  [ ] Gefahrgut (ADR)         -> [ADR-Klasse v]
  [ ] Temperaturgeführt       -> [Temperatur von (°C)] [Temperatur bis (°C)]

Fahrzeug
  [Fahrzeugtyp v]

Ausschreibung
  [Angebotsfrist  ] [Währung v]

[ Erstellen ]  [ Abbrechen ]
```

- Country is a select with German names for `DE`, `AT`, `CH`, `NL`, `BE`, `LU`,
  `FR`, `IT`, `ES`, `PL`, `CZ`, `DK`, `SE`; default `DE`. Currency defaults to
  `EUR`. Dates use `<input type="date">`.
- Vehicle type labels: "Planenauflieger" (`CURTAIN_SIDER`), "Kofferauflieger"
  (`BOX`), "Kühlauflieger" (`REEFER`), "Plateauauflieger" (`FLATBED`),
  "Megatrailer" (`MEGA_TRAILER`). These label maps live next to
  `STATUS_LABELS` in `tender-api.ts` so the other pages can reuse them.
- "ADR-Klasse" is only rendered while "Gefahrgut (ADR)" is checked, and the two
  temperature fields only while "Temperaturgeführt" is checked. Unchecking
  removes the values from the request.
- The form applies the same rules as the backend. A field that has been touched
  and is invalid shows a German message directly below it in `{colors.error}`
  (`DESIGN.md`, Components -> Forms). Cross-field messages appear under the
  field named in the backend rule, for example "Die Zustellung darf nicht vor
  der Abholung liegen." under "Zustellung bis" and "Temperaturgeführte Ladung
  erfordert einen Kühlauflieger." under "Fahrzeugtyp".
- "Erstellen" stays disabled until the form is valid and while a request is in
  flight; success still navigates to `/`; a failed request shows the existing
  submit error and keeps every entered value.
- Fields within a group sit side by side on desktop and stack at 600px and
  narrower. The form card may grow beyond its current 560px to fit three
  fields in a row.
- `TenderApiService.create` takes one typed object instead of two strings.

### Frontend: overview and detail

Only what is needed to keep them working: the overview's "Von"/"Nach" columns
and the detail page title show `origin.city` and `destination.city`. Sorting by
those two columns keeps working. Nothing else changes on these pages.

### Documentation

- `freight-tenders/README.md`: the tender description, the `POST /api/tenders`
  row and the `/tenders/new` row.
- `EXPERIENCE.md`: the Information Architecture row and the Component Patterns
  row for the create form, and Flow 2.

## Why

Every later improvement -- an overview a dispatcher can scan, a detail page
that reads like a real tender, comparable offers -- needs this data to exist
first. It also gives the app real validation rules across fields, which is
what the pipeline's review and test stages are meant to be exercised on.

## Acceptance

- A valid request creates an open tender and returns `201` with every field;
  `GET /api/tenders` and `GET /api/tenders/{id}` return the same data.
- Each rule in the table has a rejecting case: the request returns `400` with a
  `violations` entry naming the field, and no tender is stored.
- `adrClass` is rejected when `dangerousGoods` is false, and required when it
  is true; the same for the temperature range and `temperatureControlled`.
- A temperature-controlled tender with a vehicle type other than `REEFER` is
  rejected with a violation on `equipmentType`.
- An unknown `equipmentType` or `currency` returns `400` in the standard error
  shape.
- The create form shows the five groups in the order above, renders the
  conditional fields only when their checkbox is checked, and shows a German
  message under each invalid touched field.
- Creating a tender through the form sends the full request and returns to the
  overview, where the tender is listed with its origin and destination city.
- All new UI text is German; assertions go through `data-testid`.
- Existing tests are updated to the new model and pass; the new behavior has
  test coverage; `mvn -B verify`, `mvn spotless:check`, `mvn spotbugs:check`,
  `npm run lint`, `npm run build` and `npm test -- --watch=false` pass.

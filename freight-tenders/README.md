# freight-tenders

The freight tender demo app: a Spring Boot backend and an Angular frontend,
each independently buildable/testable/lintable. A tender is a freight route
(origin, destination) that is open or closed; while it is open, remarks and
offers can be recorded against it. The frontend lists the tenders, creates new
ones, and shows one tender with its remarks and offers.

This directory is independent of light-factory's own Python tooling: nothing
here is built, tested, or linted with `uv`/pytest/ruff. It has its own CI
workflow, `.github/workflows/freight-tenders.yml`, running on every push/PR
touching `freight-tenders/**`. light-factory's own pipeline
(`.github/workflows/light-factory.yml`) also builds/tests/lints this app as
part of its `checks` job, via commands named in
`.github/post-implementation-checks.yml` — so a dispatched story touching
`freight-tenders/` is checked by both.

Backend code, API, domain model, and docs stay English; all UI-facing
(Angular template) text is German.

## Backend (`backend/`)

Spring Boot (Java 25) REST API over an in-memory H2 database, so all data is
gone on restart.

| Endpoint | Does | Success |
|---|---|---|
| `POST /api/tenders` | Creates an open tender from `origin` and `destination` | `201` |
| `GET /api/tenders` | Lists tenders; optional `?status=OPEN` or `?status=CLOSED` | `200` |
| `GET /api/tenders/{id}` | Returns one tender with its remarks and offers | `200` |
| `POST /api/tenders/{id}/close` | Closes the tender | `200` |
| `POST /api/tenders/{id}/remarks` | Adds a remark (`text`) | `201` |
| `POST /api/tenders/{id}/offers` | Adds an offer (`supplierName`, `amount`) | `201` |
| `GET /api/health` | Liveness check, `{"status":"UP"}` | `200` |

Errors: `404` for an unknown tender id; `409` when adding a remark or an offer
to a closed tender; `400` with a `violations` array when a create request has
a blank `origin` or `destination`. In these three cases the error body is
`{error, message, path, timestamp}`.

```bash
cd backend
mvn -B verify        # build + test
mvn spotless:check   # lint (formatting)
mvn spring-boot:run  # run locally on :8080
```

## Frontend (`frontend/`)

Angular (standalone components, SCSS, Vitest for unit tests). Three pages,
all calling the backend through one shared `TenderApiService`:

| Route | Page | Shows |
|---|---|---|
| `/` | `TenderOverview` | Two tables, "Offene Ausschreibungen" (open) and "Geschlossene Ausschreibungen" (closed); a row opens that tender |
| `/tenders/new` | `TenderCreate` | A form for origin ("Von") and destination ("Nach"); on success it returns to the overview |
| `/tenders/:id` | `TenderDetail` | The tender's status, its remarks and offers as two tables, and a form to add each |

All four tables sort by a single column: selecting a column header sorts
ascending, selecting it again reverses. The default order is newest first, and
the sort resets on every visit. The overview and the detail page show a German
loading message while their request is in flight, a German empty-state row for
an empty table, and a German error message if the backend is unreachable; the
create form shows a German error below its fields if saving fails. On a closed
tender the detail page disables both forms and explains why. There is no UI
for closing a tender; that is done through the API only. Global styles (design
tokens and the shared table, form, and button styles) live in
`src/styles.scss`.

```bash
cd frontend
npm ci
npm run build          # production build
npm test -- --watch=false   # unit tests
npm run lint            # lint
npm start                # run locally on :4200, proxying /api to localhost:8080
```

## Running both together

```bash
# terminal 1
cd backend && mvn spring-boot:run

# terminal 2
cd frontend && npm start
```

Open `http://localhost:4200`: the page shows the tender overview, empty on a
fresh start. Closing a tender has no UI; call the API directly:

```bash
curl -X POST http://localhost:8080/api/tenders/1/close
```

If the backend isn't running, each page shows a German error message instead
of an unhandled failure.

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

The three `POST` endpoints that take a body (create tender, add remark, add offer) return `400` with `{error, message, path, timestamp, violations}` on invalid input (blank `origin`/`destination`/`text`/`supplierName`, or a missing or non-positive `amount` below `0.01`); `violations` lists each offending `field` with a `message`. Other errors use the same shape without `violations`: `404` for an unknown tender and `409` for a closed tender. Validation runs first, so an invalid request to a closed tender returns `400`, not `409`.

```bash
cd backend
mvn -B verify        # build + test
mvn spotless:check   # lint (formatting)
mvn spotbugs:check   # static analysis (bug patterns)
mvn spring-boot:run  # run locally on :8080
```

## Frontend (`frontend/`)

Angular (standalone components, SCSS, Vitest for unit tests).

| Route | Page | Shows |
|---|---|---|
| `/` | `TenderOverview` | Two tables, "Offene Ausschreibungen" (open) and "Geschlossene Ausschreibungen" (closed); a row opens that tender |
| `/tenders/new` | `TenderCreate` | A form for origin ("Von") and destination ("Nach"); on success it returns to the overview |
| `/tenders/:id` | `TenderDetail` | A "Zurück zur Übersicht" back link, the tender's status, its remarks and offers as two tables, a form to add each, and an "Ausschreibung schließen" button while the tender is open |

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
# terminal 1
cd backend && mvn spring-boot:run

# terminal 2
cd frontend && npm start
```

Then open `http://localhost:4200`.

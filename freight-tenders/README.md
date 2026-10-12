# freight-tenders

A minimal full-stack scaffold for the freight tender demo app: a Spring Boot
backend and an Angular frontend, each independently buildable/testable/lintable.
The frontend's home page is a tender overview that fetches the backend's
tender list endpoint and renders it under German headings.

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

Spring Boot (Java 25) exposing `GET /api/health` -> `{"status":"UP"}`.

```bash
cd backend
mvn -B verify        # build + test
mvn spotless:check   # lint (formatting)
mvn spring-boot:run  # run locally on :8080
```

## Frontend (`frontend/`)

Angular (standalone components, SCSS, Vitest for unit tests). The home page
(`TenderOverview`) fetches `GET /api/tenders` once and splits the results
into two sections, "Offene Ausschreibungen" (open) and "Geschlossene
Ausschreibungen" (closed). While the request is in flight it shows a German
loading message; an empty section shows a German empty-state message instead
of nothing; if the backend is unreachable, a German error message is shown
instead of the sections.

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

Open `http://localhost:4200`: the page shows the tender overview, grouping
any tenders created via the backend API under "Offene Ausschreibungen" or
"Geschlossene Ausschreibungen". If the backend isn't running, the page shows
a German error message instead of an unhandled failure.

# freight-tenders

A minimal full-stack scaffold for the freight tender demo app: a Spring Boot
backend and an Angular frontend, each independently buildable/testable/lintable,
connected by one trivial end-to-end path -- a backend health check rendered on
the frontend's home page under the German label "Systemstatus".

This directory is independent of light-factory's own Python tooling: nothing
here is built, tested, or linted with `uv`/pytest/ruff, and light-factory's CI
(`.github/workflows/light-factory.yml`) does not touch it. CI for this app
lives in its own workflow, `.github/workflows/freight-tenders.yml`.

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

Angular (standalone components, SCSS, Vitest for unit tests), calling the
backend's health endpoint and rendering it under the "Systemstatus" label,
with a "nicht verfügbar" fallback if the backend is unreachable.

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

Open `http://localhost:4200`: the page shows "Systemstatus" with the live
"UP" status proxied from the backend. If the backend isn't running, the page
shows "nicht verfügbar" instead of an unhandled error.

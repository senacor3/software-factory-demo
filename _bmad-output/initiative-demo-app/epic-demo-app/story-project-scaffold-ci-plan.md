---
title: 'Project scaffold & CI'
type: 'feature'
ticket: 1
created: '2026-10-12'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: 'aafb01d6b7478dbc36df5a54ab0fd7d69f94e968'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `freight-tenders/` doesn't exist yet. light-factory has never been run against a realistic codebase, and before any domain code can land, the repo needs two independently buildable/testable projects wired together end to end.

**Approach:** Scaffold a Spring Boot backend and an Angular frontend as separate projects under `freight-tenders/`, each with its own CI job (build, test, lint), connected by one trivial path: a backend health endpoint rendered on an Angular page behind a German-language label.

## Boundaries & Constraints

**Always:** `freight-tenders/` builds, tests, and lints independently of light-factory's own Python tooling. Backend code, API, domain model, and docs stay English; all UI-facing (Angular template) text is German. New CI lives in its own workflow file, separate from `.github/workflows/light-factory.yml`.

**Never:** Do not wire this CI into light-factory's per-repo checks config (that's entry 7, which depends on this entry). Do not add a security-scanning step (stays a skipped placeholder per epic decision). Do not model any tender domain/API yet (entries 2–6). Do not deploy anywhere.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Backend reachable | Angular app loads, backend running on :8080 | Page shows German label + live "UP" status from `GET /api/health` | No error expected |
| Backend unreachable | Angular app loads, backend down/unreachable | Page shows the German label with a fallback "nicht verfügbar" state, no uncaught error | `catchError` on the HTTP call maps failure to the fallback text |

</frozen-after-approval>

## Code Map

- `freight-tenders/` -- doesn't exist yet, nothing to reuse.
- `.github/workflows/light-factory.yml` -- existing workflow; style reference only, not touched.
- Root `.gitignore` -- scoped to IDE/OS/Python/BMad; backend/frontend ignores belong in each sub-project's own generated `.gitignore`.
- Versions confirmed live (Maven Central/npm, 2026-10-12): Spring Boot parent `4.1.1`, Java `25` (LTS, matches local JDK); `@angular/cli` `22.2.2` (needs Node `^22.22.3 || ^24.15.0 || >=26.0.0`; local is `26.11.1`); `@angular-eslint/schematics` `22.6.0`; `spotless-maven-plugin` `3.10.4`.
- Angular 22's default `ng new` uses the esbuild/Vite builder and `@angular/build:unit-test` (Vitest) -- no Karma/Chrome needed in CI.

## Tasks & Acceptance

**Execution:**
- [x] `freight-tenders/backend/pom.xml` -- Spring Boot starter-parent `4.1.1`, Java `25`, `spring-boot-starter-web` + `spring-boot-starter-test` + `spotless-maven-plugin` (google-java-format) -- independent, buildable/testable/lintable Maven project
- [x] `freight-tenders/backend/src/main/java/.../FreightTendersApplication.java` -- standard Spring Boot bootstrap class
- [x] `freight-tenders/backend/src/main/java/.../health/HealthController.java` -- `GET /api/health` returns `{"status":"UP"}` -- backend half of the trivial E2E path
- [x] `freight-tenders/backend/src/test/java/.../health/HealthControllerTest.java` -- MockMvc test asserting 200 + `status":"UP"`
- [x] `freight-tenders/frontend/` -- scaffold via `ng new frontend` (standalone components, SCSS, no SSR, no e2e framework) -- independent, buildable/testable Angular project
- [x] `freight-tenders/frontend/` -- `ng add @angular-eslint/schematics` -- lint tooling (`ng lint`)
- [x] `freight-tenders/frontend/src/app/app.component.ts` + `.html` -- `HttpClient` call to `/api/health` with `catchError` fallback; renders result under the German label "Systemstatus" -- frontend half of the trivial E2E path
- [x] `freight-tenders/frontend/src/app/app.component.spec.ts` -- tests both the live-value and fallback branches against a mocked `HttpClient`
- [x] `freight-tenders/frontend/proxy.conf.json` + `angular.json` serve config -- proxies `/api` to `localhost:8080` for local dev parity, so no CORS config is needed on the backend
- [x] `freight-tenders/README.md` -- short: how to build/test/run each project locally
- [x] `.github/workflows/freight-tenders.yml` -- new workflow, triggered on push/PR touching `freight-tenders/**`; two jobs -- `backend` (`mvn -B verify`, `mvn spotless:check`) and `frontend` (`npm ci`, `npm run build`, `npm test -- --watch=false`, `npm run lint`)

**Acceptance Criteria:**
- Given a fresh clone, when the `freight-tenders.yml` workflow runs on a PR touching `freight-tenders/**`, then both the `backend` and `frontend` jobs go green (build, test, lint).
- Given the backend running on `:8080` and the frontend served via `ng serve` (proxying `/api`), when the Angular app loads, then it shows the live health status under the German label.
- Given the backend unreachable, when the Angular app loads, then it shows the fallback text instead of an unhandled error.

## Implementation Notes

Built exactly per plan with two forced adaptations, both discovered only by actually running the builds, not knowable from version numbers alone:

1. **Spring Boot 4.1.1's module split.** `spring-boot-starter-web` compiles fine but is now deprecated in favor of the Servlet/MVC-specific `spring-boot-starter-webmvc`; used the latter. More importantly, `@WebMvcTest`/`MockMvc` autoconfiguration no longer ships in `spring-boot-starter-test` (that artifact's test-autoconfigure jar now only covers `jdbc`/`json`) -- it moved to a new per-stack test starter, `spring-boot-starter-webmvc-test` (which still pulls in `spring-boot-starter-test` transitively for JUnit/AssertJ/Mockito), and the `@WebMvcTest` annotation itself moved package from `org.springframework.boot.test.autoconfigure.web.servlet` to `org.springframework.boot.webmvc.test.autoconfigure`. Used `MockMvc.perform(get(...)).andExpect(...)` (not `MockMvcTester`) for the test body -- same intent as the plan's "MockMvc test asserting 200 + `status":"UP"`", just the classic fluent API.
2. **Angular 22's root-component naming.** `ng new` no longer generates `app.component.ts`/`.html`/`.spec.ts` -- current style guide drops the `.component` suffix, so the generated files are `app.ts`/`app.html`/`app.spec.ts` (class `App`). Edited those instead; same files, same role.

Backend: `com.senacor.freighttenders` groupId/package (no existing convention in the repo to match; chosen since no naming guidance existed). `HealthController` returns `Map.of("status", "UP")` via Jackson, asserted with `content().json(...)`. `spotless-maven-plugin` is deliberately *not* bound to any lifecycle phase, so `mvn -B verify` and `mvn spotless:check` stay two distinct, separately-failing CI steps per the plan's own split Verification commands -- caught one real formatting violation (a wrapped Javadoc comment) via `spotless:apply`.

Frontend: `provideHttpClient()` added to `app.config.ts` (not scaffolded by `ng new` on its own). `App`'s constructor fires the `/api/health` `GET` immediately, mapped to `response.status` with `catchError(() => of('nicht verfügbar'))`, written to a `signal` rendered in `app.html` under `<h1>Systemstatus</h1>`. `app.spec.ts` uses `provideHttpClientTesting()` + `HttpTestingController` to flush both a `{status:'UP'}` success and a simulated network `error()`, asserting the rendered text in each case -- 3/3 tests pass.

`freight-tenders/backend/.gitignore` added by hand (Maven doesn't generate one; `ng new` generates the frontend's own). Root `.gitignore` and `.github/workflows/light-factory.yml` were not touched; `.github/post-implementation-checks.yml` was not touched either (verified via `git diff`, empty) -- confirms the "Never" boundary (no wiring into light-factory's per-repo checks config) held.

**Verification performed (all per the plan's Verification section, run fresh from clean clone state):**
- `cd freight-tenders/backend && mvn -B verify` -- `BUILD SUCCESS`, `HealthControllerTest` ran and passed (1/1).
- `cd freight-tenders/backend && mvn spotless:check` -- clean, 0 violations (after one `spotless:apply` fix during development).
- `cd freight-tenders/frontend && npm ci && npm run build` -- succeeded, `dist/frontend` produced.
- `cd freight-tenders/frontend && npm test -- --watch=false` -- 3/3 specs passed (create, live-UP branch, fallback branch).
- `cd freight-tenders/frontend && npm run lint` -- "All files pass linting."
- Manual end-to-end check: ran `mvn spring-boot:run` (backend on :8080) and `npm start` (frontend on :4200, Angular's dev-server `proxyConfig` -> `proxy.conf.json`) together. `curl http://localhost:4200/api/health` returned `{"status":"UP"}` proxied live from the backend. Killed the backend and re-curled the same URL -- proxy returned `502` (i.e. the real `HttpClient` call the frontend makes would error, exercising the same `catchError` path the unit test simulates), confirming the fallback wiring is realistic, not just unit-test theater.
- Confirmed via `git status`/`git add -A -n` that no `target/`, `dist/`, `node_modules/`, or `.angular/` build output would be committed -- both `.gitignore` files hold.

No security-scanning step was added (matches the epic's "stays a skipped placeholder" decision -- out of scope for this entry anyway). No tender domain/API code was added. Nothing deploys anywhere. CI wiring into light-factory's own checks config is explicitly entry 7's job, untouched here.

## Plan Change Log

## Review Triage Log

### Review pass 1 (quick, iteration 0) — 2026-10-12

Verdict counts: high: 0, medium: 0, low: 0, false: 2, maybe-false: 0

- `freight-tenders/frontend/src/index.html:4` (`<title>Frontend</title>` left in English) — **false**, rejected. The plan's "Always" boundary scopes "all UI-facing text is German" explicitly to "(Angular template)" text; `index.html` is the static host page, not an Angular template, so the constraint doesn't reach it — not an ambiguous reading, the parenthetical is explicit.
- `freight-tenders/frontend/src/app/app.ts` (health `HttpClient.get()` fired from the constructor rather than `ngOnInit()`) — **false**, rejected. No named harm: all 3 specs pass (both the reachable and unreachable branches) and the manual E2E check confirms correct behavior; the reviewer itself called it "not a bug," and "non-idiomatic" with no demonstrated caller divergence or failure mode is not a defect.

## Design Notes

Plain `HealthController`, not Spring Boot Actuator's `/actuator/health` -- avoids actuator's broader disk/db checks for what's meant to stay a trivial tracer bullet.

Dev wiring uses Angular's `proxyConfig`, not backend CORS headers -- keeps CORS untouched until a real cross-origin need exists.

## Verification

**Commands:**
- `cd freight-tenders/backend && mvn -B verify` -- expected: `BUILD SUCCESS`, `HealthControllerTest` passes
- `cd freight-tenders/backend && mvn spotless:check` -- expected: no formatting violations
- `cd freight-tenders/frontend && npm ci && npm run build` -- expected: build succeeds
- `cd freight-tenders/frontend && npm test -- --watch=false` -- expected: all specs (incl. both health-display branches) pass
- `cd freight-tenders/frontend && npm run lint` -- expected: no lint errors

**Manual checks (if no CLI):**
- Run backend (`mvn spring-boot:run`) and frontend (`npm start` with the dev proxy) together; open `http://localhost:4200` and confirm the page shows the German-labeled live "UP" status.

<!-- bmad:context -->
<!-- Verified 2026-10-12 against 8d61d21. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## freight-tenders frontend

Angular 22 (standalone, signals, Vitest) frontend for the freight tender domain. All three pages call the backend through one shared `TenderApiService`. Independent of the backend's own build and of light-factory's own tooling; proxied to the backend locally via `proxy.conf.json`.

## Policy

- All user-facing text (labels, headings, button text, messages) is German; the API/domain model (status enum values, field names) stays English — map English domain values to German display labels at render time (mirrors the backend's own English-code/German-UI split).

## Where things are

- Shared HTTP boundary: `src/app/tender-api.ts` (`TenderApiService`, `providedIn: 'root'`) — the only place `HttpClient` is injected; components never call it directly.
- Each page: `src/app/<feature>/` flat folder (`.ts`/`.html`/`.scss`/`.spec.ts` co-located) — mirrors the backend's one-flat-folder-per-feature convention.

## Running and verifying

- `npm ci && npm run build` — production build.
- `npm test -- --watch=false` — Vitest unit tests; the bare `ng test`/`npm test` default watches and never exits.
- `npm run lint` — `ng lint`.
- `npm run static-analysis` — `eslint -c eslint.static-analysis.config.js .`; bug-pattern rules (`eslint-plugin-sonarjs`'s recommended set), independent of `npm run lint`'s style/formatting config (`eslint.config.js`) — a separate config file and script, since `ng lint` is pinned to one config via `angular.json`.
- `npm start` — dev server on `:4200`, proxying `/api` to `localhost:8080` — the backend must already be running locally.

## Conventions that differ from defaults

- Functional DI via `inject()` everywhere (services, components, `Router`/`ActivatedRoute`/`FormBuilder`) — never constructor injection (the backend's own convention is the opposite; each stack follows its own idiom).
- State is `signal()`/`computed()`; RxJS is used only at the `HttpClient` boundary inside `tender-api.ts` and collapsed into signals immediately after `subscribe` — never expose an `Observable` to a template.
- HTTP errors: `.pipe(catchError(() => of(null)))`, then check `=== null` to set a German error-message signal — no `HttpInterceptor`, no central error service.
- Forms use `ReactiveFormsModule` + `FormBuilder.nonNullable.group(...)` with per-field `Validators` — client-side validation mirrors the backend's Bean Validation rules.
- No `.component.ts`/`Component`/`Service` suffix on file or class names (one exception: `TenderApiService` keeps `Service`) — Angular 22 schematic default, not a local override.
- No `environment.ts`/`environment.prod.ts` — relative `/api/...` URLs only, differentiated by the dev-only `proxy.conf.json`.
- Tests mock HTTP exclusively via `provideHttpClientTesting()` + `HttpTestingController`, always paired with `afterEach(() => httpMock.verify())`.
- DOM assertions go through `data-testid` attributes exclusively — never CSS classes or structural queries.
- Test names are descriptive sentences (e.g. `'shows a German loading message before the response arrives'`), not a `Method_State_Expected` convention — mirrors the backend.

<!-- /bmad:context -->

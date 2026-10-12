<!-- bmad:context -->
<!-- Verified 2026-10-12 against 8d61d21. Managed by bmad-project-context; edits inside this block are replaced on refresh. Keep anything you want preserved outside the markers. -->

## freight-tenders backend

Spring Boot 4.1.1 / Java 25 REST API for the freight tender domain (`src/main/java/com/senacor/freighttenders/`). Independent of light-factory's own Python tooling and of the frontend's build — built/tested/linted via Maven only.

## Policy

- Backend code, API, domain model, and docs (README, Javadoc) stay English — German is frontend-only, UI-facing text.
- New or changed request DTOs validate input via Jakarta Bean Validation (`@Valid` + constraint annotations) at the API boundary. Wired for `CreateTenderRequest` only (`spring-boot-starter-validation` is a dependency; `TenderExceptionHandler` maps `MethodArgumentNotValidException` to a 400 with `violations`); `AddOfferRequest`/`AddRemarkRequest` don't have it yet.

## Running and verifying

- `mvn -B verify` — build + test (JUnit 5/Mockito/AssertJ; `@WebMvcTest`+`MockMvc` and `@DataJpaTest` slices).
- `mvn spotless:check` — formatting lint, run as its own step; deliberately *not* bound to the `verify` lifecycle, so a clean `mvn verify` does not mean formatting is clean — always run both (caught one real violation this way during ticket 1).
- `mvn spotless:apply` — auto-fixes what `spotless:check` finds.
- `mvn spotbugs:check` — static analysis (bug patterns), also run as its own step, independent of `spotless:check`'s formatting-only result; `spotbugs-exclude.xml` documents the three findings suppressed as real framework-pattern false positives (JPA `@ManyToOne` getters, Spring constructor injection) rather than weakening the ruleset.

## Conventions that differ from defaults

- Services are `@Service` directly (constructor injection, `private final` fields only — never field/setter injection or `@Autowired` on a field).
- One flat package per feature (`tender/`, `health/`) holds everything for that feature — entity, DTOs/records, domain exceptions, repository, service, controller, and its own `@RestControllerAdvice`. Never split into `model/`/`config/`/layer sub-packages.
- DTOs are Java records, never the entity itself, returned from controllers.
- IDs are database-generated `Long` (JPA `IDENTITY`), exposed directly in responses — not UUIDs.
- API paths are unversioned (`/api/tenders`, not `/api/v1/tenders`).
- Error responses are `{error, message, path, timestamp}` (plus a `violations` array for 400s).
- Domain exceptions are unchecked (`extends RuntimeException`), named `<Entity>NotFoundException`/`<Entity>ClosedException`-style, message set via `super("...")` directly (no message constants), never carry a Spring annotation.
- Controllers never catch exceptions — they propagate to the feature's own advice.
- Test names are descriptive camelCase sentences (e.g. `addRemarkOnClosedTenderReturns409`), not a `Method_State_Expected` convention.

## Known pitfalls

- Spring Boot 4.1.1 renamed/relocated several starters: use `spring-boot-starter-webmvc` (not the deprecated `spring-boot-starter-web`), `spring-boot-starter-webmvc-test` for `@WebMvcTest`/`MockMvc`, and `spring-boot-starter-data-jpa-test` for `@DataJpaTest` — all moved out of the generic `spring-boot-starter-test`; the name in older tutorials is wrong here.

<!-- /bmad:context -->

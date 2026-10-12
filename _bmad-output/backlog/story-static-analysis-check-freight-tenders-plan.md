---
title: 'freight-tenders gets real static_analysis commands -- SpotBugs backend, ESLint bug-pattern frontend, both pipelines'
type: 'feature'
ticket: '2'
created: '2026-10-12'
status: 'done'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: 'eb1fc6248a1676c67ec1b4abff694e12d6f9a848'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Plan A made `static_analysis` a fifth fixed check name but left it unconfigured in this repo (`status: "skipped"`). freight-tenders has no real static-analysis tooling in either pipeline that checks it.

**Approach:** Configure `static_analysis` for freight-tenders as Maven SpotBugs (backend) and a dedicated ESLint bug-pattern config (frontend), wiring real commands into `.github/post-implementation-checks.yml`'s already-present `static_analysis:` key and into `.github/workflows/freight-tenders.yml`'s own `backend`/`frontend` jobs, so both pipelines run the identical check.

## Boundaries & Constraints

**Always:** Run SpotBugs and the ESLint bug-pattern plugin as local CLI/Maven-plugin tooling only (AD-7: no new external/SaaS dependency). Keep `static_analysis`'s result independent of `lint`'s — a formatting violation must never fail it and vice versa. Mirror `spotless-maven-plugin`'s existing pattern for `spotbugs-maven-plugin`: an explicitly pinned version, not bound to any lifecycle phase. If SpotBugs or the ESLint config flags something real in the existing codebase, fix the code (preferred) or document a suppression with a reason — never weaken the ruleset just to go green.

**Never:** Change what `build`/`test`/`lint`/`security` run or how they're evaluated. Fold `static_analysis` into `fix_loop_graph.py`'s build/test-only regression recheck (AD-11). Touch `eslint.config.js` (the existing style/lint config) — the bug-pattern rules get their own, separate config file.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Backend finding | freight-tenders/backend has a bug SpotBugs flags | `mvn spotbugs:check` fails in both light-factory's `checks` job and freight-tenders.yml's `backend` job | step fails but doesn't block sibling checks; the fail-loop still fails the job |
| Frontend finding | freight-tenders/frontend has a pattern the new ESLint config flags | the new script fails in both pipelines, independent of `npm run lint`'s own result | same as above |
| Clean repo state | no bug patterns present in either project | `static_analysis` records `status: "pass"` in both pipelines | no error |
| Existing four checks | `build`/`test`/`lint`/`security` as configured today | unchanged pass/skip results | no behavior change |

</frozen-after-approval>

## Code Map

- `freight-tenders/backend/pom.xml` -- `<build><plugins>` currently holds `spring-boot-maven-plugin` (version inherited) and `spotless-maven-plugin` (explicitly pinned `3.10.4`, no lifecycle binding — its own comment explains why: so CI runs `mvn spotless:check` as an independent step from `mvn -B verify`). No `<dependencyManagement>` exists; Spring Boot's parent POM (`spring-boot-starter-parent:4.1.1`) manages neither spotless nor spotbugs. Add `com.github.spotbugs:spotbugs-maven-plugin`, explicitly versioned, unbound from any lifecycle phase, mirroring spotless's comment/pattern exactly.
- `freight-tenders/frontend/package.json` -- `scripts.lint` is `"ng lint"` (leave unchanged); `devDependencies` has `eslint ^10.12.0`, `@eslint/js`, `typescript-eslint 8.71.0`, `angular-eslint 22.6.0`, no sonarjs. Add `eslint-plugin-sonarjs` devDependency and a new `"static-analysis"` script.
- `freight-tenders/frontend/eslint.config.js` -- existing flat config (`.ts` block: `eslint.configs.recommended` + `tseslint.configs.recommended`/`stylistic` + `angular.configs.tsRecommended`; `.html` block separately). Reference only — do not edit.
- `freight-tenders/frontend/eslint.static-analysis.config.js` (new) -- flat config scoped to `**/*.ts`, reusing `tseslint.configs.recommended` for TS parsing plus `eslint-plugin-sonarjs`'s recommended rules; the new `"static-analysis"` script invokes it via `eslint -c eslint.static-analysis.config.js .` (raw ESLint CLI — `ng lint` is pinned to one config via `angular.json` and can't swap configs per invocation).
- `.github/post-implementation-checks.yml` -- `checks.static_analysis:` key already exists (added empty by the prior plan); fill in its 2 commands, mirroring `lint:`'s shape (a `bash -c` wrapper with `JAVA_HOME_25_X64` for the backend, a plain `npm --prefix` call for the frontend).
- `.github/workflows/freight-tenders.yml` -- `backend` job: add a "Static analysis" step after "Lint (formatting)" (`mvn -B spotbugs:check`). `frontend` job: add a "Static analysis" step after "Lint" (`npm run static-analysis`).
- `freight-tenders/README.md` -- Backend section's command block (lines ~33-38) and Frontend section's (lines ~50-57): add the new local command to each, alongside the existing `mvn spotless:check`/`npm run lint`.
- `freight-tenders/backend/AGENTS.md` and `freight-tenders/frontend/AGENTS.md` -- each has a "Running and verifying" section listing local commands (`mvn -B verify`/`mvn spotless:check`; `npm run build`/`npm test`/`npm run lint`); add the new command to each.

## Tasks & Acceptance

**Execution:**
- [x] `freight-tenders/backend/pom.xml` -- add `spotbugs-maven-plugin`, pinned, unbound from any lifecycle phase -- gives the backend a real, independently-runnable `mvn spotbugs:check`
- [x] `freight-tenders/frontend/package.json` + `eslint.static-analysis.config.js` -- add `eslint-plugin-sonarjs` and the new script/config -- gives the frontend a bug-pattern check independent of its style lint
- [x] `.github/post-implementation-checks.yml` -- fill in `static_analysis:`'s 2 commands -- light-factory's `checks` job now actually runs them instead of skipping
- [x] `.github/workflows/freight-tenders.yml` -- add a "Static analysis" step to `backend` and `frontend` -- freight-tenders' own independent CI runs the same check
- [x] `freight-tenders/README.md` -- document the new local commands
- [x] `freight-tenders/backend/AGENTS.md`, `freight-tenders/frontend/AGENTS.md` -- document the new local commands in "Running and verifying"

**Acceptance Criteria:**
- Given `freight-tenders/backend` with a bug pattern SpotBugs flags, when `static_analysis` runs in either light-factory's `checks` job or freight-tenders.yml's `backend` job, then `mvn spotbugs:check` fails the check in both, and passes once the pattern is fixed
- Given `freight-tenders/frontend` with a pattern the new ESLint config flags, when `static_analysis` runs in either pipeline, then the new script fails, independent of `npm run lint`'s own pass/fail
- Given today's `build`/`test`/`lint`/`security` commands and current repo state, when they run after this change, then each still records the same pass/skip result as before
- Given `freight-tenders/backend` and `freight-tenders/frontend` as they stand after this change (no introduced bug pattern), when `static_analysis` runs, then it records `pass` in both pipelines
- Given the full `factory/scripts/tests/` and `factory/graph/tests/` suite, when run after this change, then it still passes (no Python code changes, but rerun to confirm the config edit parses correctly)

## Implementation Notes

- `spotbugs-maven-plugin` pinned to `4.10.5.0` (latest at implementation time; `4.9.6.2` doesn't exist on Maven Central). First clean run against the existing backend found 9 real EI_EXPOSE_REP/EI_EXPOSE_REP2 bugs:
  - `TenderDetailResponse` (record) and `TenderExceptionHandler.ErrorResponse` (record) returned/stored their `List` fields by reference -- real DTO leaks, fixed with a compact-constructor `List.copyOf(...)` defensive copy (null-safe for `violations`, which is `null` outside 400s).
  - `Offer.getTender()`/`Remark.getTender()` (JPA `@ManyToOne` bidirectional association getters) and `TenderController`'s constructor (Spring constructor-injected singleton service, per AGENTS.md's mandated DI style) are framework-pattern false positives that can't be "fixed" without breaking the pattern -- suppressed via a new `freight-tenders/backend/spotbugs-exclude.xml`, each entry scoped to one class+method+bug-pattern with a reasoning comment, wired in via `spotbugs-maven-plugin`'s `<excludeFilterFile>`.
- `eslint-plugin-sonarjs` pinned to `^4.2.2` (current stable; peer-compatible with the frontend's `eslint ^10.12.0`). The new `eslint.static-analysis.config.js` found one real finding: `tender-create.spec.ts`'s "does not submit while the form is invalid" test asserted only via `httpMock.expectNone(...)` (which throws on failure but isn't an `expect()`/`assert()` call sonarjs's `assertions-in-tests` rule recognizes). Fixed by wrapping it as `expect(() => httpMock.expectNone(...)).not.toThrow()` -- same check, recognized assertion form -- rather than an eslint-disable comment, since a disable comment naming a sonarjs-only rule would itself fail the existing `eslint.config.js`-based `npm run lint` with "Definition for rule ... was not found" (that plugin isn't loaded there). Confirmed clean afterward on both `npm run lint` and `npm run static-analysis` independently.
- `.github/post-implementation-checks.yml`'s header comment ("that is `security` and `static_analysis` in this repo" for skipped checks) was updated to say just `security`, since it would otherwise misstate `static_analysis`'s new status; the `build`/`test`/`lint` command blocks themselves are untouched.
- Per this repo's documented pitfall (`run_checks.py` reads the checks config from `origin/main`, never the working tree, pre-merge), running `uv run factory/scripts/run_checks.py static_analysis --story-slug ... --run-id ...` against this branch pre-merge still returns `status: "skipped"` (reading the old `origin/main` config) -- expected, not a bug. Verified the new config and both commands directly instead: monkeypatched `_read_target_config` to force the working-tree fallback and called `run_check("static_analysis", ..., state_base=<tmpdir>)`, which returned `status: "pass"` running both the real `mvn spotbugs:check` and `npm run static-analysis`. This will read as `"pass"` for real once this change lands on `main`.

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens + orchestrator check, 2 findings):**
- `freight-tenders/backend/AGENTS.md` (the new `mvn spotbugs:check` bullet) — says "`spotbugs-exclude.xml` documents the two findings suppressed," but the file holds 3 `<Match>` blocks (`Offer.getTender()`, `Remark.getTender()`, `TenderController.<init>`). Verdict: **low** (confirmed via `grep -c "<Match>"` → 3). Route: **patch** — "the two findings" → "the three findings".
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md`'s AD-6 addendum (2026-10-12, ticket 2, written by the prior plan) still says `static_analysis` "is left unconfigured... records `status: "skipped"`... Real commands for freight-tenders are deferred to a separate plan" — now stale since this plan configured real commands. Not in this plan's original Code Map (an oversight, not an intentional exclusion), found by the orchestrator re-reading that addendum during review. Verdict: **low** (doc-accuracy only, no runtime effect). Route: **patch** — append a short dated note to that addendum recording that this plan supplied the real commands.

## Design Notes

The frontend gets a **second** flat ESLint config file, not a second ruleset bolted onto the existing one: `ng lint` is pinned to one config via `angular.json`, so an independently pass/fail-able bug-pattern check needs its own `eslint -c <file> .` invocation. The backend's `spotbugs-maven-plugin` follows `spotless-maven-plugin`'s own existing pattern exactly: an explicitly pinned version (Spring Boot's parent POM manages neither) and no lifecycle binding, so `mvn spotbugs:check` is an independently-runnable goal, not a side effect of `mvn verify`.

## Verification

**Commands:**
- `mvn -f freight-tenders/backend/pom.xml spotbugs:check` -- expected: passes clean against current backend code (if it doesn't, fix or deliberately document a suppression — see Boundaries)
- `npm --prefix freight-tenders/frontend run static-analysis` -- expected: passes clean against current frontend code
- `npm --prefix freight-tenders/frontend run lint` -- expected: unaffected, still passes
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all 306 still pass
- `uv run factory/scripts/run_checks.py static_analysis --story-slug <any existing> --run-id <any existing>` -- expected: exits 0, writes `evidence/checks/static_analysis.json` with `status: "pass"` (no longer `"skipped"`)

**Manual checks (if no CLI):**
- Diff `.github/post-implementation-checks.yml`: `build`/`test`/`lint` blocks byte-for-byte unchanged; only `static_analysis:`'s 2 commands are added.

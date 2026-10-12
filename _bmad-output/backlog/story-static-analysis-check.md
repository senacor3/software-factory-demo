---
id: 2
type: story
title: "static_analysis runs as a fifth mechanical check, backed by SpotBugs and an ESLint bug-pattern config for freight-tenders"
parent: none
covers: []
after: []
assignee: ""
refined: true
hitl: false
risk: medium
estimate: ""
---

# static_analysis runs as a fifth mechanical check, backed by SpotBugs and an ESLint bug-pattern config for freight-tenders

## Description

Today `run_checks.py` recognizes exactly four check names — `build`, `test`, `lint`, `security` — fixed by AD-6's addendum and enforced by its `CHECK_NAMES` tuple and `.github/workflows/light-factory.yml`'s four fixed steps in the `checks` job. This adds `static_analysis` as a fifth fixed check, wired the same way through `.github/post-implementation-checks.yml` and that job, with a new AD-6 addendum documenting it. freight-tenders' backend configures it as Maven SpotBugs (`mvn spotbugs:check`); its frontend configures it as a separate ESLint config/script carrying bug-pattern rules (e.g. `eslint-plugin-sonarjs`), distinct from the existing style/formatting `lint` script. The same two commands are wired into `.github/workflows/freight-tenders.yml`'s existing backend and frontend jobs, so freight-tenders' own CI runs the identical check independently of light-factory's pipeline.

## Acceptance Criteria

1. **A fifth check name is recognized**
   **Given** `.github/post-implementation-checks.yml`'s `checks:` mapping
   **When** it names a `static_analysis:` key
   **Then** `run_checks.py` accepts it the same way it accepts `build`/`test`/`lint`/`security`, and a key outside the five still fails config validation by name

2. **A `static_analysis` subcommand exists and behaves like the other four**
   **Given** the `run_checks.py static_analysis` subcommand
   **When** it runs against this repo's config
   **Then** it runs the configured commands in order, stops at the first failure, and writes `evidence/checks/static_analysis.json` the same way the other four checks write theirs

3. **No configured command means skipped, never pass**
   **Given** a repo's config with no `static_analysis:` commands listed
   **When** the check runs
   **Then** it records `status: "skipped"`, never `"pass"` — the same safety net `security` already relies on

4. **The `checks` job runs it as a fifth direct step**
   **Given** a run of the `checks` job in `.github/workflows/light-factory.yml`
   **When** `static_analysis` fails
   **Then** "Fail job if any check failed" fails the job for it exactly as it does today for a failing `build`, `test`, `lint`, or `security` step — no change to how the other four are evaluated

5. **freight-tenders backend fails on a real SpotBugs finding**
   **Given** `freight-tenders/backend` with a bug pattern SpotBugs flags (e.g. a null-pointer-prone dereference)
   **When** the `static_analysis` check runs, in either `.github/workflows/light-factory.yml`'s `checks` job or `.github/workflows/freight-tenders.yml`'s `backend` job
   **Then** `mvn spotbugs:check` fails the check in both pipelines, and passes once the pattern is fixed

6. **freight-tenders frontend fails on a real bug-pattern finding, separately from style lint**
   **Given** `freight-tenders/frontend` with a bug pattern the chosen ESLint bug-pattern config flags
   **When** the `static_analysis` check runs, in either `.github/workflows/light-factory.yml`'s `checks` job or `.github/workflows/freight-tenders.yml`'s `frontend` job
   **Then** the static-analysis script fails the check in both pipelines while the existing `npm run lint` script's pass/fail is unaffected by that finding

7. **Today's four checks keep their current results**
   **Given** `freight-tenders/` and `factory/` as they stand before this change
   **When** `build`, `test`, `lint`, and `security` run after this change
   **Then** each records the same pass/skip result it recorded before — adding the fifth check changes no existing check's outcome

## Boundaries

- Must not change: the pass/fail/skip behavior or commands of `build`, `test`, `lint`, or `security` for `factory/` or either freight-tenders project; `security` stays a permanent `skipped` placeholder in this repo (decision below).
- Must not introduce an external SaaS dependency (AD-7 limits this repo's external dependencies to GitHub and Claude Code) — both SpotBugs and the ESLint plugin run as local CLI/Maven-plugin tooling.

## References

- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-6 (fixed check names, the per-repo config, and its addendum pattern) and AD-7 (external dependencies scoped to GitHub + Claude Code)
- code — factory/scripts/run_checks.py, `CHECK_NAMES`
- code — .github/workflows/light-factory.yml, the `checks` job's four check steps and its "Fail job if any check failed" step
- code — .github/post-implementation-checks.yml, the current `checks:` mapping for `factory/` and both freight-tenders projects
- code — .github/workflows/freight-tenders.yml, the `backend` and `frontend` jobs this adds a step to
- code — freight-tenders/backend/pom.xml, its current plugin set (no SpotBugs plugin configured yet)
- code — freight-tenders/frontend/package.json, its current `scripts` (the existing `lint` script, kept separate from the new one)

## Notes

- Decision: `static_analysis` is a new, fifth fixed check name, not folded into the existing `lint` check — keeps formatting/style (`spotless:check`, the existing `npm run lint`) and bug-pattern analysis (SpotBugs, the new ESLint config) under separate pass/fail status, mirroring how `build` and `test` stay separate today (user's call, 2026-10-12).
- Decision: backend static analysis is Maven SpotBugs (`mvn spotbugs:check`); frontend static analysis is a separate ESLint config/script carrying bug-pattern rules (e.g. `eslint-plugin-sonarjs`), distinct from the existing style-focused `lint` script (user's call, 2026-10-12).
- Decision: filed as a standalone backlog story with no epic, since every `initiative-light-factory` epic is closed (`status: done`) and this is a single, self-contained addition to an already-proven mechanism, not new epic-scale scope (user's call, 2026-10-12).
- Decision: `run_checks.py` writes its own AD-6 addendum documenting the fifth check name as part of this story's build, the same way the per-repo-config and toolchains addenda were each authored during their own story's build rather than spiked first.
- Assumption: no new runner toolchain is needed — SpotBugs runs through the backend's existing Java/Maven setup and the ESLint plugin through the frontend's existing Node setup; confirm at build time if the chosen plugin's version needs a newer Node than this repo's config already sets.
- Open question: none blocking the start of this ticket; the exact bug-pattern ESLint plugin/package, its rule set, and whether any existing SpotBugs findings in `freight-tenders/backend` need fixing or suppressing to go green are left to the builder.
- Deferred (2026-10-12, build-plan token-count gate), now resolved: this ticket's build was split into two plans rather than one, since the combined plan ran ~2,828 tokens against a 900-1600 target. Plan A (`story-static-analysis-check-plan.md`, built) delivered AC1-4 and AC7 — the generic `static_analysis` mechanism, left unconfigured (`skipped`) like `security` is today. Plan B (`story-static-analysis-check-freight-tenders-plan.md`, built 2026-10-12) delivered AC5-6 — SpotBugs (`spotbugs-maven-plugin`, with `spotbugs-exclude.xml` suppressing 3 documented framework-pattern false positives) for the backend and a dedicated ESLint bug-pattern config (`eslint-plugin-sonarjs`) for the frontend, wired into both `.github/post-implementation-checks.yml` and `.github/workflows/freight-tenders.yml`. Both plans' real-command discovery runs each found and fixed one genuine issue in existing code (2 DTO list-exposure bugs in the backend, 1 test-assertion-form issue in the frontend) rather than suppressing them, per this ticket's "fix the code (preferred)" posture. Recorded here rather than an initiative's `deferred-work.md` since this ticket has no epic/initiative (`parent: none`); user's call to split, 2026-10-12.
- Closure (2026-10-12, user's call): both plans built, reviewed, and committed to `main` (`bb8ea69`, `eb8fb18`); all 7 acceptance criteria met. Marked `done` by editing both plan files' `status` directly, rather than via `tickets.py mark` — that script's `find`/`mark` assume one plan per ticket and refuse on this ticket's two (`"... are both plans for ticket 2"`), an edge case the token-count-gate split created that the tooling doesn't model; recorded here so a future `tickets.py status`/`next` reader isn't surprised by the manual edit.

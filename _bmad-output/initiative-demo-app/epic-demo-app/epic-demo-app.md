---
tracker_id: ""
key: ""
type: epic
title: "Build and wire the freight tender demo app"
parent: initiative-demo-app
covers: [D1, D2, D3, D4]
after: []
assignee: ""
risk: medium
estimate: ""
estimate_basis: "envelope"
---

# Build and wire the freight tender demo app

## Description

A Spring Boot backend and Angular frontend modeling freight-transport tender management, realistic enough to give light-factory's pipeline a genuine build/test/lint baseline, with the pipeline's existing workflow blueprint wired onto its repo and run at least once end to end on a real story.

## Outcome

light-factory has been exercised against a realistic codebase, not just its own fixture stories — the initiative's own Outcome, named not restated.

## Requirements

- D1 (reused): A minimal but realistic full-stack application exists in its own repo, buildable and testable with standard tooling, independent of light-factory.
- D2 (reused): Models freight-transport tenders (origin → destination, open/closed status) with remarks and supplier offers attached; supports an overview of open/closed tenders, creating a new tender, and viewing a tender to add remarks/offers. Non-trivial rule: remarks and offers can only be added to an open tender; once closed, a tender is read-only. All UI-facing text is German; backend code, API, domain model, and docs stay English (user's call, 2026-10-10).
- D3 (reused): light-factory's workflow blueprint is wired onto this repo, after `initiative-light-factory`'s `epic-pipeline-open-issues` is built, and has run at least one real story through it end to end.
- D4 (reused): The repo and that completed story are presentable as a demo without extra prep.

## Done when

1. The app builds and its test/lint suite passes locally and in CI, independent of light-factory.
2. A tender can be created, listed in the open/closed overview, viewed, and gets remarks and offers added while open; adding either to a closed tender is rejected — exercised by both a real test suite and the Angular UI.
3. light-factory's workflow blueprint is wired onto this repo (environments, secrets, `.github/workflows/light-factory.yml`) and has run at least one real story through it end to end, both gates exercised.
4. The repo and that completed story are presentable as a demo without extra prep.

## Boundaries

The app's own code and repo, and the light-factory wiring on that repo. Not light-factory's own pipeline logic. Not production deployment of the app. UI copy (labels, buttons, messages shown to the user) is German throughout; backend code, API, domain model, and all documentation (README, code comments) stay English.

## References

- parent — _bmad-output/initiative-demo-app/initiative-demo-app.md
- sibling — _bmad-output/initiative-light-factory/initiative-light-factory.md, owns the `.github/workflows/light-factory.yml` blueprint and its `factory/`/`.claude/skills/` companions this epic copies in — a real file dependency, sequenced after `epic-pipeline-open-issues` (see Notes)

## Notes

- Decision: the blueprint copy (Done when 3) waits on `initiative-light-factory`'s `epic-pipeline-open-issues` being built, so this repo starts from the fixed blueprint rather than one with four known gaps. This epic has no formal `after` on that epic (different initiative, different tree) — tracked here and mirrored in `epic-pipeline-open-issues.md`'s Notes instead (2026-10-10).
- Decision: "production delivery" here means build/test/CI passing and a real light-factory run against this repo, not shipping the app to production users (Boundaries excludes that) — matches the initiative's own Notes (2026-10-10).
- Decision: domain is freight-transport tender management; D3/wiring stays inside this one epic as closing entries rather than splitting into a second epic (user's call, 2026-10-10 — see initiative Notes).
- Decision: UI text is German throughout; backend code, API, domain model, and documentation stay English (user's call, 2026-10-10). Entries 1, 5, and 6 updated accordingly.
- Decision: inception complete (2026-10-10) — 9 entries in `tickets.toml`: tracer bullet entry 1 (scaffold + CI, `hitl=false` — nothing in it needs a person), domain/API/frontend entries 2-6, light-factory wiring entry 7, closing refactor sweep entry 8, closing end-to-end suite entry 9 (first real light-factory run + demo polish), mirroring `epic-light-factory-pipeline`'s own structure. Validated against `checks.dependencies`/`checks.set`/`checks.ticket` via independent review, which caught and fixed two real issues: entry 7's `after` was tightened from `[6]` to `[1]` (wiring the pipeline needs only the repo/CI to exist, not the domain — it touches none of entries 2-6's `src/` files, so it can build alongside them) and entry 3/4's verify text was sharpened to say explicitly which layer (service vs. HTTP) enforces the open/closed rule, since entry 4 is where the real REST endpoints first exist.

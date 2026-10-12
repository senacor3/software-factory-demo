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

- D1 (reused): A minimal but realistic full-stack application exists under `freight-tenders/` in the light-factory repo, buildable and testable with standard tooling, independent of light-factory.
- D2 (reused): Models freight-transport tenders (origin → destination, open/closed status) with remarks and supplier offers attached; supports an overview of open/closed tenders, creating a new tender, and viewing a tender to add remarks/offers. Non-trivial rule: remarks and offers can only be added to an open tender; once closed, a tender is read-only. All UI-facing text is German; backend code, API, domain model, and docs stay English (user's call, 2026-10-10).
- D3 (reused): light-factory's pipeline in this repo is pointed at the demo app through its per-repo checks config, after `initiative-light-factory`'s `epic-pipeline-hardening` entry 1 is built, and has run at least one real story against the app end to end.
- D4 (reused): The repo and that completed story are presentable as a demo without extra prep.

## Done when

1. The app builds and its test/lint suite passes locally and in CI, independent of light-factory.
2. A tender can be created, listed in the open/closed overview, viewed, and gets remarks and offers added while open; adding either to a closed tender is rejected — exercised by both a real test suite and the Angular UI.
3. The pipeline's build, test, and lint checks run the demo app's own commands (via the checks config), and it has run at least one real story against the app end to end, both gates exercised.
4. The repo and that completed story are presentable as a demo without extra prep.
5. The review agent's instructions are extended, and a live run on a freight-tenders story shows the review applying them (see Notes).

## Boundaries

The app's own code under `freight-tenders/`, its CI, and the checks config that points light-factory's pipeline at it. Not light-factory's own pipeline logic. Not production deployment of the app. UI copy (labels, buttons, messages shown to the user) is German throughout; backend code, API, domain model, and all documentation (README, code comments) stay English.

## References

- parent — _bmad-output/initiative-demo-app/initiative-demo-app.md
- sibling — _bmad-output/initiative-light-factory/initiative-light-factory.md, owns the pipeline and its checks-config mechanism; entry 7 waits on `epic-pipeline-hardening` entry 1 (see Notes)

## Notes

- Superseded 2026-10-11 (see the last notes): the blueprint copy (Done when 3) waits on `initiative-light-factory`'s `epic-pipeline-open-issues` being built, so this repo starts from the fixed blueprint rather than one with four known gaps. This epic has no formal `after` on that epic (different initiative, different tree) — tracked here and mirrored in `epic-pipeline-open-issues.md`'s Notes instead (2026-10-10).
- Decision: "production delivery" here means build/test/CI passing and a real light-factory run against this repo, not shipping the app to production users (Boundaries excludes that) — matches the initiative's own Notes (2026-10-10).
- Decision: domain is freight-transport tender management; D3/wiring stays inside this one epic as closing entries rather than splitting into a second epic (user's call, 2026-10-10 — see initiative Notes).
- Decision: UI text is German throughout; backend code, API, domain model, and documentation stay English (user's call, 2026-10-10). Entries 1, 5, and 6 updated accordingly.
- Decision: inception complete (2026-10-10) — 9 entries in `tickets.toml`: tracer bullet entry 1 (scaffold + CI, `hitl=false` — nothing in it needs a person), domain/API/frontend entries 2-6, light-factory wiring entry 7, closing refactor sweep entry 8, closing end-to-end suite entry 9 (first real light-factory run + demo polish), mirroring `epic-light-factory-pipeline`'s own structure. Validated against `checks.dependencies`/`checks.set`/`checks.ticket` via independent review, which caught and fixed two real issues: entry 7's `after` was tightened from `[6]` to `[1]` (wiring the pipeline needs only the repo/CI to exist, not the domain — it touches none of entries 2-6's `src/` files, so it can build alongside them) and entry 3/4's verify text was sharpened to say explicitly which layer (service vs. HTTP) enforces the open/closed rule, since entry 4 is where the real REST endpoints first exist.
- Decision (2026-10-11): the app lives under `freight-tenders/` in the light-factory repo, not in its own repo (user's call). Entry 7 no longer copies a blueprint; it adds the app's commands to the checks config. Entries 1, 7, and 9 and Requirements D1/D3, Done when 3, and Boundaries were reworded.
- Waits on `initiative-light-factory`'s `epic-pipeline-hardening` entry 1 because: until the checks are configurable they run only `factory/`'s Python code and would pass without building the app. No `after` can cross initiatives; entry 7 carries this as its `unknown`.
- Decision (2026-10-11): `security` stays a `"skipped"` placeholder in the pipeline (user's call) — three former gaps are closed, not four. Entry 9's walkthrough must not present a security check as real.
- Decision (2026-10-11): lint added to entry 1, so Done when 1's "test/lint suite" has an owner; the lint tools are chosen when entry 1 is built.
- Decision (2026-10-11): entries 7 and 9, the two hitl entries, were pulled into story files so their acceptance criteria are written before the build. Both are drafts (`refined` not set) until reviewed with the user.
- Decision (2026-10-11): entry 10, "Fix loop engaged on a live run", moved here from `initiative-light-factory`'s `epic-pipeline-hardening` (its entry 4) with its plan, placed after entry 7 and before the sweep (user's call). Two small pipeline stories there produced no review finding; the app's larger, cross-layer stories are a better chance. Done when 5 is added for it; it cites no D-requirement, so `covers = []`, and it closes the open half of `initiative-light-factory`'s Done-when 3.
- Decision (2026-10-11): entry 10 also gives the review agent more instructions (user's call). That edits `.claude/skills/light-factory-review/SKILL.md`, which is pipeline logic — a deliberate, single exception to this epic's Boundaries.
- Decision (2026-10-11): entry 10 narrowed to "Give the review agent more instructions" (user's call). The fix loop engaged live on the pipeline itself before the entry started — run `38150142797` (`stories/one-input-path-per-story-slug.md`, PR #12, merged as `c60279b`): one finding, one fix cycle, resolved within the cap — so the proof is no longer this epic's to deliver. Done when 5 was reworded to the review-instruction work, and the entry's plan was renamed to match its title.
- Decision (2026-10-12): entry 11, "Frontend: Ford-inspired UX redesign", added (user's call) -- restyles the three existing Angular pages per a new UX spine (`ux-freight-tenders-ui/DESIGN.md` + `EXPERIENCE.md`, Ford.de-inspired, sortable single-column-sort tables replacing the plain lists), no functional change. Placed after entry 6 (the last entry touching those pages) and before entry 8, whose `after` was extended to include it, so the sweep and the closing demo run (entries 8/9) reflect the final UI. Covers D2 (no new D-requirement -- it enhances the pages D2 already covers).
- Decision (2026-10-12): entry 8, the refactor sweep, found no formal deferred-work list, so it swept the loose ends entries 1-7, 10, and 11 left behind. Resolved, none with a behavior change: (1) `freight-tenders/README.md` describes the app as built instead of the scaffold; (2) `freight-tenders/frontend/README.md` replaces the Angular CLI boilerplate; (3) `EXPERIENCE.md` no longer contradicts entry 11's sort decisions; (4) the five files failing `prettier --check` are formatted; (5) `styles.scss` uses `@use` instead of the deprecated Sass `@import`; (6) `HealthController`'s class comment no longer calls it the scaffold's tracer bullet. Re-parked, each with its reason:
  - (7) `AddRemarkRequest`/`AddOfferRequest` are unvalidated at the API boundary; only `CreateTenderRequest` is (PR #13). Not fixed: validating them is new behavior; a candidate for entry 9's real story.
  - (8) `TenderService` has no `@Transactional` and relies on `open-in-view` (entry 4 review). Not fixed: transaction boundaries are a behavior change; guarded today by `TenderServicePersistenceTest`.
  - (9) The frontend `AGENTS.md` is stale after entry 11 and PR #13: it points to a backend pitfall that no longer exists and says nothing of global styles or `table-sort.ts`. Not fixed: the block is regenerated by `bmad-project-context`, not hand-edited.
  - (10) Entry 11's forms (add remark/offer, error placement, in-flight guard) and the mobile breakpoint were never exercised in a real browser; keyboard sorting was checked once by hand. Not fixed: entry 9 starts the app and inspects the UI anyway.

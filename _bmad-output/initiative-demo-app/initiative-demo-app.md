---
tracker_id: ""
key: ""
type: initiative
title: "Freight tender management demo app"
parent: none
covers: [D1, D2, D3, D4]
after: []
assignee: ""
risk: medium
estimate: ""
estimate_basis: ""
---

# Freight tender management demo app

## Description

light-factory (`initiative-light-factory`) has proven its Success signal against its own toy stories, but never against a realistic, non-trivial codebase. This initiative builds a demo application — Spring Boot backend, Angular frontend, modeling freight-transport tender management — whose purpose is twofold: give the pipeline a harder, more realistic target to refine against, and give the team something presentable to demo software-factory/light-factory's real implementation work on.

## Outcome

A realistic full-stack application exists, independently buildable and testable, that light-factory can be run against for real — proving the pipeline against something closer to production code than its own fixture stories, and giving stakeholders a demo they can follow without reading the pipeline's internals.

## Requirements

- D1: A minimal but realistic full-stack application — Spring Boot backend, Angular frontend — exists in its own top-level directory (`freight-tenders/`) of the light-factory repo, buildable and testable with standard tooling (Maven/Gradle + npm/ng), independent of light-factory.
- D2: The application models freight-transport tender management — tenders for a contract to transport freight from A to B, each open or closed, carrying free-text remarks and concrete supplier offers — supporting an overview of open/closed tenders, creating a new tender, and viewing an existing tender to add remarks and offers. Backed by a real test suite over at least one non-trivial business rule (e.g. offers/remarks can only be added to an open tender).
- D3: light-factory's pipeline, already live in this repo, is pointed at the demo app through its per-repo checks config (after `initiative-light-factory`'s `epic-pipeline-hardening` entry 1 is built — see Notes), so its checks run the app's own build, test, and lint, and has run at least one real, non-trivial story against the app end to end.
- D4: The repo and at least one completed story are presentable as a demo to a semi-technical audience without extra prep (clear README, a walkthrough of what the pipeline did).

## Done when

1. The demo app exists under `freight-tenders/` in the light-factory repo, builds and passes its own test/lint checks locally and in CI, independent of light-factory.
2. light-factory has run at least once against the demo app end to end (both gates exercised) on a real, non-trivial story — proving the pipeline against something harder than its own fixture stories.
3. The repo and that completed story are presentable as a demo without extra prep.

## Boundaries

The demo app's own code under `freight-tenders/`, its CI, and the checks config that points light-factory's pipeline at it. Not changes to light-factory's own pipeline logic (that's `initiative-light-factory`'s own open-issues epic), not production deployment of the demo app itself, not a second AI-provider/runtime.

## References

- sibling — _bmad-output/initiative-light-factory/initiative-light-factory.md (owns the pipeline and its checks-config mechanism; D3 waits on `epic-pipeline-hardening` entry 1)

## Notes

- Decision: housed as its own initiative, separate from `initiative-light-factory`, since that initiative's Boundaries explicitly exclude "any application it is later used to build" (user's call, 2026-10-10).
- Superseded 2026-10-11 (see the last notes): D3's blueprint copy sequences after `initiative-light-factory`'s `epic-pipeline-open-issues` (epic 2) is built, not after epic 1 alone — so this repo inherits the fixed blueprint (real `security` check, AD-15 supersession-closing, reject-closes-PR) rather than a version with four known gaps baked in. `initiative-light-factory`'s `epic-pipeline-open-issues.md` names this initiative as a downstream consumer for the same reason (2026-10-10).
- Decision: "production delivery" for this initiative's Done when means the app builds/tests/CI-passes and light-factory runs a real story against it end to end — not shipping the app to production users, which Boundaries explicitly excludes. The demo app's job is to be a harness/target, not a shipped product (2026-10-10).
- Decision: domain is freight-transport tender management (user's call, 2026-10-10) — use cases: overview of open/closed tenders, create a new tender, view an existing tender and add remarks/supplier offers to it.
- Decision: D3 (light-factory wiring + first real run) stays inside this one epic as closing entries, not a second epic — mirrors `epic-light-factory-pipeline`'s own pattern (user's call, 2026-10-10).
- Decision (2026-10-11): the demo app lives inside the light-factory repo under `freight-tenders/`, not in a repo of its own (user's call). Nothing is copied: the pipeline, its Environments, and its secrets already exist here. D1, D3, Done when, and Boundaries were reworded to match.
- Decision (2026-10-11): the directory is named `freight-tenders/`, after the app's business area rather than its role as a demo (user's call).
- Decision (2026-10-11): D3 now waits on `initiative-light-factory`'s `epic-pipeline-hardening` entry 1 (per-repo checks config) — today the checks are hard-coded to `factory/`'s Python code and would pass without building the app.
- Decision (2026-10-11): the pipeline this app is checked by has three former gaps closed, not four — `security` is a permanent `"skipped"` placeholder in the light-factory repo (user's call). The demo must not present a security check as real unless the app configures one.
- Decision (2026-10-11): this initiative takes over the pipeline's first live fix-loop engagement (`initiative-light-factory` Done-when 3, CAP-7) as `epic-demo-app` entry 10, including stronger instructions for the review agent (user's call). It is the one place this initiative changes pipeline logic.
- Decision (2026-10-11): the fix-loop proof this initiative had taken over was delivered on the pipeline itself (run `38150142797` (`stories/one-input-path-per-story-slug.md`, PR #12, merged as `c60279b`)). `epic-demo-app` entry 10 stays, narrowed to extending the review agent's instructions (user's call).

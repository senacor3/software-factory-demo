---
id: 9
type: story
title: "Closing end-to-end suite"
parent: epic-demo-app
covers: [D3, D4]
after: [8]
hitl: true
risk: medium
---

# Closing end-to-end suite

## Description

Dispatches a real, non-trivial story through light-factory against this repo end to end (both gates exercised), and polishes `freight-tenders/`'s README and walkthrough (in English, like the rest of the docs -- the German UI is the app's, not the repo's documentation) so the repo and that run are presentable as a demo.

## Acceptance Criteria

Verify: A real story run completes to merge through this repo's light-factory pipeline, and the README gives a semi-technical reader everything needed to follow it without extra prep.

Draft criteria, not yet reviewed with the user:

1. Given a story file under `stories/` that asks for a non-trivial change to the demo app (it touches a business rule or spans backend and frontend), when it is dispatched, then the run reaches merge on `main`.
2. Given that run, when it reaches `plan-approval` and `evidence-approval`, then each gate pauses and a person approves it.
3. Given that run, when the `checks` job runs, then the demo app's build, test, and lint commands from entry 7 run and pass.
4. Given the merged change, when the app is started, then the story's behavior is visible in the German UI.
5. `freight-tenders/`'s README, in English, says what the app is, how to build and run it, and walks through the run: the story, the plan, both gate decisions, the evidence summary, and the merged change, each with a link.
6. The walkthrough says that `security` is a skipped placeholder, and does not present it as a passed check.

## References

- parent — _bmad-output/initiative-demo-app/epic-demo-app/epic-demo-app.md
- sibling — _bmad-output/initiative-light-factory/epic-pipeline-hardening/epic-pipeline-hardening.md, entry 3 (the pipeline's first six-job merge) and entry 2 (clarification halt)

## Notes

- Unknown: which story to run. It is chosen when this entry starts, from what entries 2-6 leave worth adding.
- Decision: merging through the six-job pipeline is tested here on purpose (user's call, 2026-10-11). `epic-pipeline-hardening` entry 3 also merges a story; if it has not run by then, this is the pipeline's first six-job merge.
- Assumption: the criteria above were drafted from the 2026-10-11 ticket-tree review without a refinement session; `refined` stays unset until the user has reviewed them.

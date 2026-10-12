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

Dispatches a real, non-trivial story through light-factory against this repo end to end (both gates exercised), and leaves `freight-tenders/`'s README (in English, like the rest of the docs -- the German UI is the app's, not the repo's documentation) short and accurate, so the repo and that run are presentable as a demo.

## Acceptance Criteria

Verify: A real story run completes to merge through this repo's light-factory pipeline, and the README tells a semi-technical reader what the app is and how to build and run it.

Criteria, reviewed with the user on 2026-10-12:

1. Given a story file under `stories/` that asks for a non-trivial change to the demo app (it touches a business rule or spans backend and frontend), when it is dispatched, then the run reaches merge on `main`.
2. Given that run, when it reaches `plan-approval` and `evidence-approval`, then each gate pauses and a person approves it.
3. Given that run, when the `checks` job runs, then the demo app's build, test, and lint commands from entry 7 run and pass; passing after a checks-fix-loop cycle counts.
4. Given the merged change, when the app is started, then the story's behavior is visible in the German UI -- checked in a browser, together with the browser check of entry 11's forms and narrow layout that entry 8 re-parked here.
5. `freight-tenders/`'s README, in English, says what the app is, lists its endpoints and pages, and gives the commands to build, test, lint, and run it. It carries no walkthrough of the run.
6. A run that halts or fails before merge does not satisfy this story: it is reported, and the user decides whether to fix and re-dispatch.

## References

- parent — _bmad-output/initiative-demo-app/epic-demo-app/epic-demo-app.md
- sibling — _bmad-output/initiative-light-factory/epic-pipeline-hardening/epic-pipeline-hardening.md, entry 3 (the pipeline's first six-job merge) and entry 2 (clarification halt)

## Notes

- Decision (2026-10-12): the story run is `stories/close-tender-from-detail-page.md` (user's call). It is frontend-only; making the open/closed rule usable in the UI is accepted as meeting criterion 1.
- Decision: merging through the six-job pipeline is tested here on purpose (user's call, 2026-10-11). `epic-pipeline-hardening` entry 3 also merges a story; if it has not run by then, this is the pipeline's first six-job merge.
- Decision (2026-10-12): criteria reviewed with the user before dispatch, then changed after the run (user's call): the README walkthrough of the run, and with it the requirement that the walkthrough name `security` as a skipped placeholder, were dropped -- the README stays a short description, endpoint and page tables, and commands. The run's own record is PR #15 and `.factory/close-tender-from-detail-page/run-38295852809/`.

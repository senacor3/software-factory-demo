---
id: 7
type: story
title: "Point light-factory at the demo app"
parent: epic-demo-app
covers: [D3]
after: [1]
hitl: true
risk: medium
---

# Point light-factory at the demo app

## Description

Adds the demo app's build, test, and lint commands to the repo's checks config (and any runner toolchain setup they need), so a pipeline run on a story touching `freight-tenders/` checks the app itself -- the pipeline, its Environments, and its secrets already exist in this repo, so nothing is copied; needs only entry 1's scaffold and touches none of entries 2-6's src/ files, so it can build alongside them.

## Acceptance Criteria

Verify: A trivial story touching `freight-tenders/` pauses at plan-approval, and after approval its evidence/checks/ records show the app's backend and frontend build, test, and lint commands ran and passed.

Draft criteria, not yet reviewed with the user:

1. Given the checks config from `epic-pipeline-hardening` entry 1, when this story is done, then the config names the demo app's backend build, test, and lint commands and its frontend build, test, and lint commands.
2. Given a dispatched story that changes a file under `freight-tenders/`, when the `checks` job runs, then each configured command runs as a direct pipeline step with zero agent turns, and its result is recorded under `evidence/checks/`.
3. Given a demo-app story whose change breaks a backend or frontend test, when the `checks` job runs, then that check records `fail` and the job fails.
4. Given the same dispatch, when `analysis` finishes, then the run pauses at `plan-approval` until a person approves it.
5. Given a story that touches only `factory/`, when it runs, then the pipeline's own Python checks still run as they do today.
6. `security` records `skipped` unless the config names a command for it; nothing reports it as passed.

## References

- parent — _bmad-output/initiative-demo-app/epic-demo-app/epic-demo-app.md
- sibling — _bmad-output/initiative-light-factory/epic-pipeline-hardening/epic-pipeline-hardening.md, entry 1 (the checks config this story fills in)
- code — factory/scripts/run_checks.py, the commands hard-coded today
- code — .github/workflows/light-factory.yml, the `checks` job

## Notes

- Unknown: Waits on initiative-light-factory's epic-pipeline-hardening entry 1 (the per-repo checks config) -- a cross-initiative dependency no `after` can express; the config's shape, and whether factory/'s own checks still run on a demo-app story, come from there. Criterion 5 assumes they do.
- Unknown: whether installing a JDK and Node on the runner is expressed in the checks config or needs a workflow edit. A workflow edit is pipeline logic, outside this epic's Boundaries; if it is needed, it belongs to `epic-pipeline-hardening` entry 1.
- Decision: nothing is copied and no Environment or secret is created — the demo app lives in this repo, where both gates are already protected (user's call, 2026-10-11).
- Assumption: the criteria above were drafted from the 2026-10-11 ticket-tree review without a refinement session; `refined` stays unset until the user has reviewed them.

---
tracker_id: ""
key: ""
type: epic
title: "Pipeline status dashboard"
parent: initiative-light-factory
covers: [CAP-10]
after: ["epic-orchestrator-gates"]
assignee: ""
risk: medium
estimate: ""
estimate_basis: "envelope"
---

# Pipeline status dashboard

## Description

`epic-orchestrator-gates` makes both gates work entirely through PR comments. This epic gives the requesting developer a nicer front door onto the same mechanism: a React SPA, hosted on S3, that shows a story's live pipeline state across all stages and lets the developer act on either gate from one place — the dashboard posts the same PR comment a developer could post by hand, with their real GitHub identity attributed to it.

## Outcome

The requesting developer can see and act on any story's pipeline state from one dashboard instead of finding the right PR comment thread — CAP-10, demonstrated live the same way the orchestrator epic demonstrates its own gates.

## Requirements

[Completed at this epic's inception — see `epic-orchestrator-gates`'s Requirements for the pattern. Maps to CAP-10 alone.]

## Done when

1. The dashboard shows the live pipeline stage/status for a story the developer has access to, sourced from the orchestrator's own state.
2. A gate action (`/approve`, `/rework`, `/reject`) taken from the dashboard produces the identical PR comment and orchestrator-side effect as posting it directly, attributed to the developer's real GitHub identity.
3. A developer who has never opened the dashboard can still exercise both gates by commenting directly — the dashboard adds nothing the orchestrator doesn't already do without it.

## Boundaries

The React SPA (`ui/` namespace), its GitHub OAuth login, and its S3 hosting. Not the orchestrator itself, not either gate's underlying mechanism — both already work without this epic (`epic-orchestrator-gates`).

## References

- parent — _bmad-output/initiative-light-factory/initiative-light-factory.md, Done when
- spec — _bmad-output/initiative-light-factory/spec-light-factory/spec-light-factory.md, Capability CAP-10
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-18, AD-21, AD-23
- sibling — _bmad-output/initiative-light-factory/epic-orchestrator-gates/epic-orchestrator-gates.md, the prerequisite orchestrator epic

## Notes

- Decision (2026-11-03): split from `epic-orchestrator-gates` because this epic is additive — see that epic's Notes.
- Waits on epic-orchestrator-gates because: the orchestrator's API and GitHub App credential boundary (AD-18) must exist before the UI has anything to call.

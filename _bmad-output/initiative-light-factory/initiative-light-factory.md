---
tracker_id: ""
key: ""
type: initiative
title: "light-factory"
parent: none
covers: [CAP-1, CAP-2, CAP-3, CAP-4, CAP-5, CAP-6, CAP-7, CAP-8, CAP-9]
after: []
assignee: ""
risk: medium
estimate: ""
estimate_basis: ""
---

# light-factory

## Description

AI coding agents now generate more code than a developer can responsibly review line by line. light-factory is a gated pipeline that proves code-level quality mechanically — build, tests, lint, security, and an independent agent review — so the requesting developer's judgment is spent only where a machine can't substitute: task breakdown, design soundness, and whether the result satisfies the acceptance criteria. The spec owns the capabilities, constraints, and non-goals; this initiative delivers them as a PoC blueprint.

## Outcome

The requesting developer trusts a green pipeline enough to not re-read the diff by default, opening the full PR/diff only when something looks off — the spec's Success signal, demonstrated by a real story run completing end-to-end to merge with both gates exercised.

## Done when

1. A real story run completes end-to-end to merge with both the `plan-approval` and `evidence-approval` gates exercised.
2. Mechanical checks (build/test/lint/security) run as direct pipeline steps with zero agent turns spent on them.
3. The clarification loop and the fix loop each demonstrably stay within their caps (2 rounds, 2 cycles) on a run that exercises them.
4. The requesting developer approves `evidence-approval` from the gate summary alone in the common case, without needing to open the full diff.
5. A re-triggered run of a rejected or capped-out story supersedes its predecessor's PR cleanly (no zombie approval, no colliding state).

## Boundaries

The pipeline itself — not any application it is later used to build. Out of scope per the spec's non-goals: staging deployment/production rollout automation, swappable AI providers/models, alternative trigger mechanisms (v1 is manual-trigger-only), multi-role approval workflows, zero-manual-code-edits enforcement, ticket-system/chat integrations, migration to a dedicated orchestrating repo, Temporal/Camunda. One epic owns the whole pipeline — see Notes.

## References

- spec — _bmad-output/initiative-light-factory/spec-light-factory/spec-light-factory.md, section Capabilities
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md (companion, AD-1..AD-15)
- brief — _bmad-output/initiative-light-factory/brief-light-factory/brief-light-factory.md, for history only

## Notes

- Decision: CAP-1..CAP-9 form one linear, tightly coupled loop (intake → analysis → plan-approval → implementation → checks → review → fix-loop → evidence-approval → merge) with a single owner; this is one epic, not several (2026-10-01).
- Decision: ticketing store is repo files (markdown + `tickets.toml` under version control); a git repo was initialized for this workspace specifically so tickets carry history (2026-10-01).

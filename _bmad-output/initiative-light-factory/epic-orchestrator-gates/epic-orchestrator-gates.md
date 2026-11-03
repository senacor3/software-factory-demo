---
tracker_id: ""
key: ""
type: epic
title: "Orchestrator-owned gates"
parent: initiative-light-factory
covers: [CAP-3, CAP-8, CAP-9, CAP-11]
after: ["epic-pipeline-hardening"]
assignee: ""
risk: high
estimate: ""
estimate_basis: "envelope"
---

# Orchestrator-owned gates

## Description

GitHub's required-reviewers-on-environments gate — the mechanism `plan-approval` and `evidence-approval` have used since epic 1 — is restricted to GitHub Enterprise or public repos. That breaks AD-1's whole premise: light-factory is a blueprint meant to copy into any target repo, including a private, non-Enterprise one. This epic replaces both gates' mechanism: an external AWS Lambda orchestrator (Function URL, DynamoDB control-plane state, a dedicated GitHub App credential, a hand-rolled cross-stage state machine — LangGraph's own scope is unchanged) reads a PR-comment command grammar off GitHub webhooks and drives GitHub Actions, now split into three independently-dispatched workflow files, as a step-runner. It also adds a capability the old mechanism never had: bounded, agent-assisted merge-conflict resolution before the final merge.

## Outcome

A real story run completes end-to-end to merge with both gates exercised via PR comments, on a private repo with no GitHub Enterprise dependency anywhere in the mechanism — the spec's CAP-3/CAP-8/CAP-9/CAP-11, demonstrated live the same way epic 1 demonstrated the original loop.

## Requirements

- CAP-3: The requesting developer can review and confirm the proposed plan before any code is written. — This epic's part: the gate is a PR-comment command grammar (`/approve`, `/rework <feedback>`, `/reject`) the orchestrator reads off GitHub webhooks, not a GitHub Environment. (architecture AD-2, AD-13, AD-17, AD-20)
- CAP-8: The requesting developer can make an evidence-based approval decision from a concise metrics summary plus a drillable PR/diff. — This epic's part: same PR-comment mechanism as CAP-3, `/approve` triggers CAP-11's conflict-resolution-then-merge sequence. (architecture AD-2, AD-4)
- CAP-9 (reused): On developer approval, the branch can merge to the target branch. — This epic's part: merge now happens only after CAP-11's bounded resolution succeeds when a conflict exists; no change to "no agent holds merge/admin tools". (architecture AD-14, AD-19)
- CAP-11: On `evidence-approval`, a conflict between the isolated branch and the target branch can be resolved without the developer doing it by hand. — This epic's own capability: an agent scoped only to the feature branch, hard-capped at 2 attempts, inside the `merge` workflow. (architecture AD-14, AD-19)

## Done when

1. A real story run completes end-to-end to merge with both `plan-approval` and `evidence-approval` exercised entirely via PR comments (`/approve`, `/rework`, `/reject`) — no GitHub Environment involved anywhere in the run.
2. A `/rework <feedback>` on `plan-approval` demonstrably loops back to analysis with the feedback appended to the story file, distinct from CAP-2's own clarification loop.
3. A run with a real merge conflict at `evidence-approval` is resolved by the bounded conflict-resolution agent (cap 2) without human intervention, then merges.
4. A run that exhausts the conflict-resolution cap stops and surfaces the unresolved conflict to the developer, rather than merging or looping again.
5. The `plan-approval` and `evidence-approval` GitHub Environments are removed from the repo, along with the dead `close_rejected_pr.py` reject-detection path (AD-16, superseded) — no remaining dependency on either.

## Boundaries

The orchestrator (new `orchestrator/` + `infra/` namespaces per the architecture spine), the three split GitHub Actions workflow files, and `factory/`'s existing graphs/scripts where they're touched by the gate-mechanism change. Not the UI dashboard (CAP-10, `epic-pipeline-dashboard`) — that epic is additive, not a dependency of this one's Done when: every gate action here is exercised by posting a PR comment directly, same as a developer could do without ever opening a dashboard. Not CAP-1/2/4/5/6/7's own logic — unaffected, reused as-is.

## References

- parent — _bmad-output/initiative-light-factory/initiative-light-factory.md, Done when
- spec — _bmad-output/initiative-light-factory/spec-light-factory/spec-light-factory.md, Capabilities CAP-3, CAP-8, CAP-9, CAP-11
- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-2, AD-6, AD-7, AD-8, AD-13, AD-14, AD-15, AD-16, AD-17, AD-18, AD-19, AD-20
- origin — _bmad-output/initiative-demo-app/brainstorm-quality-gate-alternatives/brainstorm-quality-gate-alternatives.md
- sibling — _bmad-output/initiative-light-factory/epic-pipeline-dashboard/epic-pipeline-dashboard.md, the follow-on UI epic this one does not depend on

## Notes

- Decision (2026-11-03): initiative reopened for this epic and `epic-pipeline-dashboard` — see initiative Notes.
- Decision (2026-11-03): CAP-10 (dashboard) split into its own epic, sequenced after this one, since this epic's Done when is fully achievable via PR comments alone (user's call).
- Unknown: exact DynamoDB item schema, GitHub App permission scopes, and Terraform module layout are architecture-level (AD-17..AD-20) but not yet written as code — this epic's entries will settle the concrete shape as they build, within those ADs' constraints.
- Waits on epic-pipeline-hardening because: the six-job pipeline's checks/clarification/supersession hardening should land before the gate mechanism under it changes.
- Decision (2026-11-03): an independent validation pass (checks.dependencies) found entries 2 and 3 both touch `orchestrator/github_app.py` per the architecture's file tree — serialized as entry 3 `after = [1, 2]`, not left parallel.
- Decision (2026-11-03): entry 7 reuses entry 5's PR-comment-command-parsing helper (one owner, the earlier entry) rather than each gate parsing independently.
- Decision (2026-11-03): the plan-approval gate summary PR comment (AD-4) is explicitly owned by entry 6, posted by the Lambda orchestrator itself when the analysis workflow's completion callback arrives — not the GitHub Actions job, since AD-5 doesn't scope that job's token for it. Entries 5 and 6 are serialized (`6` after `5`) since both land in `orchestrator/handler.py`, the same reasoning as the entry 2/3 fix above (user's call, 2026-11-03).

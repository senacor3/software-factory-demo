---
id: 8
type: story
title: "Explicit job naming and QS sub-jobs"
parent: epic-pipeline-open-issues
after: [1, 2, 4, 5]
hitl: false
risk: medium
refined: true
---

# Explicit job naming and QS sub-jobs

## Description

Rename the workflow's generic "Job N: ..." job names to explicit, descriptive names with no number prefix (Analysis, Implementation, Checks, Review & fix loop, Merge -- "Close PR on gate reject" already has no prefix and is the naming precedent the others should match). Extract the Implementation job's QS steps into two new jobs that run after it: `checks` (build/test/lint/security) and `review` (independent review + bounded fix-loop, which also posts the evidence-approval summary). No behavior change: the `plan-approval` gate stays on Implementation's entry and `evidence-approval` stays on Merge's entry (AD-2) -- only ungated jobs are inserted between them. Evidence files (`evidence/checks/*.json`, `review.md`) are committed and pushed after each new job runs, extending the existing git-based state mechanism (AD-10) rather than adding a second one (e.g. workflow artifacts), so the next job's checkout always has the latest state.

## Acceptance Criteria

Verify: A trivial story run produces the same checks/review outcome as before, now spread across Implementation -> Checks -> Review & fix loop -> Merge, with each new job's evidence visible in git immediately after it completes, and the plan-approval/evidence-approval gates still landing on the same job boundaries as today.

## References

- parent — _bmad-output/initiative-light-factory/epic-pipeline-open-issues/epic-pipeline-open-issues.md
- architecture-light-factory/architecture-light-factory.md#ad-2
- architecture-light-factory/architecture-light-factory.md#ad-4
- architecture-light-factory/architecture-light-factory.md#ad-6
- architecture-light-factory/architecture-light-factory.md#ad-10
- .github/workflows/light-factory.yml

## Notes

- Decision: QS is extracted into two sub-jobs -- `checks` (build/test/lint/security) then `review` (independent review + bounded fix-loop + evidence-approval summary post) -- rather than one combined QS job or a further three-way split (user's call, refined 2026-10-11).
- Decision: evidence crosses the new job boundaries by always git-committing it, extending the existing commit+push mechanism (AD-10), rather than introducing GitHub Actions artifacts as a second state-crossing mechanism (user's call, refined 2026-10-11). Resolves the inception-time "unknown" this entry carried; still expect an AD-10 addendum documenting this during the build, mirroring how AD-14 was settled during epic 1's entry 11 and how entry 5 is expected to add its own addendum.
- `close-rejected-pr`'s trigger condition and `--gate` selection stay keyed to `implementation`/`merge` only, the two gated jobs -- a `checks`/`review` job failure is a genuine tooling or regression failure, not a gate reject, and needs no PR-closing logic. The no-op path a checks failure takes through `close-rejected-pr` today disappears, since a checks failure no longer surfaces as `needs.implementation.result == 'failure'`.

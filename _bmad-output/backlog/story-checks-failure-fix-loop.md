---
id: 1
type: story
title: "A failed mechanical check retries through a bounded agent fix loop, not a stuck PR"
parent: none
covers: []
after: []
assignee: ""
refined: true
hitl: true
risk: high
estimate: ""
---

# A failed mechanical check retries through a bounded agent fix loop, not a stuck PR

## Description

Today, when the `checks` job (build/test/lint/security) fails, the run simply
stops: the `review` job (which owns the bounded fix loop, AD-11) never starts
because it requires `checks` to succeed first, and `close-rejected-pr` does not
fire either (its condition only watches `implementation`/`merge` failures). The
PR is left open, failed, with no further automated action — a human has to
notice and intervene by hand. When this is done, a failed check instead
re-engages the implementation agent with the failure as context and retries,
bounded by the same kind of cap AD-11's existing review fix loop already uses,
before ever leaving a PR for a human to rescue manually.

## Acceptance Criteria

1. **A failed check re-engages implementation**
   **Given** a dispatched story whose `checks` job fails on `build`, `test`,
   `lint`, or `security`
   **When** that failure occurs
   **Then** the implementation agent is re-engaged with the failing check's
   output as context and the check is re-run, before the run gives up on it

2. **The retry is bounded**
   **Given** a checks failure that is still present after a fix attempt
   **When** the retry cap (matching AD-11's existing cap of 2) is reached
   **Then** the run stops retrying and reaches the same kind of terminal,
   human-actionable state a capped review fix loop already reaches today —
   never an unbounded or silent loop

3. **A fixed check lets the run continue normally**
   **Given** a checks failure that the re-engaged implementation agent
   actually resolves
   **When** the check is re-run and passes
   **Then** the run proceeds to the review stage exactly as if the original
   checks run had passed on the first attempt

4. **The existing review-stage fix loop is unaffected**
   **Given** a run whose `checks` job passes on the first attempt
   **When** the review stage later raises a finding
   **Then** the existing bounded fix loop (AD-11) behaves exactly as it does
   today — this adds a check-level retry, not a change to the review-level one

5. **A capped-out run leaves a clear trail**
   **Given** a checks failure that exhausts the retry cap
   **When** the run ends
   **Then** the state this run leaves behind names which check failed and how
   many fix attempts were made, and the PR is left open and clearly
   unresolved, never silently merged or ambiguous

## Boundaries

- Must not change: the review stage's own existing fix loop or its cap; which
  checks run or what counts as pass/fail/skip for them (CAP-5/AD-6).

## References

- architecture — _bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md, AD-6 (deterministic checks are direct pipeline steps) and AD-11 (the bounded fix loop)
- code — factory/graph/fix_loop_graph.py, the existing bounded fix loop this should mirror or extend
- code — .github/workflows/light-factory.yml, the `checks`/`review`/`close-rejected-pr` job wiring this touches
- evidence — github.com/senacor3/software-factory-demo, run 38258449451 (`stories/validate-tender-creation-input.md`, PR #13): a `lint` check failure left the PR stuck with no automated recovery; a human pushed the fix directly to the PR's branch to unstick it

## Notes

- Open question: build this by extending `fix_loop_graph.py` to also own the initial checks run (folding the `checks` job's responsibility into the existing fix-loop stage), or by adding a new, analogous bounded retry inside the `checks` job itself that hands off to `review` only once checks pass? Both satisfy the criteria above; whichever the analysis stage picks must weigh AD-6's "deterministic checks never become graph nodes" boundary against AD-11's existing cap-of-2 pattern — settle this as a dated decision before implementation starts.
- `hitl: true`: this changes core pipeline orchestration every future story depends on. Risk is `high` because a mistake here (e.g. a retry that doesn't actually bound itself, or one that silently merges a run that never truly passed checks) is not a clean revert — it would need to be caught live, on a real dispatch, the same way the formatting-slip evidence above was. A person should review the chosen design before it is built, and watch at least one live dispatch of it before trusting it unattended.

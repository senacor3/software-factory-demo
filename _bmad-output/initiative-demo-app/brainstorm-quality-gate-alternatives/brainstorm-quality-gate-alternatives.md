# Quality-gate alternative: intent doc

## Problem statement

GitHub's required-reviewers-on-environments feature (the obvious native human-gate mechanism) is restricted to GitHub Enterprise or public repos. This repo is private and non-Enterprise, so that feature is unavailable and an alternative gate mechanism is needed.

## Chosen architecture (Must-have)

- **Custom orchestrator outside GitHub Actions**: AWS Lambda owns pipeline state/transitions, fronted by a **Lambda Function URL** (not API Gateway) as the HTTPS entry point — chosen for run cost: no separate service, no per-request charge beyond the Lambda invocation itself. Auth type `NONE`, with GitHub's webhook signature verified inside the function. GitHub Actions is demoted to a step-runner, invoked per stage via `workflow_dispatch`; it no longer orchestrates the pipeline itself.
- **Custom UI dashboard**, Must-have from day one (not deferred): shows per-story pipeline state (analysis/implementation/review/etc.).
  - Its approve/rework/reject actions call the GitHub API to post a real PR comment on the human's behalf, rather than driving the orchestrator directly.
  - This keeps the existing GitHub webhook → Lambda path, and the PR comment thread, as the system's source of truth / audit trail — the UI is a front end onto that thread, not a parallel state channel.
- **Gate 1 (plan review before implementation)** — judged the more critical of the two gates — implemented as a PR-comment command grammar:
  - `/approve` → resumes to implementation
  - `/rework <feedback>` → loops back to the analysis stage, with the comment text passed in as input
  - `/reject` → cancels the story
- **Correlation key**: a unique branch name is passed to each `workflow_dispatch` call and used to correlate the later completion webhook back to the correct story/run, since `workflow_dispatch` itself returns no run ID.
- **Idempotent state-check-on-entry**: on every Lambda invocation, check the PR's actual current state before acting (don't just trust the triggering event). This makes duplicate/double invocations safe without needing to prevent them.

## Should-have

- **Gate 2 (final merge review)** via native GitHub branch-protection "require PR approval" — free on any plan, no custom infra needed.
- **Agent-driven merge-conflict resolution**: after Gate 2 approval and before the actual merge, an agent resolves merge conflicts automatically (replacing a human in that step).
- **DynamoDB-persisted per-story checkpoint state**, since the Lambda is stateless between invocations.

## Explicitly rejected / out of scope

- GitHub's required-reviewers environment-protection feature — the blocked feature this whole effort routes around.
- Splitting Gate 1 into a separate plan-only PR — rejected; story, plan, and subtasks must be reviewed together as one surface, tied to the implementation work, not split off.
- "Nature's Solutions" (biomimetic framing, e.g. cell-cycle checkpoints) — explored, produced no actionable output.

## Open question / next step

This doc captures the target architecture as decided in brainstorming only. It has not yet been run through an architecture or implementation-planning pass — that's the next step before building.

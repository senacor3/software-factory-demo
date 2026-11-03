---
id: SPEC-light-factory
companions: ['../architecture-light-factory/architecture-light-factory.md']
sources: ['../brief-light-factory/brief-light-factory.md', '../brief-light-factory/addendum.md']
---

> **Canonical contract.** This SPEC and the files in `companions:` are the complete, preservation-validated contract for what to build, test, and validate. Source documents listed in frontmatter are for traceability — consult them only if you need narrative rationale or prose color this contract intentionally omits.

# light-factory

## Why

AI coding agents now generate more code than a developer can responsibly review line by line, which produces one of two failure modes: review quietly degrades into a rubber stamp, or developers become the bottleneck trying to read everything an agent produced. light-factory is a vision to realize: a gated pipeline that proves code-level quality mechanically — build, tests, lint, security, and an independent agent review — so the requesting developer's judgment is spent only where a machine can't substitute: task breakdown, design soundness, and whether the result satisfies the acceptance criteria. This spec covers light-factory itself (the pipeline), not any application it is later used to build.

## Capabilities

- **CAP-1**
  - **intent:** The pipeline can validate that a submitted story file is complete and in scope before any agent work starts.
  - **success:** A run halts with a clear reason on an incomplete or out-of-scope story; it proceeds when intake passes.

- **CAP-2**
  - **intent:** An agent can analyze the story, propose a solution, derive subtasks and tests, run a clarification loop on open questions, and document decisions as they resolve.
  - **success:** `plan.md` and `decisions.md` exist with no unresolved open question before the `plan-approval` gate is reached. Each analysis pass that returns an open question halts that run (no live mid-job wait) and surfaces the question(s) on the PR comment; the developer answers by editing the story file and re-triggering. Capped at 2 consecutive clarification rounds per story-slug, counted from the existing supersession-PR chain (AD-15) — on the 2nd unresolved pass, the run halts with a distinct "clarification cap reached" signal instead of repeating the same halt, flagging that the story likely needs rescoping rather than another answer attempt (decided 2026-10-10, `epic-pipeline-open-issues`/2.1).

- **CAP-3**
  - **intent:** The requesting developer can review and confirm the proposed plan before any code is written.
  - **success:** No implementation commit exists until approval is explicitly recorded; the orchestrator reads the approval as a PR-comment command — `/approve` resumes to implementation, `/rework <feedback>` loops back to CAP-2's analysis with the comment text appended to the story file (distinct from CAP-2's own self-raised clarification loop), `/reject` is terminal for that run (see Constraints).

- **CAP-4**
  - **intent:** An implementation agent can write the confirmed plan's code in an isolated branch/workspace, with write access scoped to only that branch, and open a pull request against the target branch so later stages and the human reviewer have a single artifact to reference.
  - **success:** All implementation commits land on the isolated branch; a PR against the target branch exists before the `evidence-approval` gate is reached; the implementation agent's permissions cannot write outside its branch or touch another stage's state file.

- **CAP-5**
  - **intent:** Build, test, lint, and security checks can run as direct CI pipeline steps against the implementation, without agent involvement.
  - **success:** Pass/fail per check is recorded in `evidence/checks/` before review proceeds.

- **CAP-6**
  - **intent:** A review agent, distinct from the implementer and permissioned read-only, can evaluate the implementation against the plan and acceptance criteria.
  - **success:** `review.md` is produced using only read access — no write/edit tool available to this invocation — carrying findings or a clean pass.

- **CAP-7**
  - **intent:** Review findings can route back to the implementation agent for a bounded number of fix cycles, re-running only the affected checks.
  - **success:** The loop is hard-capped at 2 cycles, tracked by the orchestration graph alone; on the 2nd unresolved review it stops and routes to `evidence-approval` with `status: unresolved-after-cap` instead of looping again. Each cycle re-runs only the checks relevant to the finding(s) being fixed, not the full check suite.

- **CAP-8**
  - **intent:** The requesting developer can make an evidence-based approval decision from a concise metrics summary plus a drillable PR/diff.
  - **success:** The developer can decide from the summary alone and open the full diff/PR only on demand. The orchestrator reads the decision as the same PR-comment command grammar as CAP-3 — `/approve` triggers CAP-11's conflict-resolution-then-merge sequence, `/reject` is terminal for that run (see Constraints).

- **CAP-9**
  - **intent:** On developer approval at `evidence-approval`, the branch can merge to the target branch, completing the loop.
  - **success:** Merge happens only after explicit recorded approval and, when the branch conflicts with the target, only after CAP-11's bounded resolution succeeds (see Constraints: no agent invocation holds merge/admin tools — CAP-11's agent never merges, it only edits the branch).

- **CAP-10**
  - **intent:** The requesting developer can see a story's current pipeline stage/status across the whole run from one place, and act on either gate from there, instead of having to find and read the right PR comment thread.
  - **success:** The dashboard reflects the orchestrator's live state for any story the developer has access to. A gate action taken from the dashboard produces the same PR comment, and the same orchestrator-side effect, as posting the command directly on the PR — with the developer's real identity attributed to it.

- **CAP-11**
  - **intent:** On `evidence-approval`, if the isolated branch now conflicts with the target branch, that conflict can be resolved without the developer doing it by hand.
  - **success:** An agent scoped only to the feature branch (no access to the target branch, no merge/admin tool — same layer-1 restriction as CAP-4's implementation agent) attempts reconciliation, hard-capped at 2 attempts; only then does CAP-9's merge proceed. On cap-out, the run stops and surfaces the unresolved conflict to the developer rather than merging or looping again.

## Constraints

- Agent runtime is Claude Code for v1 only, authenticated via subscription `CLAUDE_CODE_OAUTH_TOKEN` generated by `claude setup-token` (not `ANTHROPIC_API_KEY`, not the `/install-github-app` flow). Distinct custom skills per job type (analysis, implementation, review) — not one general agent.
- An external, stateless AWS Lambda orchestrator (fronted by a Lambda Function URL, not API Gateway; a hand-rolled cross-stage state machine; DynamoDB control-plane state only, never a second copy of stage content) owns the pipeline-level state machine and both human-wait gates (`plan-approval`, `evidence-approval`), reading gate actions as a PR-comment command grammar off GitHub webhooks. GitHub Actions is demoted to a step-runner: three separate workflow files (analysis / implementation→checks→review / merge) invoked via `workflow_dispatch`, split at the two gate boundaries — no longer one chained workflow run. LangGraph (Python) is unchanged in scope: in-job agent orchestration only, within a single job's own lifetime.
- Ships as a blueprint/template copied into each target repo, not a dedicated orchestrating repo. The orchestration layer (`factory/`, `.claude/skills/`) must never reference `.github/workflows/`-specific constructs, keeping it portable to a future dedicated orchestrator.
- No hosted orchestration server (Camunda/Zeebe, Temporal) — contradicts the blueprint/minimal-footprint PoC goal. The new Lambda orchestrator doesn't change this: it's serverless/event-driven, not a stateful hosted server of that kind.
- Deterministic checks (build, test, lint, security) run as direct pipeline steps, never delegated to an agent.
- Least privilege is enforced at two independent layers for every agent invocation, neither sufficient alone: a Claude Code tool-allowlist scoped to the isolated branch and to that stage's own state-file paths, and GitHub token/branch-protection scoping that blocks direct push to main and requires PR + checks. No agent invocation ever holds merge/admin tools.
- State lives at `.factory/<story-slug>/`, one file per stage, append-only ownership — no stage mutates another stage's file. A shared frontmatter schema (`schema_version`, `story_slug`, `stage`, `status`, `updated`) is the single source of truth for both the human reviewer and the orchestration script. `story-slug` is derived once (now by the orchestrator, passed as a `workflow_dispatch` input to whichever of the three workflows is firing) and never independently re-derived. DynamoDB's orchestrator control-plane state (current stage/status, branch name, retry counters) is a distinct, separate store from this git-committed content state — never a duplicate of it.
- A `/reject` at either gate is terminal for that run — no automatic same-run loop-back. A `/rework` at `plan-approval` is not a reject: it's a bounded loop back to CAP-2's analysis, distinct from CAP-2's own self-raised clarification loop. A terminal reject means the human re-triggers the pipeline as a new run, consistent with the manual-trigger-only model.
- External dependencies are GitHub (repo, Actions, a dedicated GitHub App installation — scoped permissions, short-lived installation tokens, distinct from the per-job `GITHUB_TOKEN` GitHub Actions jobs already get automatically), Anthropic/Claude Code, and AWS (Lambda, Lambda Function URL, DynamoDB, Secrets Manager for the GitHub App private key) — no ticket system or chat integration.
- The React SPA (CAP-10's dashboard) never holds any GitHub credential. Developers authenticate into it via GitHub OAuth; the orchestrator validates that identity server-side and is the only thing that ever calls the GitHub API, using the developer's real validated GitHub username for per-developer attribution on posted gate-action PR comments rather than an anonymous bot comment.

## Non-goals

- Staging deployment and controlled production rollout automation.
- Swappable AI providers/models.
- Alternative trigger mechanisms (issue labels, PR-linked stories, watched intake folders, ticket-system webhooks) — manually triggered only.
- Multi-role approval workflows — a single requesting-developer role holds all gates.
- Zero-manual-code-edits enforcement (a post-v1 goal, not the MVP bar).
- Ticket-system and chat integrations.
- Migration to a dedicated orchestrating repo.
- Temporal/Camunda as an orchestration upgrade.

## Success signal

Demonstrable when a real story run completes end-to-end to merge with both gates exercised via the PR-comment grammar (directly or through the dashboard); mechanical checks run as pipeline steps with zero agent turns spent on them; the fix loop never exceeds 2 cycles on any run; the merge-conflict-resolution loop never exceeds 2 attempts on any run that hits one; and the requesting developer approves from the gate summary alone in the common case, opening the full PR/diff only when something looks off rather than re-reading it by default.

## Open Questions

- What operationally defines a "complete" and "in scope" story file for CAP-1 — are there required sections/fields an intake check should look for?
- Should CAP-6 also require review-agent findings/metrics to land in `evidence/review/`, not just `review.md`, to match the architecture companion's file-ownership model?
- Is there a defined failure/non-completion path for CAP-4 when the implementation agent itself gets stuck or cannot complete the plan, distinct from a post-hoc review finding?
- Does CAP-6 review proceed when a CAP-5 mechanical check (e.g. build) fails outright, or does a hard check failure short-circuit before the review agent runs?
- Under the new orchestrator model, a gate has no native platform wait-cap (unlike the old GitHub Environment's 30-day limit) — is an unactioned gate allowed to wait indefinitely, or does it need its own staleness/timeout handling?

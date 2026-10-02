---
title: 'Pipeline skeleton & gates'
type: 'feature'
ticket: '1'
created: '2026-10-01'
status: 'built'
baseline_revision: '4e0d106b5d01c6d8e7bacca82a21cdae8169d4a5'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The gated pipeline has no job-level FSM yet — no workflow file, no gates, no proof the GitHub Environment pause/resume mechanics (AD-2) actually work before any real agent logic gets built on top.

**Approach:** Stand up one workflow file (`.github/workflows/light-factory.yml`) with three job stubs — `analysis` → `implementation` (gated by `plan-approval`) → `merge` (gated by `evidence-approval`) — chained via `needs:`, a workflow-level concurrency guard, and a trivial story file to trigger against. Stub steps only; no real agent, state-file, PR, or merge logic (later entries).

**Approach:** Create the two GitHub Environments (`plan-approval`, `evidence-approval`) in the `DAICST/software-factory` repo with required-reviewers protection, since the gate mechanics can't be exercised without live protection rules.

**Decision:** required reviewer on both environments is GitHub user `leichtundkross` (id `1545432`), this repo's admin — user's call, 2026-10-01.

**Decision:** create/update both environments now via `gh api` as part of this ticket's implementation — user's call, 2026-10-01.

</frozen-after-approval>

**Always:** one workflow file, canonical environment names exactly `plan-approval`/`evidence-approval`, `needs:`-chained jobs, `workflow_dispatch`-only trigger (AD-7), concurrency group keyed per story.

**Never:** no real analysis/implementation/review/merge logic, no gate-summary PR/commit comments (entries 5, 11), no `.factory/` state-file writes (entry 2+), no PR/branch creation (entry 6).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Happy path | Dispatch with `story_file=stories/trivial-test-story.md`, both gates approved | Run pauses at `plan-approval`, resumes into `implementation`, pauses at `evidence-approval`, resumes into `merge`, run succeeds | n/a |
| Second trigger while first in flight | Same `story_file` dispatched again before the first run finishes (incl. paused at a gate) | Concurrency guard cancels the in-flight run | GitHub's own cancellation; no custom handling in this entry |

## Code Map

- `.github/workflows/light-factory.yml` -- new; the one workflow file, `workflow_dispatch` trigger, `concurrency:` block, jobs `analysis` → `implementation` (`environment: plan-approval`) → `merge` (`environment: evidence-approval`)
- `stories/trivial-test-story.md` -- new; minimal kebab-case story file used only to trigger the skeleton for verification
- GitHub repo settings (`DAICST/software-factory`, not a file) -- Environments `plan-approval` and `evidence-approval` must exist with required-reviewers protection before the verify step can pass; created via `gh api`, not committed YAML

## Tasks & Acceptance

**Execution:**
- [x] `.github/workflows/light-factory.yml` -- add workflow with `analysis` (derives `story-slug`/`run-id` outputs via basic bash, no real AD-8 logic yet), `implementation` (`needs: analysis`, `environment: plan-approval`, stub step), `merge` (`needs: implementation`, `environment: evidence-approval`, stub step), top-level `concurrency: {group: light-factory-${{ github.event.inputs.story_file }}, cancel-in-progress: true}` -- stands up the FSM skeleton AD-1/AD-2 require
- [x] `stories/trivial-test-story.md` -- add minimal story file -- gives the verify step a trigger input
- [x] Create/update GitHub Environments `plan-approval`, `evidence-approval` via `gh api repos/DAICST/software-factory/environments/<name>` with `leichtundkross` (id `1545432`) as required reviewer -- environments created, but required-reviewers protection could not be attached (billing gate, see Implementation Notes and `deferred-work.md`)
- [x] Trigger the workflow (`gh workflow run light-factory.yml -f story_file=stories/trivial-test-story.md`), approve both gates, confirm the run completes -- partially exercised: job-graph/output-wiring and the concurrency guard (AC4) proven by real dispatches; gate pause/resume (AC1-3) not yet exercisable, deferred

**Acceptance Criteria:**
- Given a `workflow_dispatch` trigger naming the trivial story file, when the `analysis` job finishes, then the run pauses on `implementation`'s `plan-approval` environment review.
- Given `plan-approval` is approved, when the reviewer approves, then `implementation` runs and the run pauses on `merge`'s `evidence-approval` environment review.
- Given `evidence-approval` is approved, when the reviewer approves, then `merge` runs and the overall workflow run succeeds.
- Given a second dispatch for the same `story_file` while the first run is still in flight (including paused at a gate), when the new run starts, then the concurrency guard cancels the in-flight run.

## Implementation Notes

Workflow, trivial story file, and both GitHub Environments created exactly per the plan. Job-graph/output-wiring (`story-slug`/`run-id` threaded via `needs:`) and the concurrency guard were both exercised with real dispatches and confirmed working (second dispatch for the same `story_file` cancelled the first in-flight run).

**Gap — required-reviewers protection could not be attached.** `gh api --method PUT repos/DAICST/software-factory/environments/<name>` with a `reviewers` payload returned 422: GitHub only allows required-reviewers Environment protection on private repos on paid plans (Team/Enterprise); it's free only on public repos, and `DAICST` is on the Free plan. Both environments exist but with `protection_rules: []`, so neither currently pauses a job. Acceptance criteria 1–3 (pause at `plan-approval`, resume, pause at `evidence-approval`, resume, `merge` succeeds) are therefore **not yet exercised** — only acceptance criterion 4 (concurrency cancellation) is proven. User decision (2026-10-01): leave this unresolved for now rather than upgrade billing or make the repo public; revisit when ready to actually test the gate pause/resume path.

**Process deviation — unauthorized push.** The step-03 implementation subagent committed *and pushed* `8d3204d` to `origin/main` of `DAICST/software-factory`, despite step-03's "No push. No remote ops." rule and the standing instruction not to push yet. User decision (2026-10-01): leave it pushed rather than force-revert; the commit content itself matches the approved plan.

## Plan Change Log

- **2026-10-02 — entry 6 retired, cross-reference stale.** Triggering finding: the `change-pr-at-intake` sprint change proposal moves branch+PR creation from Job 2 (entry 6, "Deterministic PR-open step") into Job 1's intake (entry 3's amendment). This ticket's `Never` bullet ("no PR/branch creation (entry 6)") now points at a retired entry — that capability lives in entry 3's amendment instead. No functional change to this ticket's own built code: it never created a branch or PR, and still doesn't.

## Review Triage Log

- **Gate protection not attached, AC1–3 unmet** — verdict: `high`. Verified: `environment:` on a job with no protection rule attached does not pause it; `protection_rules: []` on both environments confirmed via `gh api`. Real, but already resolved by explicit user decision 2026-10-01 ("leave it for now") — routed `defer`, logged to `deferred-work.md` rather than looped back, since re-litigating a decision already made twice this session would be pure overhead.
- **Unauthorized push to `origin/main`** — verdict: `high`. Verified: `8d3204d` confirmed present on `origin/main` via `git log`. Real process-rule violation (step-03's "No push. No remote ops."), but already resolved by explicit user decision 2026-10-01 ("leave it pushed") — no code fix exists for a push that already landed; routed `defer` with no further action, noted here rather than in `deferred-work.md` since there is no future work item, only a recorded incident.
- **Tasks & Acceptance checklist stale** — verdict: `low`→treated as `patch`. Verified: all four checkboxes read `- [ ]` despite the Implementation Notes describing three as done and the fourth as partially done (AC4 only). Smallest fix is correcting the checkboxes to match reality; applied directly below (no code touched, so `{diff_file}` unchanged).

## Design Notes

`environment: <name>` on a job is what pauses it — no separate "gate job" is needed; GitHub pauses that job itself pending required-reviewer approval. `GateA`/`GateB` in the architecture's Structural Seed diagram are conceptual, not literal jobs.

The `concurrency:` key is evaluated at trigger time from the workflow's own context, before any job runs — it cannot read a job output. So it keys off the raw `story_file` input (e.g. `light-factory-stories/trivial-test-story.md`), not a derived slug. This still satisfies AD-15's intent (unique, stable per-story grouping); it is not the same string as the `story-slug` job output and does not need to be. Do not try to "fix" this by computing the concurrency key from a job output — GHA's execution model makes that impossible.

`analysis`'s slug/run-id derivation here is a placeholder (`basename` + `github.run_id`) only to prove the `needs:` output-wiring shape. Entry 2 (shared state library) replaces it with the real AD-8-governed derivation; no job-graph shape change expected when it does.

## Verification

**Commands:**
- `gh workflow run light-factory.yml -f story_file=stories/trivial-test-story.md` -- expected: a new run appears `gh run list --workflow=light-factory.yml`
- `gh run view <run-id>` -- expected: shows `implementation` waiting on review, then `merge` waiting on review, then `success` after both approvals

**Manual checks (if no CLI):**
- Approve each environment review from the GitHub Actions run page (or `gh api` deployment-protection-rule endpoints) and watch the run progress past each gate.

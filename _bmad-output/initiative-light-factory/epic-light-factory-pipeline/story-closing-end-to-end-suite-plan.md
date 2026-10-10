---
title: 'Closing end-to-end suite'
type: 'feature'
ticket: '13'
created: '2026-10-10'
status: 'built'
baseline_revision: '68e7681f6ded0d849b9db19af641b48fa6276678'
route: 'oneshot'
route_source: 'auto'
review: ''
review_source: ''
lenses_ran: []
review_loop_iteration: 0
context: ['_bmad-output/initiative-light-factory/deferred-work.md']
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Entries 1-12 built the pipeline piece by piece, each verified by unit tests and (mostly) static review — no real story has ever gone through the whole thing end to end with real agents, real gates that actually pause, and a real merge. The spec's own Success signal is unproven live.

**Approach:** Not a code-authoring ticket — a live operational run. This plan's "implementation" is: (1) write one real, complete, in-scope story file (`stories/wire-ruff-lint.md`, already decided: real `ruff` lint tooling for `run_checks.py`'s `run_lint` placeholder) and push it to `senacor3/software-factory-demo`'s `main`; (2) dispatch `light-factory.yml` against it via `gh workflow run`; (3) watch Job 1 (analysis) run for real and reach the `plan-approval` gate; (4) **the human (not me) reviews the plan-approval PR comment and approves or rejects it** — this is the whole point of CAP-3, and an AI approving its own pipeline's gate would defeat the demonstration; (5) watch Job 2 (implementation → checks → review → bounded fix loop if needed) run for real; (6) **the human reviews the evidence-approval PR comment and approves or rejects it**; (7) watch Job 3 merge for real. My role throughout is to dispatch, monitor, report each gate's summary clearly when it's reached, and verify the final state — never to click approve myself.

## Boundaries & Constraints

**Always:** every gate approval is a real action taken by the human, in the GitHub UI or via their own `gh` command — I report what's waiting and why, never approve on their behalf. The story file is genuinely complete and in-scope (a real improvement to `run_checks.py`, not throwaway content) — chosen from `deferred-work.md`'s own already-specified `ruff`-lint item. If the fix loop engages, I observe and report it — I do not intervene in or redirect what the implementation/review agents do mid-run. If a step fails for a reason unrelated to the pipeline itself (e.g. my own `gh`/monitoring commands), I say so plainly rather than treating it as a pipeline defect.

**Never:** I never submit a deployment-review approval or rejection via `gh api`/`gh run review` or any other automated path — that action is reserved for the human throughout this run. No code changes to the pipeline itself as part of this ticket (any real pipeline bug discovered live is a `deferred-work.md` entry or a follow-up ticket, not a mid-run patch).

</frozen-after-approval>

## Implementation Notes

- **Deviation from the frozen "no code changes" boundary, both times explicitly authorized by the user in-session:**
  - Run 1 (`38070419177`) failed Job 1 outright: all 4 `factory/graph/*.py` scripts declared `requires-python = ">=3.13"` with no upper bound; a fresh GitHub-hosted runner resolved Python 3.15, and `ormsgpack` (a `langgraph` transitive dependency) has no prebuilt wheel for it, forcing a source build that fails against PyO3's 3.14 cap. Fixed by pinning `>=3.13,<3.14` on those 4 scripts (commit `43c5159`) — a pure environment-drift bug, not a story-content or pipeline-logic issue; nothing like it existed when ticket 3 live-verified on 2026-10-02.
  - Run 2 (`38070635366`) reached and passed `plan-approval` for real (first genuine human-gate pause/approve of this entire epic), then failed Job 2: the implementation agent's own plan reasonably included updating `.github/workflows/light-factory.yml`'s step comment, but GitHub's default `GITHUB_TOKEN` can never push a change to any file under `.github/workflows/`, regardless of granted permissions — verified via research, not assumed. Considered widening this with a workflow-scoped PAT; rejected (user's call) since it would let the implementation agent also rewrite the gates that constrain it, an AD-5 regression. Fixed by narrowing the story instead (commit `307586c`) to explicitly exclude workflow-file edits. The abandoned PR from this run (`#1`) was closed manually with an explanatory comment — AD-15's supersession-closing isn't built yet (`deferred-work.md`), so no automatic cleanup exists.
  - Both are real findings about the pipeline's actual behavior under live conditions — exactly what ticket 13 exists to surface. Neither was a ticket-13-authored feature; both were minimal fixes to pre-existing gaps blocking any real run.
  - Run 3 (`38072116876`) passed `plan-approval` again, implementation/build/test all succeeded for real, then failed on the real `lint` check itself — `factory/` had genuine pre-existing `ruff` violations (never cleaned up, since `lint` was a placeholder until this exact story). Deeper finding: the implementation agent has no Bash tool at all (AD-5), so it structurally cannot run `ruff` itself to discover or fix findings — its own plan said it would, but it correctly just skipped that part rather than guess. While investigating, found a second, independent bug: `run_checks.py`'s `_run_command_check` preferred `stderr` over `stdout` for the failure `detail` — for any `uv run --with X X ...` command, `uv`'s own download/install banner goes to stderr and silently masked the wrapped tool's real stdout findings. Both user-authorized (2026-10-10): fixed the detail-capture precedence (now concatenates both streams, stdout first); established a clean `ruff` baseline myself as the human operator (no agent can do this) — `ruff --fix` for 133 of 189 findings, `chmod +x` on all 12 shebang-bearing scripts (EXE001), two trivial manual unused-variable fixes, and a new `ruff.toml` scoping out `SIM117` (nested `with patch()/pytest.raises()` is this codebase's own consistent, repeated test convention, not accidental debt — flattening ~42 instances would be pure churn). Verified: 154/154 tests still pass, `ruff check factory/` now clean. The abandoned PR from this run (`#2`) was closed manually, same as before.
  - **Run 4 (`38076319765`) succeeded completely, end to end.** `plan-approval` paused for real, approved by the human; implementation/build/test/lint/security all passed; review resolved clean on the first pass (`fix_cycle: 0`, 0 findings) — the bounded fix loop never needed to engage; `evidence-approval` paused for real, approved by the human; Job 3 squash-merged (`cfd3ca0`) and deleted the branch, no agent holding merge rights anywhere in the call path. Verified post-merge on `main`: 158/158 tests pass (154 pre-existing + 4 new from the real implementation agent), `ruff check factory/` clean, `.github/workflows/light-factory.yml` genuinely untouched.
  - **All of ticket 13's verify criteria are satisfied:** a real story run completed to merge; both gates were genuinely exercised (paused and approved by the human, never by me); the clarification loop never triggered (story was complete/in-scope) and the fix loop stayed within its cap (used 0 of 2); mechanical checks ran with zero agent turns throughout (every check is a plain deterministic subprocess call).


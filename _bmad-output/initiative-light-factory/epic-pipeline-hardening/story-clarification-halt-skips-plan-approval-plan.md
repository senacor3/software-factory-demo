---
title: 'Clarification halt skips plan-approval'
type: 'bugfix'
ticket: '2'
created: '2026-10-11'
status: done
baseline_revision: '67fae9b3fef6b6b350a1e9b49b89a24eb4adb8b6'
route: 'oneshot'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** A run that halts for clarification (`awaiting-clarification` or `clarification-cap-reached`) still pauses at the `plan-approval` gate, because the `analysis` job exits 0 and `implementation` has no condition on its outcome. AD-13 says such a run ends without a gate; today approving the dangling gate would implement a plan with open questions.

**Approach:** The `analysis` job exposes the analysis status as a job output, and `implementation` runs only when that status is `ready-for-review`. The later jobs are skipped with it.

</frozen-after-approval>

## Implementation Notes

Oneshot: about 15 lines of code and workflow, plus tests — one function and one job condition.

- `factory/graph/analysis_graph.py` — `main` appends `status=<status>` to the file `GITHUB_OUTPUT` names, after a successful analysis; it writes nothing when the variable is unset (local runs) or when the run halted or failed (exit 1/3/4, which already stop the workflow).
- `.github/workflows/light-factory.yml` — the "Run analysis" step gets `id: analyze`; the `analysis` job gains a `status` output; `implementation` gets `if: needs.analysis.outputs.status == 'ready-for-review'`. The condition is an allow-list on purpose: an empty or unexpected status skips the gate rather than opening it.
- No edit to `checks`, `review`, or `merge`: each needs `implementation`, and GitHub skips a job whose needed job was skipped. `close-rejected-pr`'s own `if:` requires a `failure` result, so it stays off too. A job-level `if:` is evaluated before Environment protection, so a skipped `implementation` requests no review.
- Architecture AD-13 gains one sentence naming the mechanism.
- Verified locally with the unit tests and lint only. The workflow behavior itself — no pending `plan-approval` review on a halted run, a pause on a clean one — needs a live dispatch after a push; that is this entry's own verify check and is still open.
- Live proof, clean-story half (2026-10-11): runs `38146170332`, `38147061301`, and `38148260661` each resolved to `ready-for-review` and paused at `plan-approval` with the `status` output in place.
- Live proof, halted half: to be shown with `stories/one-input-path-per-story-slug.md`, a real story (the per-slug concurrency finding from `deferred-work.md`) that leaves one decision open on purpose and says so. Expected: `awaiting-clarification`; the PR labeled `clarification-round`, commented with the question, and closed; `Implementation`, `Checks`, `Review & fix loop`, `Merge`, and `Close PR on gate reject` all skipped; the run concludes `success` with no pending review.
- **Halted half shown live (2026-10-11), run `38149509051`** on `main` at `54e4b59`. Analysis returned the story's open decision (plus one follow-up question of its own) as `awaiting-clarification`; PR #11 was labeled `clarification-round`, commented with the questions, and closed. `Implementation`, `Checks`, `Review & fix loop`, `Merge`, and `Close PR on gate reject` were all `skipped`; the run concluded `success`; the pending-deployments API returned 0 entries, so no `plan-approval` review was requested. Both halves of this entry's verify check are now met. Not shown: the at-cap variant (`clarification-cap-reached`), which takes the same code path -- the `if:` allows only `ready-for-review`.

## Plan Change Log

## Review Triage Log

Pass 1 (2026-10-11, lens `quick`):

- medium, patched -- `test_cli_main_success_exits_0` appended `status=...` to the runner's real `GITHUB_OUTPUT` when the suite runs as the pipeline's own `test` check. Real (reproduced by the reviewer). Fixed with an autouse fixture in the module that clears the variable.
- medium, not fixable in this build -- the entry's verify and the epic's Done-when 2 need a live dispatch (a halted run with no pending review, a clean run that still pauses). Real: only the Python writer is unit-tested; the workflow half rests on GitHub's skip semantics. It needs a push, which this build does not do. The ticket stays `built`, not `done`, until that run exists.
- low, rejected for now -- `deferred-work.md`'s entry for this defect has no `resolved:` line. Left open on purpose until the live run confirms the fix; add it then.
- low, rejected -- an `OSError` while writing `GITHUB_OUTPUT` exits 1, the "halted" code, after the PR exists. Real but unlikely on a runner, it fails closed (no gate opens), and the fix is a new guard and exit code.
- low, patched -- "writes nothing on failure" was asserted for exit 1 only. The code was already correct; the test is now parametrized over exits 1, 3, and 4.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass
- `uv run --with ruff ruff check factory/` -- expected: no findings

**Manual checks (if no CLI):**
- After a push: dispatch a story with an open question and confirm the run ends after `Analysis` with the other five jobs skipped and no pending review; dispatch a clean story and confirm it pauses at `plan-approval`.

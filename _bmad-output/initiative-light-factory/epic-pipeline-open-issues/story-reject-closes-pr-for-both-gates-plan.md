---
title: 'Reject-closes-PR for both gates'
type: 'feature'
ticket: '5'
created: '2026-10-11'
status: 'built'
baseline_revision: '4b093fa9120d2f29e0c7ecc133e6d58ec8f8f221'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** When a reviewer rejects `plan-approval` or `evidence-approval`, the run ends but its PR stays open, because the gated job runs no step and its result reads `failure` exactly like an ordinary crash. AD-2 says the PR closes at reject time; today someone closes it by hand.

**Approach:** Add a final workflow job that runs only when a gated job failed, asks GitHub's workflow-run review history whether that job's Environment was rejected, and on a real reject closes this run's PR with an explanatory comment. An ordinary failure leaves the PR untouched.

## Boundaries & Constraints

**Always:** Detection and closing are a deterministic script, never an agent (AD-5). A reject is decided only from the review history of this run (`GET /repos/{owner}/{repo}/actions/runs/{run_id}/approvals`, an entry with `state: "rejected"` naming the gate's Environment) — never inferred from `needs.<job>.result` alone. The gate checked is the one guarding the job that failed: `plan-approval` for Job 2, `evidence-approval` for Job 3. The PR is this run's own (`light-factory/<story-slug>/<run-id>`, both threaded via `needs:` outputs). The closing comment names the gate, the rejecting reviewer, their review comment when they left one, and that a re-trigger starts a new run. Only the PR closes — no `--delete-branch`, no state-file write. The new job's token carries only what it needs. The detection mechanism is recorded as a new architecture decision (AD-16).

**Never:** No change to Jobs 1–3's steps, the `concurrency` block, or the existing scripts' behaviour. No close on an ordinary failure, on a cancelled run, or on a successful run. No label on the closed PR (`clarification-round` is for AD-13 only). No automatic re-trigger. No new dependency beyond `gh`. No live `gh workflow run` dispatch and no push to `main` in this ticket — verification is unit tests plus a YAML parse; the live reject proof, including the new job's run condition and token scope, is carried by entry 7 (user's call, 2026-10-11).

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Reject at `plan-approval` | Job 2 failed; history has a `rejected` entry for `plan-approval`; PR #9 open | #9 closed with a comment naming `plan-approval` and the reviewer | No error expected |
| Reject at `evidence-approval` | Job 3 failed; history has `approved` for `plan-approval` and `rejected` for `evidence-approval` | #9 closed with a comment naming `evidence-approval` | No error expected |
| Reject with a review comment | Rejected entry carries a non-empty `comment` | Closing comment quotes it | No error expected |
| Ordinary Job 2 failure | Job 2 failed; history has only `approved` for `plan-approval` | PR left open; step succeeds, reports "not a reject" | No error expected |
| Ordinary Job 3 failure | Job 3 failed (e.g. merge conflict); `evidence-approval` approved | PR left open; step succeeds | No error expected |
| Reject of the other gate only | Job 3 failed; a `rejected` entry exists only for `plan-approval` | PR left open | No error expected |
| Rejected, PR already closed | Rejected entry present; no open PR for the branch | Nothing closed; step succeeds | No error expected |
| API or `gh` failure | Review-history call, PR lookup, or close exits non-zero, or returns malformed JSON | Step fails | Single script-specific exception; exit 1 with the command and its output |

</frozen-after-approval>

## Code Map

- `.github/workflows/light-factory.yml` -- jobs `analysis` (outputs `story-slug`, `run-id`), `implementation` (`environment: plan-approval`), `merge` (`environment: evidence-approval`, `needs: [analysis, implementation]`). Each job's steps follow one shape: Checkout, `astral-sh/setup-uv`, then `uv run factory/scripts/<script>.py --story-slug … --run-id …` with `GH_TOKEN: ${{ github.token }}` where `gh` is called. Add the new job last. A rejected gated job has result `failure` and zero steps; the job after it is `skipped`; a concurrency-cancelled run gives `cancelled`.
- `factory/scripts/merge_story.py` -- closest template for the new script: own `_run` wrapper and exception class, reuses `open_implementation_pr.find_open_pr(branch)` (returns `{"branch","pr_number","pr_url"}` or `None`), argparse `main` printing JSON and returning 0/1.
- `factory/scripts/open_implementation_pr.py` -- `close_for_clarification` shows the close call: `gh pr close <n> --comment <text>`. Do not add to this module's public surface beyond reuse.
- `factory/scripts/tests/test_merge_story.py` -- test template: `subprocess.run` patched, `find_open_pr` patched, no real `gh`.
- Review-history response, confirmed against run `38076319765` on `senacor3/software-factory-demo`: a JSON array of `{"state": "approved", "comment": "", "environments": [{"name": "plan-approval", …}], "user": {"login": …}}`. `gh api repos/{owner}/{repo}/actions/runs/<id>/approvals` resolves `{owner}/{repo}` itself inside a checkout. The numeric id is `github.run_id` (the `run-id` output is `run-<id>`).
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- ADs end at AD-15 (line 125); AD-2 (51) states the reject rule; AD-5 (65) lists per-job token scopes; Structural Seed lists scripts (line ~255) and shows `reject (terminal -- see AD-2)` edges (206, 232).
- `_bmad-output/initiative-light-factory/deferred-work.md` lines 25–28 -- the source entry; gets a `resolved:` line.

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/close_rejected_pr.py` -- new script taking `--story-slug`, `--run-id`, `--github-run-id`, `--gate` (`plan-approval` | `evidence-approval`): fetch the review history, decide reject for that gate, close the open PR with the comment, print a JSON outcome saying whether it was a reject and which PR closed -- the detection and closing logic
- [x] `factory/scripts/tests/test_close_rejected_pr.py` -- one test per matrix row, plus comment content and no `--delete-branch` -- matrix coverage
- [x] `.github/workflows/light-factory.yml` -- add a final job needing all three jobs, running when the run was not cancelled and `implementation` or `merge` has result `failure`, with permissions `actions: read`, `pull-requests: write`, `contents: read`, passing the gate that matches the failed job; comment it in the file's existing style -- wires the script in
- [x] `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md` -- add AD-16 (Binds/Prevents/Rule, same form as its neighbours) for review-history-based reject detection in a trailing job; point AD-2's closing sentence at it; add the script to the Structural Seed listing and the new job's token scope to AD-5 -- the epic expects this addendum
- [x] `_bmad-output/initiative-light-factory/deferred-work.md` -- append a `resolved:` line to the reject-closes-PR entry -- the gap is closed

**Acceptance Criteria:**
- Given a run whose `plan-approval` or `evidence-approval` review was rejected, when the workflow finishes, then that run's PR is closed and carries a comment explaining the reject.
- Given a run whose gated job failed after its gate was approved, when the workflow finishes, then its PR is still open and has no reject comment.
- Given a run that succeeds or is cancelled, when the workflow finishes, then the new job does not run.
- Given the workflow file after the change, when it is parsed as YAML, then it loads and Jobs 1–3 are unchanged.

## Implementation Notes

- New job id is `close-rejected-pr`. Its condition is `!cancelled() && (needs.implementation.result == 'failure' || needs.merge.result == 'failure')`; the gate passed is `plan-approval` when `implementation` failed, otherwise `evidence-approval` (`merge` is `skipped`, never `failure`, when `implementation` failed).
- `close_rejected_pr.py` reads the review history first and looks up the PR only on a real reject, so an ordinary failure makes exactly one `gh` call. JSON outcome: `{"ok", "gate", "rejected", "closed_pr_number"}`; the "not a reject" / "nothing to close" line goes to stderr.
- A malformed review history (not JSON, not an array of objects, `environments` not a list of objects) and a malformed `gh pr list` answer both raise `RejectCloseError`. A rejected entry with no `user.login` is still a reject; the comment then says "a reviewer".
- Not run here, per the plan: no live dispatch. The run condition, the `actions: read` scope for the approvals endpoint, and the gate expression are unproven until entry 7.
- Review patches (2026-10-11): AD-15's Rule and the "Naming (PR/comment target)" conventions row now name a reject at either gate and point at AD-16; the `RunEndsA`/`RunEndsB` diagram notes say the PR is closed at reject; a `main`-level test covers "rejected, nothing to close".
- Verification ran 2026-10-11: `pytest factory/` 213 passed; `ruff check factory/` clean; the workflow parses with four jobs, `close-rejected-pr` last. No live dispatch, per the frozen block.

## Plan Change Log

## Review Triage Log

Pass 1 (quick lens, 2026-10-11) — high 0, medium 0, low 5, false 0, maybe-false 1; one finding rejected as excluded by intent.

| # | Finding | Verdict | Route | Evidence |
|---|---------|---------|-------|----------|
| 1 | `find_rejection` returns the first `rejected` entry for the gate, so on a same-run re-run a stale reject outranks a later approval and an ordinary failure closes the PR | maybe-false | reject | Needs review history to persist across attempts, which neither the reviewer nor this session confirmed against the API, plus a failed first cleanup or a hand-reopened PR. Settling it needs a live reject followed by a re-run (entry 7 can observe this). If true it would be low: a reopenable PR closed with a misleading comment on a rare path, and the fix is attempt filtering the API shape may not support. |
| 2 | Rejecting `plan-approval` on a run that hit the clarification cap closes the at-cap PR AD-13 leaves open | low | defer | Real, confirmed: `analysis_graph.main` returns 0 for both clarification outcomes, so the run pauses at `plan-approval` although AD-13 says it ends without a gate. That behaviour predates this change; here its effect is a PR closed by an explicit reviewer reject, with an accurate comment. Parked as the pre-existing gate-reached-after-clarification defect. |
| 3 | A truthy non-string `comment` raises `AttributeError` instead of `RejectCloseError` | low | reject | Real by inspection, but the API returns a string for `comment` (confirmed on run `38076319765`); the step still fails, only with a traceback. Unlikely in use and the fix is another shape guard. |
| 4 | AD-15's Rule and the conventions row still said only a `plan-approval` reject closes the PR | low | patch | Real: contradicted AD-2 and AD-16 after this change. Both reworded to either gate. The row's "cap-out closes the PR" wording predates this change and is parked separately. |
| 5 | `RunEndsA`/`RunEndsB` diagram notes said the re-trigger supersedes this run's PR | low | patch | Real: the PR is now closed at reject. Notes reworded, no new nodes. |
| 6 | No `main`-level test for "rejected, no open PR" | low | patch | Real: only the function-level case existed. Test added. |
| 7 | The job's `if:` and `--gate` expressions have no automated check | low | reject | True, and excluded by the frozen block: the live proof of the run condition is entry 7's (user's call, 2026-10-11). |

## Design Notes

A same-run-id "re-run failed jobs" keeps earlier review-history entries: after a reject, a re-run whose gate is then approved and whose job genuinely fails would still see the old `rejected` entry. The PR is already closed by then (the first attempt's cleanup closed it), so the "already closed" row applies and nothing wrong happens; no attempt-number filtering is needed.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/scripts/tests/test_close_rejected_pr.py -q` -- expected: all pass
- `uv run --with pytest pytest factory/ -q` -- expected: full suite green (188 passed before this change, plus the new tests)
- `uv run --with ruff ruff check factory/` -- expected: All checks passed!
- `uv run --with pyyaml python -c "import yaml,sys; d=yaml.safe_load(open('.github/workflows/light-factory.yml')); print(list(d['jobs']))"` -- expected: four jobs listed, the new one last

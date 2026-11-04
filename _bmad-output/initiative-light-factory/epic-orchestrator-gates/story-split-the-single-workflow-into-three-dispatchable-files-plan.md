---
title: 'Split the single workflow into three dispatchable files'
type: 'feature'
ticket: '4'
created: '2026-11-04'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: 'd0e7f9dd3af7e308da274ed3e80ddb2745d46be8'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `.github/workflows/software-factory.yml` is one monolithic workflow where every stage shares a single run and propagates `story-slug`/`run-id` via `needs:` outputs — it cannot be triggered per-stage, which the orchestrator design (AD-2) requires.

**Approach:** Split it into three `workflow_dispatch`-triggered files at the two existing gate boundaries, with no gate-mechanism change (that's entries 5/7): `analysis.yml` (unchanged derivation), `implementation-checks-review.yml` (internal `needs:` chain unchanged, now fed by `workflow_dispatch` inputs), `merge.yml`. Verified by dispatching all three in sequence against a real test story and getting the same result as today's single workflow.

## Boundaries & Constraints

**Always:** Every deterministic script's CLI flags stay byte-for-byte identical — only the YAML source of `--story-slug`/`--run-id` changes (`needs.analysis.outputs.*` -> `github.event.inputs.*`, or a first-job passthrough so the rest of a file's internal `needs:` chain keeps reading `needs.<job>.outputs.*` verbatim). `run-id` is computed exactly once, in `analysis.yml`, from its own `github.run_id` -- never re-derived from `implementation-checks-review.yml`'s or `merge.yml`'s own `github.run_id`, which would produce three different values for one logical run. Both GitHub Environments (`plan-approval` on `implementation`, `evidence-approval` on `merge`) stay exactly as-is -- just now the first/only job of their new file. `close-rejected-pr`'s mechanism is duplicated into both downstream files (one job each, each using that file's own `github.run_id`) rather than removed or left broken by the split -- AD-16 already marks this whole mechanism superseded by a later story, so duplicating it now is the minimal-change path, not new design. Each new file gets its own `concurrency:` block keyed on what it actually receives.

**Never:** No change to the two Environment names, any deterministic script's CLI contract, or the fix-loop/clarification-loop logic. No orchestrator wiring (a Lambda calling `workflow_dispatch`) -- that's entries 5/6/7; this story's own verification dispatch is manual (`gh workflow run`), per its own `hitl: false` (no human-content decision needed, but a human/agent still runs the CLI). Pushing the branch to `origin` and triggering real `workflow_dispatch` runs against the real repo is a separate, explicitly-confirmed step -- not done silently as part of planning or implementation.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| `analysis.yml` dispatched with a real `story_file` | `story_file` input | Identical to today's `analysis` job: derives slug/run-id, opens branch+PR, posts the `plan-approval` summary, exposes `story-slug`/`run-id` as job outputs | Unchanged from today |
| `implementation-checks-review.yml` dispatched with slug/run-id from the prior dispatch | `story-slug`, `run-id` inputs | `implementation`->`checks`->`checks-fix-loop`->`review` run in the same internal order as today, gated by `plan-approval` at the start | Unchanged from today |
| `merge.yml` dispatched with the same slug/run-id | `story-slug`, `run-id` inputs | `merge` runs gated by `evidence-approval`, same squash-merge as today | Unchanged from today |
| A gate reject on either downstream file | Reviewer rejects `plan-approval` or `evidence-approval` | That file's own `close-rejected-pr`-equivalent job closes the PR with a comment, using its own `github.run_id` | Same effect as today, now duplicated per file |

</frozen-after-approval>

## Code Map

- `.github/workflows/software-factory.yml` -- DELETE, replaced by the three files below
- `.github/workflows/analysis.yml` -- new: job `analysis` only (unchanged steps/derivation/outputs from today), `workflow_dispatch.inputs.story_file`, `concurrency` keyed on `story_file` (same pattern as today)
- `.github/workflows/implementation-checks-review.yml` -- new: jobs `implementation` (env `plan-approval`) -> `checks` -> `checks-fix-loop` -> `review`, internal `needs:` chain unchanged; `workflow_dispatch.inputs.story-slug`/`run-id`; `implementation`'s own `outputs:` passthrough the two inputs so every later job keeps reading `needs.implementation.outputs.*` verbatim; the now-meaningless "Assert propagation" step dropped; new `close-rejected-pr`-equivalent job (`needs: implementation`, gate `plan-approval` hardcoded, own `github.run_id`); `concurrency` keyed on `story-slug`+`run-id`
- `.github/workflows/merge.yml` -- new: job `merge` only (env `evidence-approval`), `workflow_dispatch.inputs.story-slug`/`run-id`; new `close-rejected-pr`-equivalent job (`needs: merge`, gate `evidence-approval` hardcoded, own `github.run_id`); `concurrency` keyed on `story-slug`+`run-id`
- `factory/scripts/*.py`, `factory/graph/*.py` -- unchanged (every CLI contract confirmed identical; only the YAML source of flag values changes)

## Tasks & Acceptance

**Execution:**
- [x] `.github/workflows/analysis.yml` -- carry over the `analysis` job verbatim -- preserves today's intake/analysis behavior exactly
- [x] `.github/workflows/implementation-checks-review.yml` -- carry over `implementation`/`checks`/`checks-fix-loop`/`review` with inputs-based wiring -- preserves the internal chain per the ticket's own instruction
- [x] `.github/workflows/merge.yml` -- carry over `merge` with inputs-based wiring -- preserves today's merge behavior
- [x] Add a `close-rejected-pr`-equivalent job to each of the two downstream files -- keeps reject-cleanup working per-file since cross-file `needs:` is impossible
- [x] Delete `.github/workflows/software-factory.yml` -- the split replaces it, doesn't duplicate it
- [x] Local YAML-syntax check on all three new files -- catches a malformed file before any real dispatch

**Acceptance Criteria:**
- Given a real test story, when `analysis.yml` is dispatched with `story_file`, then it behaves identically to today's `analysis` job and exposes `story-slug`/`run-id` as job outputs.
- Given the slug/run-id from that dispatch, when `implementation-checks-review.yml` is dispatched with them as inputs, then its jobs run in the same internal `needs:` order as today, gated by `plan-approval` at the start, every script invoked with byte-identical CLI flags.
- Given the same slug/run-id, when `merge.yml` is dispatched, then `merge` runs gated by `evidence-approval`, producing the same squash-merge as today.
- Given a reject at either gate, then that file's own `close-rejected-pr`-equivalent job closes the PR with a comment, using its own `github.run_id`.
- Given a full real dispatch sequence against a real test story, the end result (merged PR, `.factory/<slug>/<run-id>/` state, branch) is indistinguishable from today's single-workflow run -- the ticket's own named check, performed live, not just reviewed.

## Implementation Notes

Split `.github/workflows/software-factory.yml` into `analysis.yml`, `implementation-checks-review.yml`, and `merge.yml`; deleted the original. Every `uv run factory/...` invocation's CLI flags verified byte-identical to the original (confirmed via a diff of all `run:` blocks, normalizing only the output/input source token) -- only `needs.analysis.outputs.*` became `needs.implementation.outputs.*` (via `implementation`'s own inputs-passthrough `outputs:`) or `github.event.inputs.*` where a file's first job reads its own dispatch inputs directly.

Design choices made where the plan left the mechanism but not the exact wiring to judgment:
- The `implementation` job carries no `if:` gate on an analysis status any more (the original's `needs.analysis.outputs.status == 'ready-for-review'` check is unreachable from this file, since `analysis` now lives elsewhere) -- that decision moves to whatever dispatches this file next, consistent with the ticket's own "no orchestrator wiring" boundary.
- The now cross-file-impossible "Assert story-slug/run-id propagation matches AD-8 derivation" step was dropped from `implementation`, per the ticket's own instruction.
- Both new `close-rejected-pr`-equivalent jobs read `story-slug`/`run-id` straight from that file's own `workflow_dispatch` inputs (`github.event.inputs.*`), not via `needs.<gated-job>.outputs.*` -- deliberately, so the reject-cleanup path never depends on the gated job (`implementation`/`merge`) having run a single step to produce those outputs, which is exactly the situation on a real reject. `needs: implementation` / `needs: merge` is kept only for the `.result` gating check.
- `merge.yml`'s own `merge` job carries no `if:` gate on a review result either, for the same cross-file reason as `implementation` above.

Verified: `yaml.safe_load` on all three new files (no exceptions); `actionlint` (installed locally, not part of the repo's own toolchain) on all three with zero findings, including expression type-checking across the `needs.*.outputs.*` chain; the full `factory/graph/tests/` + `factory/scripts/tests/` suite (390 passed) after retargeting `factory/scripts/tests/test_workflow_checks_setup.py`'s `WORKFLOW` constant at `implementation-checks-review.yml` (it reads the `checks`/`checks-fix-loop` job bodies as data -- not in the ticket's own Code Map, but left pointed at the deleted file it would otherwise fail outright); `ruff check factory/` clean.

Not done, by the ticket's own explicit instruction: no push to `origin`, no real `workflow_dispatch` runs, no orchestrator wiring. That live three-file dispatch sequence against a real test story remains the ticket's own named outstanding verification step, to run only after separate, explicit confirmation.

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-04):** 1 finding rejected (out of scope by the intent itself), 1 finding routed. Verdict counts: low=1 (patch), 1 rejected.

- "AC5 (the live three-file dispatch sequence) is unmet" — **rejected, out of scope by intent.** The frozen Boundaries & Constraints block explicitly states "Pushing the branch to `origin` and triggering real `workflow_dispatch` runs ... is a separate, explicitly-confirmed step -- not done silently as part of planning or implementation." The intent itself excludes this from the current pass, not just the Code Map's shape -- correctly deferred, to be run next as its own confirmed action, not a gap in this diff.
- `AGENTS.md:15` and `freight-tenders/README.md:16` both still name the now-deleted `.github/workflows/software-factory.yml` -- **low, patch.** Verified: the diff deletes that file outright and replaces it with the three new files; neither doc line was updated, a direct unaddressed consequence of this exact diff (not excluded by the frozen intent, just missing from the Code Map's enumeration). Fix: update both lines to name the new files.

Patch applied and re-verified: `grep -n "software-factory.yml" AGENTS.md freight-tenders/README.md` returns no matches.

## Design Notes

File naming drops the `software-factory-` prefix (`analysis.yml`, not `software-factory-analysis.yml`) -- the directory already scopes it, consistent with this repo's own `light_factory/` -> `factory/` stutter-dropping precedent.

`close-rejected-pr` duplication, not removal: today's one trailing job spans jobs that will live in two separate files once split -- cross-file `needs:` is impossible, and each split file has its own `github.run_id`, so the query target for "did a reject happen in *this* run" is always available within whichever file the reject occurred in. AD-16 already marks this entire mechanism superseded by a later story's direct `/reject` webhook handling -- duplicating the existing, soon-to-be-replaced logic per file is the minimal-change path that keeps this story's own scope ("no gate-mechanism change") honest, rather than inventing a cross-file alternative that will be thrown away shortly anyway.

Concurrency keys: `analysis.yml` keeps today's `story_file`-keyed group. The two downstream files no longer receive `story_file` at all, so their groups key on `story-slug`+`run-id` instead -- the only identifiers they actually have.

The `implementation` job's outputs-passthrough (re-exposing its own `workflow_dispatch` inputs as job outputs) is chosen specifically so every later job in that file keeps reading `needs.implementation.outputs.*`, matching the ticket's own instruction that the internal `needs:` chain stays unchanged -- only the first job's *source* of those values changes, not the pattern every later job already uses.

The real live dispatch sequence (pushing this branch to `origin`, running `gh workflow run analysis.yml --ref <branch> -f story_file=...`, then the other two) is this story's actual proof and will be run as a separate, explicitly-confirmed step once the code itself is reviewed -- not bundled silently into implementation, since it pushes to the shared remote and triggers real GitHub Actions runs against the real org repo.

## Verification

**Commands:**
- `python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/analysis.yml` (repeat for the other two files) -- expected: no exception, catches YAML syntax errors before any dispatch
- `grep -c "needs.analysis.outputs\|needs.implementation.outputs" .github/workflows/implementation-checks-review.yml` and a manual diff review against today's job bodies -- expected: every script invocation's flags are byte-identical to today's, only the output/input source changed

**Manual checks (if no CLI):**
- The full live dispatch sequence (analysis -> implementation-checks-review -> merge) against a real test story, confirming the same end state as today's single-workflow run -- run only after explicit confirmation, since it pushes to `origin` and triggers real Actions runs.

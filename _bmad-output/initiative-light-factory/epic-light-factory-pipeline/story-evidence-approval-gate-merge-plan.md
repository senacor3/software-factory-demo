---
title: 'evidence-approval gate + merge'
type: 'feature'
ticket: '11'
created: '2026-10-02'
status: 'built'
baseline_revision: '8d785d5126895e68092aeed284de8e1d1d3e948c'
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

**Problem:** CAP-8 (evidence summary) and CAP-9 (merge) are unbuilt. Job 2 ends after ticket 10's fix loop with no gate-summary comment, and Job 3 is still the ticket-1 stub — `evidence-approval` pauses with nothing for the human to decide from, and approving it does nothing.

**Approach:** Add `factory/scripts/post_evidence_summary.py` (Job 2's final step, before the gate): reads `evidence/checks/*.json` (ticket 8) and `evidence/review/findings.json` + `review.md`'s `status`/`fix_cycle` (tickets 9/10), renders a concise metrics summary, posts it via `post_summary.post_comment` (the same shared AD-4 module ticket 5 used). CAP-8's "drillable diff" is satisfied for free by the PR's own Files-changed tab — the summary points to it rather than inlining the diff. Add `factory/scripts/merge_story.py` (Job 3, real steps replacing the stub): on `evidence-approval`'s approval, finds the PR and runs `gh pr merge --squash --delete-branch` (user's call, 2026-10-02) — a deterministic script, never an agent (AD-5/AD-14). A merge conflict just fails the step; auto-resolution is explicitly out of scope (the spec's own open question) — the human resolves out-of-band and re-triggers, consistent with every other terminal-failure path in this pipeline.

## Boundaries & Constraints

**Always:** the evidence summary step runs and succeeds whether `review.md`'s status is `resolved` or `unresolved-after-cap` — both are legitimate, human-decides-at-the-gate outcomes, not failures; merge strategy is `--squash --delete-branch` (user's call, 2026-10-02); merge is a plain deterministic script with no `claude` CLI invocation anywhere in this ticket — no judgment work exists here; both new scripts find the PR via `open_implementation_pr.find_open_pr` (promoted from the existing private `_find_existing_pr`, same branch-name formula every other stage already uses).

**Never:** no merge-conflict auto-resolution logic (out of scope — a conflict fails the step, human resolves + re-triggers); no change to any judgment-stage script (`analysis_graph.py`/`implementation_graph.py`/`review_graph.py`/`fix_loop_graph.py`) beyond the `find_open_pr` rename; no new agent or skill anywhere in this entry; the evidence summary never inlines the full diff text.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Evidence summary posts (review resolved) | `review.md` status `resolved` | PR comment: checks pass/fail, review resolved + fix-cycle count, pointer to the diff; step exits 0 | n/a |
| Evidence summary posts (review unresolved-after-cap) | `review.md` status `unresolved-after-cap` | PR comment includes the outstanding findings list and the capped status; step exits 0 | n/a — legitimate outcome, not a failure |
| Evidence summary posting fails | No open PR found, or `gh pr comment` fails | Raises `EvidenceSummaryError`; step exits non-zero | Distinguishable from a legitimate summary |
| Merge succeeds | Approval granted, no conflict | `gh pr merge --squash --delete-branch` succeeds; step exits 0 | n/a |
| Merge fails (conflict or other `gh` failure) | e.g. target branch moved since the PR opened | Raises `MergeError`; step exits non-zero | Human resolves out-of-band, re-triggers as a new run — not handled here |
| Merge: no open PR found | Defensive — shouldn't happen for a run that reached this gate | Raises `MergeError` | Same exception as a merge failure — both mean "could not complete the merge" |

</frozen-after-approval>

## Code Map

- `factory/scripts/open_implementation_pr.py` -- edit: rename `_find_existing_pr` -> `find_open_pr` (now public — reused by both new scripts below, same branch-name-lookup need). Its two internal call sites (`open_pr_for_story`) updated to the new name; behavior unchanged, no test currently references the old underscored name.
- `factory/scripts/post_evidence_summary.py` -- new. `EvidenceSummaryError(RuntimeError)`. `post_evidence_summary(story_slug, run_id, *, state_base=state_io.FACTORY_DIR, cwd=None) -> dict`: reads the 4 `evidence/checks/<name>.json` files (`status: "not-run"` if one is somehow missing), `review.md`'s frontmatter (`status`, `fix_cycle`) via `state_io.read_state`, and `evidence/review/findings.json`; renders a Markdown summary (checks list, review status + fix-cycle count + finding count, findings listed when present, a pointer to the PR's Files-changed tab); finds the PR via `open_implementation_pr.find_open_pr`, posts via `post_summary.post_comment`. CLI: `--story-slug`/`--run-id`.
- `factory/scripts/merge_story.py` -- new. `MergeError(RuntimeError)`. `merge_story(story_slug, run_id, *, cwd=None) -> dict`: finds the PR via `open_implementation_pr.find_open_pr`, runs `gh pr merge <number> --squash --delete-branch` via a local `_run` helper (duplicated `_run` pattern, established convention). CLI: `--story-slug`/`--run-id`.
- `.github/workflows/light-factory.yml` -- edit: Job 2 (`implementation`) gains `pull-requests: write` in `permissions:` and a new final step "Post evidence-approval summary" (`uv run factory/scripts/post_evidence_summary.py ...`, `GH_TOKEN` env) after "Run review (bounded fix loop)". Job 3 (`merge`) changes `needs: implementation` to `needs: [analysis, implementation]` (it needs `needs.analysis.outputs.story-slug`/`run-id`, not currently reachable), gains `permissions: {contents: write, pull-requests: write}`, and its steps become real: Checkout, Install uv, "Merge" (`uv run factory/scripts/merge_story.py ...`, `GH_TOKEN` env) replacing "Merge stub".
- `factory/scripts/tests/test_post_evidence_summary.py`, `factory/scripts/tests/test_merge_story.py` -- new, covering the I/O Matrix, `subprocess.run`/filesystem mocked (same pattern as the existing test files).

## Tasks & Acceptance

**Execution:**
- [ ] `factory/scripts/open_implementation_pr.py` -- rename `_find_existing_pr` to `find_open_pr`
- [ ] `factory/scripts/post_evidence_summary.py` -- add `post_evidence_summary`, `EvidenceSummaryError`, CLI
- [ ] `factory/scripts/merge_story.py` -- add `merge_story`, `MergeError`, CLI
- [ ] `.github/workflows/light-factory.yml` -- wire both into Job 2/Job 3, fix Job 3's `needs:`, add permissions
- [ ] `factory/scripts/tests/test_post_evidence_summary.py`, `factory/scripts/tests/test_merge_story.py` -- new tests per the I/O Matrix
- [ ] Run `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- all pass

**Acceptance Criteria:**
- Given a run that reaches the evidence-approval gate, when Job 2's final step runs, then the PR carries a concise summary (checks, review status/fix-cycle/findings) and a pointer to the diff, regardless of whether review ended `resolved` or `unresolved-after-cap`.
- Given the evidence-approval gate is approved, when Job 3 runs, then the PR merges via squash with the source branch deleted, with no agent invocation holding merge rights anywhere in the call path.
- Given a merge conflict, when Job 3's merge step runs, then it raises `MergeError` and fails the step rather than attempting any auto-resolution.

## Implementation Notes

## Plan Change Log

## Review Triage Log

- **Quick lens, 2026-10-02: no findings.** Verified against all three acceptance criteria, all 6 I/O Matrix rows, and the Boundaries & Constraints; confirmed the `find_open_pr` rename is complete with no remaining references to the old name; confirmed field names read from `evidence/review/findings.json` match what `review_graph.py` actually writes; confirmed the summary step runs unconditionally after the fix loop (which exits 0 for both terminal statuses, no `if: always()` needed); confirmed no judgment-stage script was touched; ran the real test suite (154 passed) and validated the workflow YAML's shape. One non-blocking note: `review_meta.get("fix_cycle", 0)` reads back as a string (frontmatter round-trips as strings, `state_io.read_state` only coerces `schema_version`), not an int — immaterial, since it's only ever f-string-interpolated into the rendered summary, never compared numerically. No loopback triggered.

## Design Notes

**Why "drillable diff" needs no new diff-rendering code:** AD-12 already opens the PR at intake, so the full diff has lived on GitHub's own PR UI (Files changed tab) since entry 3. CAP-8's "drillable... open full diff/PR only on demand" is satisfied by pointing to that existing surface, not by building a diff-rendering feature this pipeline would otherwise need to invent from scratch.

**Why `find_open_pr` is promoted to public rather than duplicated again:** unlike the `_run` subprocess helper (deliberately duplicated per-module, since each owns its own exception type), the branch→PR lookup is the exact same operation for every caller (idempotent-PR-open-check in ticket 3, now the evidence summary and the merge step) with no per-caller variation — a second near-identical private copy would just be the same logic maintained twice.

**Why merge-conflict handling is out of scope:** this mirrors the spec's own unresolved open question, and every other terminal-failure path already established in this epic (CLI tooling failures, check regressions) — fail cleanly, let the human resolve and re-trigger, rather than build speculative conflict-resolution logic nothing has asked for yet.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all pass

**Manual checks (if no CLI):**
- Inspect Job 3's `needs:`/`permissions:` and both new steps' `GH_TOKEN` env directly — no automated YAML-shape check.

---
title: 'Remove the old gate mechanism'
type: 'feature'
ticket: '10'
created: '2026-11-05'
status: 'built'
route: 'full'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: ['{project-root}/AGENTS.md']
baseline_revision: '9d54a1a918769871b0aa226fc24d6030752ea45f'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** `close_rejected_pr.py` and its trailing `close-rejected-pr` job in `implementation-checks-review.yml`/`merge.yml` are dead weight (AD-16, superseded) — every PR-level reject now goes through the orchestrator's direct `/reject` webhook handling (entries 5/7); this script/job pair can never fire a real reject anymore, only mask an ordinary crash as "not a reject." The two repo-settings GitHub Environments (`plan-approval`, `evidence-approval`) are also unused dead configuration.

**Approach:** Delete `close_rejected_pr.py`, its test file, and both `close-rejected-pr` jobs entirely (not disable — AD-16 already names this exact removal). Update both workflow files' header comments, which currently say removing this job and the Environment resource is "entry 10's scope" / "left in place until a later entry" — this is that entry. The two GitHub Environments themselves are deleted via `gh api`, as a separate, explicitly-confirmed step after the code change is built and reviewed (destructive against the live repo; not delegated to the implementation subagent).

## Boundaries & Constraints

**Always:** `close-rejected-pr` is removed as a whole job (not just its one step) from both files — nothing else `needs:` it (verified: it's a leaf job in both). No change to `implementation`'s, `checks`'s, `review`'s, or `merge`'s own logic beyond the header-comment updates naming what changed. The literal strings `plan-approval`/`evidence-approval` as PR-comment-gate *names* (AD-2's own canonical identifiers, used throughout `handler.py`/`comment_commands.py`/`AGENTS.md`/historical story files) are untouched — only the GitHub Environment *mechanism* and `close_rejected_pr.py` are being removed, not the gate concept itself. Historical story/plan files under `stories/`/`.factory/` that mention either name are untouched (audit-trail-over-cleanup, same posture as AD-12/AD-15).

**Never:** No change to `merge_story.py`, `post_evidence_summary.py`, `post_summary.py`, or any other script that legitimately names a gate by its canonical identifier. The actual `gh api` deletion of the two Environment resources is not performed by the implementation subagent — it happens after this plan's code change is reviewed and committed, as its own explicitly-confirmed action.

## I/O & Edge-Case Matrix

<!-- No meaningful I/O scenarios -- this entry removes dead code, it adds no new behavior to test. -->

</frozen-after-approval>

## Code Map

- `factory/scripts/close_rejected_pr.py` -- delete.
- `factory/scripts/tests/test_close_rejected_pr.py` -- delete (its only importer).
- `.github/workflows/implementation-checks-review.yml` -- remove the `close-rejected-pr` job (lines ~474-524, the file's last job) entirely; update the header comment block (currently: "Also carries a `close-rejected-pr`-equivalent job for this file's own gate... left in place per this entry's own boundaries -- removing it is entry 10's scope, not this one's") to state it's been removed, this entry, with `/reject`'s direct webhook handling (entries 5/7) as the sole mechanism; update the "(The repo-settings `plan-approval` Environment resource itself is left in place until a later entry removes it.)" sentence to say it has been removed (once the separate `gh api` step actually completes -- see Verification).
- `.github/workflows/merge.yml` -- same two edits, mirrored for `evidence-approval`/entry 7's wording.

## Tasks & Acceptance

**Execution:**
- [ ] Delete `factory/scripts/close_rejected_pr.py` and `factory/scripts/tests/test_close_rejected_pr.py`
- [ ] Remove the `close-rejected-pr` job from `implementation-checks-review.yml` and `merge.yml`
- [ ] Update both files' header comments to reflect the removal

**Acceptance Criteria:**
- Given the repo, when searched for `close_rejected_pr` or `close-rejected-pr`, then zero matches remain outside historical `_bmad-output`/`stories`/`.factory` records.
- Given either workflow file, when inspected, then it has no `close-rejected-pr` job and no step invoking `close_rejected_pr.py`.
- Given the full `factory/` test suite, when run, then it passes with the same count minus `test_close_rejected_pr.py`'s own tests.

## Implementation Notes

## Plan Change Log

## Review Triage Log

**Pass 1 (quick lens, 2026-11-05):** 1 finding, resolved by sequencing (no code patch).

- Both workflow files' updated header comments assert the GitHub Environment resource "has been removed" as a completed fact, but the plan's own Boundaries/Design Notes defer that `gh api -X DELETE` call to a separate, explicitly-confirmed step *after* this code change is reviewed and committed -- at the point this diff was reviewed, the claim was not yet true. **Verified true as a point-in-time observation.** Resolution: not a code patch -- the live `gh api -X DELETE` calls run (with separate explicit confirmation) *before* this commit lands, so the statement is accurate at the moment it's actually committed. No wording change needed once sequenced this way.

## Design Notes

Deleting rather than disabling matches AD-16's own Rule text verbatim: "a `/reject` PR comment is now read directly off the GitHub webhook by the orchestrator... and acted on immediately: no trailing job, no polling, no review-history lookup" -- the superseded mechanism was never meant to linger as dead code.

The GitHub Environment resources themselves are deleted out-of-band from this plan's own implementation step, via a separate, explicitly-confirmed `gh api -X DELETE` call against the live repo once this code change is reviewed and committed -- consistent with this epic's own established pattern of gating any live, destructive, or hard-to-reverse action against the real repo behind its own explicit confirmation, separate from the code-review/commit cycle.

## Verification

**Commands:**
- `grep -rn "close_rejected_pr\|close-rejected-pr" .github .claude factory orchestrator` -- expected: no matches
- `uv run --with pytest --with pyyaml pytest factory/graph/tests/ factory/scripts/tests/` -- expected: all remaining tests pass
- `uv run --with pyyaml python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/implementation-checks-review.yml` (repeat for `merge.yml`) -- expected: no exception
- `uv run --with ruff ruff check factory/` -- expected: clean

**Manual checks (if no CLI):**
- Deleting the `plan-approval`/`evidence-approval` GitHub Environments from the live repo (`gh api -X DELETE repos/senacor3/software-factory-demo/environments/<name>`) runs only after this plan's code change is committed and only with separate, explicit confirmation -- not part of this plan's automated verification, and not performed by the implementation subagent.

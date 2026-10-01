---
title: 'Shared state library'
type: 'feature'
ticket: '2'
created: '2026-10-01'
status: 'built'
baseline_revision: '2de7b5941e7c987224b876f9fd2e3d13879b7e34'
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

**Problem:** Every later stage (analysis, checks, review, fix-loop) needs one shared way to read/write `.factory/<story-slug>/<run-id>/` state files with AD-10's exact frontmatter schema — without it, each entry would invent its own, and AD-10's "no stage invents its own naming" rule breaks immediately. The workflow's own slug/run-id derivation (entry 1) is also still a bash placeholder, not the validated AD-8 logic.

**Approach:** Add `factory/scripts/state_io.py` — a stdlib-only Python module + CLI, mirroring `_bmad/scripts/memlog.py`'s pattern (PEP 723 header, plain `key: value` frontmatter, atomic write) — providing slug/run-id derivation, the `.factory/` directory layout, and a generic frontmatter read/write pair enforcing AD-10's schema. Swap the `analysis` job's placeholder bash derivation for a call into it, and add a real assertion in `implementation` that it received the same slug/run-id `analysis` derived.

</frozen-after-approval>

**Always:** stdlib only (no new runtime dependency), AD-10's five frontmatter fields verbatim (`schema_version`, `story_slug`, `stage`, `status`, `updated`), status validated against AD-10's per-stage enum, atomic writes (temp + fsync + rename).

**Never:** no plan.md/decisions.md/review.md content yet (entries 3, 9 write those), no evidence-file format invented (entries 8, 9 decide that), no new job added to the workflow.

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| Round-trip | `write_state(path, story_slug="foo-bar", stage="analysis", status="drafted", body="...")` then `read_state(path)` | Returned `meta` has all five AD-10 fields, `story_slug`/`stage`/`status` match, body matches | n/a |
| Invalid status for stage | `stage="review"`, `status="drafted"` (an analysis-only status) | Raises `ValueError` before any write | Caller (future stage code) must catch and fail loudly |
| Non-kebab-case story file | `derive_story_slug("stories/Not_Kebab.md")` | Raises `ValueError` | CLI `derive` prints to stderr, exits 2 |
| Propagation | Real workflow dispatch | `implementation` job's assertion step confirms `needs.analysis.outputs.story-slug`/`run-id` match what `analysis` derived | Step fails loudly (`exit 1`) on mismatch |

## Code Map

- `_bmad/scripts/memlog.py` -- precedent to mirror: PEP 723 inline deps, hand-rolled `key: value` frontmatter `split`/`render`, `write_atomic` (temp+fsync+rename), CLI via `argparse`, JSON ack to stdout. No existing code to reuse directly (different schema), but the pattern is binding.
- `_bmad/scripts/tests/test_memlog.py` -- precedent for test shape: `sys.path.insert` + direct `import`, `uv run --with pytest pytest <path>`, `tmp_path` fixture.
- `factory/scripts/state_io.py` -- new; slug/run-id derivation, `.factory/` layout, frontmatter read/write enforcing AD-10's schema.
- `factory/scripts/tests/test_state_io.py` -- new; round-trip, validation, and derivation tests.
- `.github/workflows/light-factory.yml` -- edit; add `astral-sh/setup-uv@v10.2.0` to `analysis` and `implementation`, replace `analysis`'s bash slug/run-id derivation with a call into `state_io.py derive`, add an assertion step to `implementation`.

## Tasks & Acceptance

**Execution:**
- [x] `factory/scripts/state_io.py` -- `derive_story_slug`, `derive_run_id`, `state_dir`, `ensure_layout`, `write_state`/`read_state` (AD-10 schema + per-stage status enum), plus a `derive`/`write`/`read` CLI mirroring `memlog.py` -- the shared library every later entry depends on
- [x] `factory/scripts/tests/test_state_io.py` -- round-trip, invalid-status, non-kebab-case cases from the I/O matrix -- proves the library before anything builds on it
- [x] `.github/workflows/light-factory.yml` -- add `astral-sh/setup-uv@v10.2.0` to `analysis`/`implementation`; `analysis`'s derive step becomes `uv run factory/scripts/state_io.py derive --story-file ... --github-run-id ... >> "$GITHUB_OUTPUT"`; `implementation` gets an assertion step comparing its received `needs.analysis.outputs.*` against an independently-recomputed expected slug/run-id -- real AD-8 derivation, and a concrete pass/fail test of the `needs:` propagation
- [x] Run `uv run --with pytest pytest factory/scripts/tests/test_state_io.py` -- 40/40 passed; 43/43 after review fixes (below). `gh workflow run light-factory.yml -f story_file=stories/trivial-test-story.md` run live after committing+pushing `5ed6f77` (user-authorized): run `36908896413`, `implementation`'s assertion step logged `PASS: propagation verified -- story-slug=trivial-test-story run-id=run-36908896413`

**Acceptance Criteria:**
- Given a state file written via `write_state` with valid stage/status, when read back via `read_state`, then all five AD-10 frontmatter fields and the body round-trip exactly.
- Given `write_state` called with a status not in that stage's AD-10 enum, when called, then it raises before writing anything.
- Given a story file name that isn't kebab-case, when `derive_story_slug` runs, then it raises `ValueError` and the CLI exits non-zero.
- Given a real workflow dispatch, when `implementation` runs, then its assertion step confirms the slug/run-id it received via `needs:` match what `analysis` derived.

## Implementation Notes

Built exactly per plan: `factory/scripts/state_io.py` (stdlib-only, PEP 723 header, mirrors `memlog.py`'s hand-rolled `key: value` frontmatter split/render + atomic temp-fsync-rename write) provides `derive_story_slug`, `derive_run_id`, `state_dir`, `ensure_layout`, `write_state`/`read_state`, and a `derive`/`write`/`read` CLI. `factory/scripts/tests/test_state_io.py` (40 tests) covers the I/O matrix plus extra edge cases (empty slug, unknown stage, double/leading/trailing hyphen, idempotent `ensure_layout`, CLI exit codes, `---` inside a body). `.github/workflows/light-factory.yml`: added `actions/checkout@v4` (later bumped to `v7`, see below) + `astral-sh/setup-uv@v10.2.0` to `analysis` and `implementation` (checkout was missing entirely before -- needed so the runner has `factory/scripts/state_io.py` to invoke); `analysis`'s derive step now shells out to `state_io.py derive`; `implementation` gained an "Assert story-slug/run-id propagation" step that independently re-derives the expected slug/run-id (same inputs, including `github.run_id`, which is constant across every job in one run) and fails (`exit 1`) on any mismatch against `needs.analysis.outputs.*`.

`uv run --with pytest pytest factory/scripts/tests/test_state_io.py` ran clean (40/40). The CLI was also smoke-tested directly (`uv run factory/scripts/state_io.py derive --story-file stories/trivial-test-story.md --github-run-id 123456` → `story-slug=trivial-test-story` / `run-id=run-123456`).

The implementer deliberately left the live `gh workflow run` dispatch unexercised rather than commit/push without explicit instruction (entry 1's Review Triage Log had flagged an unauthorized push as a real process violation on this same ticket chain). At review time the orchestrator asked the user explicitly; user authorized commit+push (2026-10-01). Committed as `5ed6f77`, pushed to `origin/main`, then dispatched live: run `36908896413` — `implementation`'s "Assert story-slug/run-id propagation" step logged `PASS: propagation verified -- story-slug=trivial-test-story run-id=run-36908896413`. All four acceptance criteria are now genuinely verified, including the live propagation check.

**Out-of-band fix — `actions/checkout` bumped v4 → v7.** User asked directly to ensure latest plugin versions. Verified v7.0.1 is current (v7 is a maintained moving major tag, confirmed via the GitHub API against the same commit as v7.0.1); `astral-sh/setup-uv@v10.2.0` was already current. Committed `5481a70`, pushed, re-dispatched (`36909313132`) — all three jobs passed, and the `v4`-era "Node.js 20 is deprecated" annotation is gone.

## Plan Change Log

## Review Triage Log

- **`state_io.py`'s `requires-python = ">=3.11"` contradicted the architecture's Stack decision** — verdict: `high`. Verified: Stack table pins `Python >=3.13` and `factory/scripts/state_io.py` is explicitly inside the namespace that table governs; the script instead copied `_bmad/scripts/memlog.py`'s floor verbatim, a different tool at a different altitude. Routed `patch`, applied directly: bumped the PEP 723 header to `>=3.13`.
- **Implementation job's propagation-assertion step independently re-derives the slug/run-id, which AD-8's rule text forbids absolutely** — verdict: `medium`. Verified: AD-8's Rule and the Consistency Conventions table both say "never independently re-derived" with no carve-out for verification; the new step does call `state_io.py derive` a second time. But the recomputed value is discarded immediately after comparison and never consumed as the value-of-record (the `Implementation stub` step still uses only `needs.analysis.outputs.*`), so the collision risk the rule exists to prevent — two jobs acting on different slugs — doesn't arise; the reviewer's own analysis confirmed this. No viable alternative design proves propagation without an independent recomputation to compare against (the raw inputs it re-derives from are already available in every job via workflow inputs + `github.run_id`, so this is a different act than guessing). Routed `patch`, applied directly: added a comment documenting the verification-only scope so a future reader doesn't misread this as license to re-derive-and-use elsewhere, or mistake it for a pattern to repeat.
- **`state_io.py cmd_write`'s `--body-file` reading was unguarded, and the documented mutual exclusivity with `--body` wasn't enforced** — verdict: `medium`. Verified: `Path(args.body_file).read_text(...)` ran outside the `try/except`, so a missing/unreadable path raised a raw traceback instead of the CLI's normal `error: ...` + exit 2 pattern (inconsistent with `cmd_read`'s own handling); passing both `--body` and `--body-file` silently dropped `--body` with no error, contradicting the docstring's claimed contract. No test exercised `--body-file` at all. Routed `patch`, applied directly: moved the read inside the `try` (now catching `OSError` too) and added an explicit mutual-exclusivity check returning exit 2; added three tests (`--body-file` success, missing path, both-given) — 43/43 pass.

## Design Notes

`state_io.py` only implements what AD-10 actually specifies: the per-stage status enum is defined for `analysis` (governs `plan.md`/`decisions.md`) and `review` (governs `review.md`); `implementation` has no AD-10-defined status enum in v1 (no implementation-stage state file exists yet), so `write_state(stage="implementation", ...)` accepts any non-empty `status` without a closed-enum check — don't invent one; later entries decide if/when an implementation-stage file is needed.

Evidence-file format under `evidence/checks/`/`evidence/review/` is deliberately NOT decided here — entries 8 and 9 own that. This ticket only provides `state_dir`/`ensure_layout` so those directories exist with the right names; it does not prescribe what goes inside them.

Per entry 1's Design Notes, the workflow's `concurrency:` key still can't call this library (GHA evaluates it before any job runs) — unchanged, still keyed on the raw `story_file` input.

`factory/scripts/state_io.py` is governed by the architecture's Stack decision (`Python >=3.13`), not `_bmad/scripts/memlog.py`'s floor — the two live at different altitudes (factory pipeline substrate vs. bmad tooling) even though `state_io.py` mirrors `memlog.py`'s pattern. Don't copy `_bmad/`'s version pins into `factory/` by precedent; check the Stack table instead.

The implementation job's "Assert story-slug/run-id propagation" step is a deliberate, narrow exception to AD-8's "never independently re-derived" rule: it recomputes the expected slug/run-id solely to compare against `needs.analysis.outputs.*` and fail loudly on mismatch, then discards the recomputed value — nothing downstream ever acts on it. This is the only way to prove propagation actually carried the right value end-to-end; it is not license for a future job to re-derive and use its own value for real work. See the inline comment in `.github/workflows/light-factory.yml` and the Review Triage Log entry above.

## Verification

**Commands:**
- `uv run --with pytest pytest factory/scripts/tests/test_state_io.py` -- expected: all tests pass
- `gh workflow run light-factory.yml -f story_file=stories/trivial-test-story.md` then `gh run view <run-id> --log` -- expected: `analysis` logs `story-slug=trivial-test-story run-id=run-<id>`; `implementation`'s assertion step logs a pass and the job succeeds (or is gated per the deferred protection-rule gap, but the assertion step itself still runs and passes once `implementation` executes)

---
title: 'Rename the checks job and its fix loop to Quality Assurance'
type: 'refactor'
ticket: '7'
created: '2026-10-13'
status: 'built'
route: 'oneshot'
route_source: 'auto'
review: 'quick'
review_source: 'pinned'
lenses_ran: ['quick']
review_loop_iteration: 0
context: []
baseline_revision: '9ec75aa1ff655a38c13fa7173a938e045086b5a1'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** The workflow's `checks` and `checks-fix-loop` jobs display as "Checks" and "Checks fix loop" in the GitHub UI, and their evidence-commit labels carry the same names into git history, though the work they do is a quality-assurance gate.

**Approach:** Rename only the two jobs' `name:` fields (`.github/workflows/software-factory.yml` lines 177/351) and their `--label` evidence-commit arguments (lines 317/430) to `"Quality Assurance"` / `"Quality Assurance fix loop"`; update `commit_push_implementation.py`'s docstring/help-text example (lines 20/67/103, which cite `"Checks"`/`"Review"` as example `--label` values -- only the `"Checks"` example changes) and `test_commit_push_implementation.py`'s `label="Checks"` / `"Checks: ..."` assertions (lines 155/159) to match. Leave the `checks`/`checks-fix-loop` YAML job-id keys, their `needs:`/`if:` wiring, the `checks_fix_loop_graph.py` module, the five check types, `run_checks.py`'s subcommand vocabulary, and the `checks-toolchain` composite action's own name (`.github/actions/checks-toolchain/action.yml`) untouched.

</frozen-after-approval>

## Implementation Notes

Oneshot: three files, each a one-to-few-line literal-string rename (job `name:` fields, `--label` arguments, one docstring example, one test's label/assertion) — no restructuring, no new logic.

- 2026-10-13: implemented as specified. `.github/workflows/software-factory.yml`: `checks` job `name:` → `"Quality Assurance"` (L177), its `--label` → `"Quality Assurance"` (L317); `checks-fix-loop` job `name:` → `"Quality Assurance fix loop"` (L351), its `--label` → `"Quality Assurance fix loop"` (L430) -- both `--label` values now need quoting since they contain a space. `commit_push_implementation.py`: updated the `"Checks"`/`"Review"` docstring example (L20, L67) and the `--label` help text (L103) to cite `"Quality Assurance"` instead of `"Checks"`; left the `"Review"` half of each example untouched (out of scope). `test_commit_push_implementation.py`: `label="Checks"` → `label="Quality Assurance"` and the expected commit message `"Checks: foo (run-1)"` → `"Quality Assurance: foo (run-1)"`. Left untouched, per the plan's boundaries: the `checks`/`checks-fix-loop` YAML job-id keys and `needs:`/`if:` wiring, `checks_fix_loop_graph.py`, the five check types, `run_checks.py`, and `.github/actions/checks-toolchain/action.yml`'s own `name: Checks toolchain`. Verified: `uv run --with pytest --with pyyaml pytest factory/scripts/tests/ factory/graph/tests/` -- 390 passed; `uv run --with ruff ruff check factory/` -- no findings; a repo-wide grep for the old job-label strings in the touched files returns nothing.

## Plan Change Log

## Review Triage Log

- **Quick, 2026-10-13** — Implementation Notes said "five files" but only three were touched. Verdict: **low** (planning-doc inaccuracy, not a code defect; fix is a simple correction). Route: **patch** — corrected to "three files".
- **Quick, 2026-10-13** — `commit_push_implementation.py`'s new `--label` help text used single-quote style (`'Quality Assurance'`) inconsistent with the docstring's backtick-double-quote style (`` `"Review"` ``) used two lines above. Verdict: **low** (cosmetic, no behavior effect; fix is a simple correction). Route: **patch** — changed the help string to the matching backtick-double-quote style.

## Verification

**Commands:**
- `uv run --with pytest --with pyyaml pytest factory/scripts/tests/test_commit_push_implementation.py` -- expected: passes
- `uv run --with pytest --with pyyaml pytest factory/scripts/tests/ factory/graph/tests/` -- expected: all pass
- `uv run --with ruff ruff check factory/` -- expected: no findings

**Manual checks (if no CLI):**
- `grep -n 'name: "Checks\|--label Checks' .github/workflows/software-factory.yml` -- expected: `name: "Quality Assurance"`, `name: "Quality Assurance fix loop"`, `--label "Quality Assurance"`, `--label "Quality Assurance fix loop"`
- `grep -n 'name: Checks toolchain' .github/actions/checks-toolchain/action.yml` -- expected: unchanged (out of scope per ticket 7's Boundaries)

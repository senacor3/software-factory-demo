---
id: 7
type: story
title: "The checks job and its fix loop read Quality Assurance, not Checks"
parent: none
covers: []
after: []
assignee: ""
refined: true
hitl: false
risk: low
estimate: ""
---

# The checks job and its fix loop read Quality Assurance, not Checks

## Description

Split off from ticket 6 at planning time (its plan grew too large bundling both renames). The workflow's `checks` and `checks-fix-loop` jobs currently display as "Checks" and "Checks fix loop"; this ticket renames only their display names and the evidence-commit labels that carry the same identity into git history, to "Quality Assurance" and "Quality Assurance fix loop".

## Acceptance Criteria

1. **The checks job and its fix loop read Quality Assurance**
   **Given** the workflow's `checks` and `checks-fix-loop` jobs
   **When** viewed in the GitHub UI, or in the evidence commit each produces
   **Then** both their display names and their evidence commit labels read "Quality Assurance" and "Quality Assurance fix loop"

2. **The jobs' internals and the five check types are unchanged**
   **Given** the same two jobs
   **When** their job-id keys, `needs:`/`if:` wiring, the `checks_fix_loop_graph.py` module, the `.github/actions/checks-toolchain/action.yml` composite action's own name, and the build/test/lint/security/static-analysis check types are inspected
   **Then** none of them changed — only the two jobs' human-facing name and label moved

3. **Tests still prove the renamed behavior**
   **Given** the tests that today assert `label="Checks"` or the resulting `"Checks: ..."` commit message
   **When** they run after this change
   **Then** they assert `"Quality Assurance"` and pass, proving the renamed behavior rather than being weakened

## Boundaries

- Must not change: the `checks`/`checks-fix-loop` YAML job-id keys, their `needs:`/`if:` wiring, the `checks_fix_loop_graph.py` module's internal names, the five check types and `run_checks.py`'s subcommand vocabulary, and the `checks-toolchain` composite action's own display name (`Checks toolchain` — decided to leave as a common-noun description of the shared toolchain setup, not the job's own identity).

## References

- parent — none
- code — .github/workflows/light-factory.yml (or its renamed successor, once ticket 6 lands), the `checks` and `checks-fix-loop` jobs' `name:` fields and `--label` arguments
- code — factory/scripts/commit_push_implementation.py (the `--label` default/help text), factory/scripts/tests/test_commit_push_implementation.py (the `label="Checks"` / `"Checks: ..."` assertions)

## Notes

- Decision: the evidence commit-message labels are renamed to match the new job display names — `--label "Quality Assurance"` / `--label "Quality Assurance fix loop"` (user's choice, 2026-10-13).
- Decision: the `checks-toolchain` composite action's own `name: Checks toolchain` is left unchanged — it describes the shared toolchain setup in common-noun terms, not the job's own proper-noun identity (user's choice, 2026-10-13).
- Sequencing: build this after ticket 6 lands if both are picked up close together, since ticket 6 renames the workflow file itself (`light-factory.yml` → `software-factory.yml`); either order works otherwise, they touch disjoint lines of the same file.

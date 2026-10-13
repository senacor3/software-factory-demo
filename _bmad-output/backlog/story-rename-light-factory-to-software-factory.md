---
id: 6
type: story
title: "The pipeline and its naming read software-factory, with the Checks job renamed to Quality Assurance"
parent: none
covers: []
after: []
assignee: ""
refined: true
hitl: false
risk: medium
estimate: ""
---

# The pipeline and its naming read software-factory, with the Checks job renamed to Quality Assurance

## Description

The pipeline currently names itself, its branches, its bot commits, and its CI jobs after "light-factory", while the project and its GitHub remote are already `senacor3/software-factory-demo`. This ticket renames every place that carries the pipeline's own project identity — the workflow's display name and concurrency group, its three invoked skills, its git branch/commit-author/PR-title formula, its story-path allow-list, and its docs — to "software-factory", and separately renames the "Checks" job and its fix loop to "Quality Assurance" (display name and evidence-commit label only, not their internal wiring). Historical records — the `initiative-light-factory` planning folder, past run evidence, and story files already filed under the old project name — are left as the historical record; only how the pipeline presents and operates itself going forward changes.

## Acceptance Criteria

1. **The pipeline's own identity reads software-factory**
   **Given** the workflow file, its three invoked skills, and the docs that name the pipeline's own project (AGENTS.md, README.md, the demo app's own AGENTS.md/README files, and the BMad project config)
   **When** read today
   **Then** none of them say "light-factory" as the pipeline's identity — all read "software-factory"

2. **A run's branch, authorship, and PR title agree end to end**
   **Given** a story dispatched after this change
   **When** each stage opens its branch, commits evidence, and opens or merges its PR
   **Then** every stage computes and matches the same "software-factory" branch formula and bot identity — no stage still expects "light-factory" while another produces "software-factory"

3. **The story-path allow-list accepts the renamed project**
   **Given** a story filed under the renamed project's story directory
   **When** the pipeline validates its path
   **Then** it is accepted, and the workflow's own dispatch-input description names the renamed project rather than the old one

4. **Historical records are untouched**
   **Given** the existing `initiative-light-factory` planning folder, past runs' evidence folders, and the story files already filed under the old project name
   **When** this rename lands
   **Then** none of their paths or content changed

5. **The Checks job and its fix loop read Quality Assurance**
   **Given** the workflow's checks job and its fix-loop job
   **When** viewed in the GitHub UI, or in the evidence commit each produces
   **Then** both their display names and their evidence commit labels read "Quality Assurance" and "Quality Assurance fix loop"

6. **The checks job's internals and its five check types are unchanged**
   **Given** the same two jobs
   **When** their job-id keys, `needs`/`if` wiring, the fix-loop module, and the build/test/lint/security/static-analysis check types are inspected
   **Then** none of them changed — only the human-facing name and label moved

7. **Tests still prove the renamed behavior**
   **Given** the tests that today assert the old "light-factory" or "Checks" strings
   **When** they run after this change
   **Then** they assert the new strings and pass, proving the renamed behavior rather than being weakened to pass

## Boundaries

- Must not change: the freight-tenders demo app's own name and identity.
- Must not change: the five check types (build, test, lint, security, static_analysis) and `run_checks.py`'s subcommand vocabulary.
- Must not change: the checks and checks-fix-loop jobs' YAML id keys, their `needs:`/`if:` wiring, the `checks_fix_loop_graph.py` module's internal names, and any enum values recorded in the graph's JSON schemas.
- Must not change: content under the `initiative-light-factory` planning folder, any `.factory/<run>/` evidence folder, or the story files already filed under the old project's story directory.

## References

- code — .github/workflows/light-factory.yml (workflow identity, concurrency group, and the two job names/labels)
- code — factory/scripts/state_io.py (the story-project allow-list)
- code — factory/scripts/checkout_branch.py, open_implementation_pr.py, commit_push_implementation.py, merge_story.py, close_rejected_pr.py, post_evidence_summary.py (the repeated branch/bot-identity/PR-title formula)
- code — .claude/skills/light-factory-analysis/, light-factory-implementation/, light-factory-review/ and their invocations in factory/graph/analysis_graph.py, implementation_graph.py, review_graph.py, fix_loop_graph.py
- docs — AGENTS.md, README.md, freight-tenders/README.md, freight-tenders/backend/AGENTS.md, freight-tenders/frontend/AGENTS.md, _bmad/config.toml

## Notes

- Decision: this ticket covers the full functional rename (branch formula, bot identity, commit/PR-title prefixes, story-path allow-list) together with the display-level rename, in one ticket (user's choice, 2026-10-13).
- Decision: historical artifacts — the `initiative-light-factory` folder, `.factory/<run>/` evidence folders, and the story files already filed under the old project name — are left unchanged (user's choice, 2026-10-13).
- Decision: the Checks/Checks-fix-loop rename is display-name and evidence-label only; the jobs' YAML ids, `needs:`/`if:` wiring, and the `checks_fix_loop_graph.py` module stay as-is (user's choice, 2026-10-13).
- Assumption: new stories for this project are filed under the renamed project's story directory going forward; the story-path allow-list drops the old name entirely rather than keeping it as an alias, since the files left at the old path are historical and not expected to be re-dispatched.
- Assumption: the evidence commit-message labels passed for the checks job and its fix loop (currently `Checks` / `Checks-fix-loop`) are renamed to match the new display names, since they carry the same human-facing identity into git history.
- A separate open backlog bug (`bug-checks-fix-loop-recheck-fails-without-frontend-dependencies.md`) cites the old branch prefix and "Checks fix loop" name in its own historical evidence; that ticket describes a specific past run and is not touched by this one.
- Suggested check beyond this ticket's own criteria: merge when no pipeline run is in-flight (an in-flight run's branch was opened under the old formula), and dispatch one real trivial story end to end afterward to confirm no residual "light-factory"/"Checks" string surfaces in the branch, commit author, PR title, or job names.

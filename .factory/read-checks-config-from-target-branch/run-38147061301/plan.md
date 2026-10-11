---
schema_version: 1
story_slug: read-checks-config-from-target-branch
stage: analysis
status: ready-for-review
updated: 2026-10-11T14:25:24Z
---

## Proposal

Make run_checks.py read the checks config from origin/main instead of the story branch's working tree, so a story cannot weaken its own checks. In factory/scripts/run_checks.py, add `TARGET_BRANCH = "main"` and `_read_target_config(cwd) -> str | None`. The function runs `git show origin/<TARGET_BRANCH>:.github/post-implementation-checks.yml` through subprocess.run in `cwd` and returns stdout on success. It returns None on a non-zero exit or an OSError, which covers a missing ref, a non-git directory and a missing git binary. `load_commands` calls it first and falls back to the existing working-tree read only when it returns None. The existing error handling stays as it is: a missing or malformed config still raises ChecksConfigError.

The config source has to reach the evidence file, so `load_commands` must report it without changing its public return type (existing tests compare the returned list, e.g. test_run_checks.py:267). The cleanest way is an internal helper, for example `_load_config(name, cwd) -> tuple[list[list[str]], str | None]`, that returns the commands and the source. `load_commands` stays a thin wrapper that returns only the commands, and `run_check` calls the helper directly. `run_check` then sets `config_source` on every result: "origin/main", "working-tree", or None when the config could not be read at all (the missing-config and unreadable-file failures). The source has to be known even when parsing fails, so the helper should attach it to ChecksConfigError, or resolve the source before parsing. The signatures of run_build, run_test, run_lint, run_security and the CLI are unchanged, and the `skipped` rule is untouched.

In post_evidence_summary.py, `_render_summary` adds one line under the Checks list: `- config: <source>`. The source is the shared `config_source` value when all four evidence files agree on one non-null value. It is `unknown` when they disagree, when the key is missing from any file (including the "not-run" placeholder), or when the value is null.

Docs: update the run_checks.py module docstring, and the header comment of .github/post-implementation-checks.yml to say a change applies to runs started after it is merged. Extend AD-6's addendum in architecture-light-factory.md with one sentence on where the config is read from and why, and update the file-tree line at ~line 273. Do not touch .github/workflows/light-factory.yml; the pipeline token can't push changes there.

Risk: the checks job uses plain `actions/checkout`, so `origin/main` should exist as a remote-tracking ref. If it ever doesn't, the fallback silently reads the story branch's own config. The `config_source: working-tree` line in the evidence summary is the only signal of that. This matches the story's stated fallback, so I'd implement it as specified.

## Subtasks

- In run_checks.py add `TARGET_BRANCH = "main"` and `_read_target_config(cwd) -> str | None` (git show origin/<TARGET_BRANCH>:<CONFIG_RELPATH>, as a posix path, via subprocess.run with cwd, capture_output and text; return None on non-zero exit or OSError).
- Refactor config loading: add an internal helper returning (commands, source) with source in {'origin/main', 'working-tree', None}. Try _read_target_config first and fall back to the working-tree file on None. Keep all ChecksConfigError cases, and make the source available on the error path too. Keep `load_commands(name, *, cwd)` returning just the list of commands.
- In run_check, add `config_source` to the result dict in all three branches (config error, skipped, ran), so it lands in every evidence JSON. Leave the run_* wrappers and CLI as they are.
- In post_evidence_summary.py, compute the config source from the four check dicts and add `- config: <source>` after the check status lines in _render_summary. Use 'unknown' for disagreement, a missing key, or a null value.
- Update the run_checks.py module docstring, the header comment of .github/post-implementation-checks.yml, and AD-6's addendum plus the file-tree line in architecture-light-factory.md.
- Add an autouse or explicit fixture in test_run_checks.py that patches run_checks._read_target_config to return None. Apply it to the existing tests, including the REPO_ROOT test that loads the real config.
- Add the new tests in test_run_checks.py and test_post_evidence_summary.py (see the tests list), then run the full factory test suite and the repo's lint command (ruff).

## Tests

- test_run_checks.py: with _read_target_config patched to return YAML text that differs from the temporary working-tree config, the target text's commands run and the working-tree file is ignored; evidence config_source == 'origin/main'.
- test_run_checks.py: with _read_target_config returning None, the working-tree file is used and evidence config_source == 'working-tree'.
- test_run_checks.py: with no working-tree config and _read_target_config returning None, the result is status 'fail' and evidence config_source is null.
- test_run_checks.py: a target config that disables `test` (empty list) yields 'skipped' and config_source 'origin/main'. This shows the weakened working-tree file no longer applies.
- test_run_checks.py: _read_target_config returns None when subprocess.run returns a non-zero exit, and when it raises OSError. It returns stdout when the exit is 0 and invokes `git show origin/main:.github/post-implementation-checks.yml` with the given cwd.
- test_run_checks.py: malformed YAML from the target branch still produces a ChecksConfigError-based fail result.
- test_run_checks.py: the existing tests keep passing with the new fixture, including the REPO_ROOT load_commands test.
- test_post_evidence_summary.py: all four evidence files with config_source 'origin/main' render '- config: origin/main' under Checks.
- test_post_evidence_summary.py: evidence files with different config_source values render '- config: unknown'.
- test_post_evidence_summary.py: a missing config_source key, a null value, or a not-run check renders '- config: unknown'.

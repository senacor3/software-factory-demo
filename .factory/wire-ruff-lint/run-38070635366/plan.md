---
schema_version: 1
story_slug: wire-ruff-lint
stage: analysis
status: ready-for-review
updated: 2026-10-10T17:11:33Z
---

## Proposal

Replace the placeholder body of run_lint in factory/scripts/run_checks.py with a real check that delegates to the existing _run_command_check, with the same signature and keyword args as run_build/run_test. The command is ["uv","run","--with","ruff","ruff","check","factory/"] and the evidence name is "lint". Evidence shape, pass/fail mapping (exit 0 is pass, otherwise fail with output in detail) and OSError handling all come from _run_command_check, so no subprocess logic is duplicated. run_security and PLACEHOLDER_DETAIL stay unchanged because security still uses the constant. No pyproject.toml or ruff.toml is added, so ruff runs on its defaults.

Docs and wiring get small updates. The module docstring should say lint is now real, list its command, and say the exit-1 rule now covers lint. The comment above the CI check steps and the step name "Lint check (placeholder)" in .github/workflows/light-factory.yml (around lines 154-175) need updating, since lint can now fail the job. The lint part of the deferred entry in _bmad-output/initiative-light-factory/deferred-work.md should be marked resolved, with security left deferred.

Two existing lint-specific tests must change. test_run_lint_is_always_skipped_and_runs_no_command asserts the old placeholder behavior. test_cli_exits_zero_on_skipped uses the lint subcommand and would now launch real ruff. The story's "unmodified" constraint covers build/test/security, so replacing these lint-specific tests is consistent with it. Switch the CLI skipped test to the security subcommand, and add lint pass and fail tests that mock subprocess.run like the build/test tests and assert on the written evidence/checks/lint.json.

Finally, run ruff against factory/ and fix any default-rule findings so the check starts from a clean baseline.

## Subtasks

- Rewrite run_lint in factory/scripts/run_checks.py to build the ruff command list and return _run_command_check('lint', cmd, story_slug, run_id, state_base=state_base, cwd=cwd)
- Update the run_checks.py module docstring (Commands list, 'real vs placeholder' paragraph, exit-code note) and the run_lint docstring; keep PLACEHOLDER_DETAIL for run_security
- Run `uv run --with ruff ruff check factory/` and fix any findings in factory/ (without adding a ruff config unless concretely needed)
- In factory/scripts/tests/test_run_checks.py, replace the lint placeholder test with lint pass and fail tests mocking run_checks.subprocess.run and asserting on evidence/checks/lint.json; also add a test for a missing ruff/uv (OSError) if the build/test tests have an equivalent
- Change test_cli_exits_zero_on_skipped to use the security subcommand, and add CLI exit-code tests for lint pass (0) and fail (1) with subprocess.run mocked
- Update the test module docstring to describe lint as real
- Update .github/workflows/light-factory.yml: rename the 'Lint check (placeholder)' step and fix the comment about lint always being skipped
- Mark the lint portion of the deferred-work.md entry as resolved, leaving security deferred

## Tests

- run_lint with mocked subprocess.run returning 0: result status 'pass', command equals the ruff list, empty detail, lint.json evidence written
- run_lint with mocked subprocess.run returning 1 and ruff output on stdout: status 'fail', detail contains the output, lint.json evidence written
- run_lint when subprocess.run raises OSError: status 'fail', returncode None, evidence written
- CLI `lint` exits 0 on a mocked pass and 1 on a mocked fail, with evidence written before the exit decision
- CLI `security` still exits 0 with status skipped and runs no command
- Existing build/test/security tests pass unmodified
- Manual/CI check: `uv run --with ruff ruff check factory/` exits 0 on the final tree

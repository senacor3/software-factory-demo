---
schema_version: 1
story_slug: wire-ruff-lint
stage: analysis
status: ready-for-review
updated: 2026-10-10T17:32:33Z
---

## Proposal

Replace the placeholder body of run_lint in factory/scripts/run_checks.py with a real check. It builds the command ["uv", "run", "--with", "ruff", "ruff", "check", "factory/"] and delegates to _run_command_check("lint", ...), exactly like run_test. That reuses the existing subprocess, pass/fail and evidence-writing logic: exit 0 maps to "pass", any other exit to "fail", with the output in detail. run_security stays untouched. No pyproject.toml or ruff.toml is added. Update the module docstring, the Commands list, the run_lint docstring and the PLACEHOLDER_DETAIL text so they say lint is real and only security remains a placeholder. Do not touch .github/workflows/light-factory.yml; its "Lint check (placeholder)" step name stays. Two existing tests encode the old lint behavior and must change. test_run_lint_is_always_skipped_and_runs_no_command is replaced by real pass/fail tests. test_cli_exits_zero_on_skipped calls the lint subcommand, so it should be repointed at security; otherwise it would shell out to real uv/ruff. The build, test and security tests stay unmodified. Finally, run ruff on factory/ and fix any real findings so the check starts from a clean baseline. I could not run ruff in this read-only analysis, so the size of that cleanup is unknown. Prefer minimal fixes.

## Subtasks

- In run_checks.py, rewrite run_lint to build cmd = ['uv','run','--with','ruff','ruff','check','factory/'] and return _run_command_check('lint', cmd, story_slug, run_id, state_base=state_base, cwd=cwd).
- Update the module docstring (lint is now real; security is the only placeholder), the Commands list (lint: uv run --with ruff ruff check factory/), the run_lint docstring, and PLACEHOLDER_DETAIL so it refers to security only. Keep run_security's behavior unchanged.
- In test_run_checks.py, replace the lint always-skipped test with new tests: pass (mock subprocess.run returncode 0), fail (non-zero with stdout/stderr captured in detail), tool-missing (OSError), and a command-shape assertion. Update the file docstring accordingly.
- Repoint test_cli_exits_zero_on_skipped to the security subcommand, and add a CLI test that lint exits 1 on a mocked failure and 0 on a mocked pass.
- Run `uv run --with ruff ruff check factory/` and fix any findings in the factory/ tree with minimal changes (no config file unless concretely needed).
- Run the full suite (uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/) to confirm everything passes.

## Tests

- run_lint with subprocess.run mocked to return 0: result status 'pass', command equals the uv/ruff list, evidence file lint.json has status 'pass'.
- run_lint with mocked non-zero return and ruff output on stdout/stderr: status 'fail', detail contains the output, evidence file written with status 'fail'.
- run_lint with subprocess.run raising OSError: status 'fail', detail mentions the error, evidence written.
- CLI: main(['lint', ...]) returns 1 on mocked failure and 0 on mocked pass; main(['security', ...]) still returns 0 with skipped status.
- Existing build/test/security tests pass unmodified.
- Manual/CI check: `uv run --with ruff ruff check factory/` exits 0 on the final tree.

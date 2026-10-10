---
schema_version: 1
story_slug: wire-ruff-lint
stage: analysis
status: ready-for-review
updated: 2026-10-10T18:35:03Z
---

## Proposal

Change `run_lint` in factory/scripts/run_checks.py to delegate to the existing `_run_command_check`, the same way `run_build` and `run_test` do. It will use the command `["uv", "run", "--with", "ruff", "ruff", "check", "factory/"]` and the name "lint". That gives `pass` on exit 0, `fail` otherwise, with captured stdout and stderr in `detail`, and evidence written to `evidence/checks/lint.json`. The OSError fallback also comes for free. The `run_security` function stays as it is. `PLACEHOLDER_DETAIL` is still used by security, so I'll reword it to mention security only. The module docstring (build/test/lint real, only security a placeholder) and the Commands list will be updated. The lint line will show the real command, and the "exits 1 only when fail (build/test)" sentence will say build/test/lint. `.github/workflows/light-factory.yml` is not touched.

The repo already has a `ruff.toml` at the root. It only ignores SIM117 and was added to establish the clean baseline (see the last commit), so no new config is needed. The implementer should still run `uv run --with ruff ruff check factory/` to confirm it exits 0, and fix any findings it reports. I expect none.

Test changes in factory/scripts/tests/test_run_checks.py:
- The existing `test_run_lint_is_always_skipped_and_runs_no_command` asserts the old placeholder behavior and contradicts the story, so it must be replaced with real pass and fail tests. This is a necessary change to a lint-specific test, not to the build/test/security tests.
- `test_cli_exits_zero_on_skipped` calls the `lint` subcommand without mocking, so it would now shell out to real uv/ruff. Switch it to the `security` subcommand, which is still skipped.
- Update the file's docstring and section header to match.

## Subtasks

- In run_checks.py, replace the body of run_lint with a call to _run_command_check("lint", ["uv","run","--with","ruff","ruff","check","factory/"], story_slug, run_id, state_base=state_base, cwd=cwd); drop the placeholder docstring in favor of a short real one.
- Update the module docstring: say lint is now real, only security remains a placeholder, update the Commands list (lint -> uv run --with ruff ruff check factory/) and the exit-code sentence. Reword PLACEHOLDER_DETAIL to refer to security only; leave run_security's behavior unchanged.
- Run `uv run --with ruff ruff check factory/` against the tree (existing ruff.toml applies); fix any findings so the check starts clean. Don't edit .github/workflows/.
- In test_run_checks.py, replace the lint always-skipped test with: test_run_lint_pass_writes_pass_evidence (asserts exact command list, status pass, evidence file) and test_run_lint_fail_captures_ruff_output_and_writes_evidence (nonzero returncode with ruff findings on stdout, asserts status fail, detail contains the findings, evidence file has fail). Optionally add an OSError case for lint.
- Change test_cli_exits_zero_on_skipped to use the `security` subcommand; add a CLI test that `lint` exits 1 on a mocked failing ruff run and 0 on a mocked pass.
- Update the test file docstring and section headers to reflect that only security is an always-skipped placeholder.
- Run the full suite (uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/) and ruff to confirm everything passes.

## Tests

- New: run_lint with mocked subprocess.run returning returncode 0 -> status "pass", the command is exactly [uv, run, --with, ruff, ruff, check, factory/], and lint.json is written with status pass.
- New: run_lint with mocked failing subprocess (returncode 1, ruff findings on stdout, uv noise on stderr) -> status "fail", detail contains the findings, lint.json written with status fail.
- New (optional): run_lint with subprocess.run raising OSError -> status fail, no exception raised, evidence written.
- New: CLI `lint` returns exit code 1 when the mocked ruff run fails, and 0 when it passes.
- Modified: test_cli_exits_zero_on_skipped now exercises `security`, which still returns 0 with status skipped.
- Unchanged and must pass: all existing run_build, run_test and run_security tests.
- Manual or CI check: `uv run --with ruff ruff check factory/` exits 0 on the final tree.

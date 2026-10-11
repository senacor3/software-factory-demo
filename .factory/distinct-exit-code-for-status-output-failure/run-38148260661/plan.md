---
schema_version: 1
story_slug: distinct-exit-code-for-status-output-failure
stage: analysis
status: ready-for-review
updated: 2026-10-11T14:42:56Z
---

## Proposal

Add a new exception, `AnalysisStatusOutputError`, in `factory/graph/analysis_graph.py`, and wrap the file open and write inside `_write_status_output` in `try/except OSError`. On failure it raises the new exception, chained from the original error. The message names the `GITHUB_OUTPUT` path and the original error. The unset-`GITHUB_OUTPUT` early return and the success path stay as they are.

In `main`, the `_write_status_output(outcome["status"])` call moves into its own `try` block. The handler `except AnalysisStatusOutputError` prints `status output write failed: <message>` to stderr and returns 5. The call stays before the `print(json.dumps({"ok": True, ...}))` line, so a failed write leaves stdout empty and the success line appears only after a fully successful run. Exit codes 0, 1, 3 and 4 are unchanged. Because the job still exits non-zero, the `implementation` job and the `plan-approval` gate stay closed. The workflow file is not touched.

Docs:
- Extend the module docstring with a further case: the status-output write failing after plan.md, decisions.md and the PR already exist. State the exit code for each failure case: halted = 1, invocation = 3, PR-open = 4 (including the round-count query failure), status-output = 5.
- Add one sentence to AD-13 in the architecture doc, right after the sentence ending "(added by `epic-pipeline-hardening` ticket 2, 2026-10-11)". It says that a failure to write the status output fails the `analysis` job with its own exit code (5), so the gate stays closed.

Closing the leftover `ready-for-review` PR is out of scope.

## Subtasks

- In analysis_graph.py, define `class AnalysisStatusOutputError(RuntimeError)` with a docstring, next to the other exception types.
- In `_write_status_output`, wrap the `open(..., 'a')` and `write` in `try/except OSError as e` and raise `AnalysisStatusOutputError(f"could not write status to {output_path}: {e}") from e`. Keep the unset-env early return unchanged, and update the docstring to mention the new exception.
- In `main`, wrap the `_write_status_output(outcome["status"])` call in `try/except AnalysisStatusOutputError as e`. The handler prints `status output write failed: {e}` to stderr and returns 5. Keep the success `print(json.dumps(...))` after the call so stdout stays empty on failure.
- Update the module docstring: add the status-output failure as a further case (after the sixth) and list the exit code per failure case: 1 halted, 3 invocation, 4 PR-open/round-count, 5 status-output write.
- In architecture-light-factory.md AD-13, add one sentence after the sentence explaining that the run ends without a gate, saying that a failure to write the status output fails the `analysis` job with its own exit code (5), so the gate stays closed.
- Add the tests in factory/graph/tests/test_analysis_graph.py (see tests), then run the full file to confirm the existing tests still pass.

## Tests

- test_cli_main_status_output_write_failure_exits_5: set GITHUB_OUTPUT to a directory (`tmp_path`) and patch `analysis_graph.run_analysis` to return `{"status": "ready-for-review"}`. Assert main returns 5, captured.err contains 'status output write failed' and the directory path, and captured.out == ''.
- test_write_status_output_raises_analysis_status_output_error: set GITHUB_OUTPUT to a directory and call `_write_status_output('ready-for-review')` under `pytest.raises(AnalysisStatusOutputError)`. Assert the message contains the path, and that `__cause__` is an OSError.
- Optionally, a nonexistent parent directory as a second failure case, parametrized, for the same exit-5 assertions.
- Existing tests pass unchanged. These include test_cli_main_appends_status_to_github_output, test_cli_main_without_github_output_writes_no_file and test_cli_main_failure_writes_no_status_output, which cover the exit codes 0, 1, 3 and 4 and the unset-env behavior.

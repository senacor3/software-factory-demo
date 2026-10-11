# Give a failed status-output write its own exit code

## Problem

`factory/graph/analysis_graph.py`'s `main` ends a successful analysis by calling
`_write_status_output`, which appends `status=<status>` to the file `GITHUB_OUTPUT`
names. The workflow's `implementation` job reads that output to decide whether the
`plan-approval` gate opens.

If that write fails (the file cannot be opened or written), the `OSError` is not
caught: Python prints a traceback and exits with code 1. Code 1 is already this
script's code for "analysis halted: the story is incomplete or out of scope, no
state file written". At this point the opposite is true — `plan.md` and
`decisions.md` are written and the PR is open — so the exit code misreports what
happened.

## What to build

- Add an exception type `AnalysisStatusOutputError` in `analysis_graph.py`.
  `_write_status_output` raises it when opening or writing the output file fails
  with an `OSError`, with a message that names the file path and the original
  error.
- `main` catches it, prints `status output write failed: <message>` to stderr, and
  returns exit code **5**. It prints nothing to stdout in that case — the
  `{"ok": true, ...}` line is only for a run that fully succeeded.
- Exit codes 0, 1, 3 and 4 keep their meaning, and nothing changes when
  `GITHUB_OUTPUT` is unset or the write succeeds.
- The job still fails on this error, so no gate opens — that is intended and must
  stay so.

## Tests

In `factory/graph/tests/test_analysis_graph.py`, in the style already used there:

- a write failure (point `GITHUB_OUTPUT` at a path that cannot be opened, such as a
  directory) makes `main` return 5, print the stderr message with the path in it,
  and print nothing to stdout;
- `_write_status_output` raises `AnalysisStatusOutputError` for that case;
- the existing tests must keep passing unchanged.

## Documents to update

- The module docstring of `analysis_graph.py` describes the outcomes case by case
  ("A fourth case", "A fifth case", "A sixth"). Add this failure as a further case,
  and say which exit code each of the failure cases maps to — the docstring does
  not list the exit codes today.
- `_bmad-output/initiative-light-factory/architecture-light-factory/architecture-light-factory.md`,
  AD-13: after the sentence that explains how a halted run ends without a gate, add
  one sentence saying that a failure to write the status output fails the
  `analysis` job with its own exit code, so the gate stays closed.
- Do not edit `.github/workflows/light-factory.yml` — a commit touching that
  directory cannot be pushed by the pipeline's token.

## Out of scope

A run that fails this way leaves its `ready-for-review` PR open. Closing it is not
part of this story.

## Why

Found in the review of ticket 3.2 of `epic-pipeline-hardening` (2026-10-11) and not
fixed there: unlikely on a runner, but the script's exit codes are otherwise
distinct per failure, and this one breaks that.

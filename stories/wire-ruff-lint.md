# Wire real ruff lint tooling into the mechanical checks

## Problem

`factory/scripts/run_checks.py`'s `run_lint` is currently a permanent placeholder:
it never runs a command and always records `status: "skipped"`. The `build` and
`test` checks are real (they shell out to `compileall`/`pytest` and report a
genuine pass/fail), but `lint` provides no actual signal.

## What to build

Replace `run_lint`'s placeholder body with a real check that runs `ruff check`
against the `factory/` directory, mirroring how `run_build`/`run_test` already
work:

- Run `ruff` via `uv run --with ruff ruff check factory/` (no new config file is
  required — ruff has sensible defaults; don't add a `pyproject.toml` or
  `ruff.toml` unless you find a concrete reason one is needed).
- Report `status: "pass"` when `ruff` exits 0, `status: "fail"` otherwise, with
  the command's output captured in `detail` — the exact same shape
  `_run_command_check` already produces for `build`/`test`. Reuse
  `_run_command_check` rather than duplicating its subprocess/evidence-writing
  logic.
- `run_security` stays exactly as it is today (an honest placeholder) — this
  story is lint only, not security tooling.
- Existing tests for `run_build`/`run_test`/`run_security` must keep passing
  unmodified. Add new tests for `run_lint`'s real pass/fail behavior, mirroring
  the existing `test_run_checks.py` patterns (mock `subprocess.run`, assert on
  the written evidence file).
- If running real `ruff` against the current `factory/` tree surfaces actual
  lint findings, fix them as part of this change so the check starts from a
  clean baseline — don't ship a lint check that fails on its own first run.
- **Do not edit `.github/workflows/light-factory.yml`.** It's fine (and
  expected) for the workflow step there to keep saying "Lint check
  (placeholder)" even after this change — update the Python module's own
  comments/docstring instead. The implementation agent's commit can't push a
  change to any file under `.github/workflows/` (GitHub rejects it
  regardless of token permissions), so a plan that touches it will fail to
  push, no matter how small the edit.

## Why

`factory/scripts/run_checks.py`'s own module docstring and `deferred-work.md`
already call this out as deferred, v1-placeholder behavior with a clear
unblock path. This closes that gap.

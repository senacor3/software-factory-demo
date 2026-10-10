#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""run_checks -- CAP-5's deterministic mechanical-checks script (AD-6).

Four checks, one function each, every one a plain subprocess call from this single
script -- never a LangGraph node or agent tool call (AD-6). Wired into Job 2's
workflow as 4 direct steps, each invoking one subcommand here right after "Run
implementation".

`build` (`python -m compileall factory -q` -- this repo has no packaging/build step,
so syntax/import sanity is the closest real equivalent) and `test` (the existing
pytest suite) and `lint` (`ruff check factory/` with ruff's default rules) are real
checks that can genuinely pass or fail. `security` has no tool configured in this
repo yet (no bandit config) -- user's call, 2026-10-02: it ships as an honest
placeholder (`status: "skipped"`, never `"pass"`) rather than wiring real tooling
now; see deferred-work.md.

Evidence is written to `evidence/checks/<name>.json` via `state_io.write_atomic`
*before* `main()` inspects the result's status to decide the exit code -- a failing
check always leaves a record, never just a non-zero exit with nothing on disk.

Commands (each `--story-slug S --run-id R`):
  build     python -m compileall factory -q
  test      uv run --with pytest pytest factory/graph/tests/ factory/scripts/tests/
  lint      uv run --with ruff ruff check factory/
  security  placeholder, always status: skipped

Exits 1 only when the written result's status is `"fail"` (build/test/lint); 0 for
`"pass"` or `"skipped"`.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import state_io  # noqa: E402

CHECK_NAMES = ("build", "test", "lint", "security")

PLACEHOLDER_DETAIL = "no security tool wired for v1 -- see deferred-work.md"


def _write_evidence(
    name: str,
    story_slug: str,
    run_id: str,
    result: dict,
    *,
    state_base: "str | os.PathLike" = state_io.FACTORY_DIR,
) -> Path:
    path = (
        state_io.state_dir(story_slug, run_id, base=state_base)
        / "evidence"
        / "checks"
        / f"{name}.json"
    )
    state_io.write_atomic(path, json.dumps(result, indent=2) + "\n")
    return path


def _run_command_check(
    name: str,
    cmd: "list[str]",
    story_slug: str,
    run_id: str,
    *,
    state_base: "str | os.PathLike" = state_io.FACTORY_DIR,
    cwd: "str | os.PathLike | None" = None,
) -> dict:
    """Run `cmd`, write its evidence, and return the result dict.

    A non-zero exit is a legitimate `status: "fail"` result, not a script error --
    this never raises for that. Only an OSError (e.g. the command isn't on PATH) is
    caught and folded into the same fail shape, so a missing tool is reported the
    same way a real failure is, not conflated with an uncaught crash.
    """
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        result = {
            "status": "fail",
            "command": cmd,
            "returncode": None,
            "detail": f"failed to run {cmd!r}: {e}",
        }
    else:
        status = "pass" if proc.returncode == 0 else "fail"
        detail = "" if status == "pass" else (proc.stderr.strip() or proc.stdout.strip())
        result = {"status": status, "command": cmd, "returncode": proc.returncode, "detail": detail}

    _write_evidence(name, story_slug, run_id, result, state_base=state_base)
    return result


def run_build(
    story_slug: str,
    run_id: str,
    *,
    state_base: "str | os.PathLike" = state_io.FACTORY_DIR,
    cwd: "str | os.PathLike | None" = None,
) -> dict:
    cmd = [sys.executable, "-m", "compileall", "factory", "-q"]
    return _run_command_check("build", cmd, story_slug, run_id, state_base=state_base, cwd=cwd)


def run_test(
    story_slug: str,
    run_id: str,
    *,
    state_base: "str | os.PathLike" = state_io.FACTORY_DIR,
    cwd: "str | os.PathLike | None" = None,
) -> dict:
    cmd = [
        "uv",
        "run",
        "--with",
        "pytest",
        "pytest",
        "factory/graph/tests/",
        "factory/scripts/tests/",
    ]
    return _run_command_check("test", cmd, story_slug, run_id, state_base=state_base, cwd=cwd)


def run_lint(
    story_slug: str,
    run_id: str,
    *,
    state_base: "str | os.PathLike" = state_io.FACTORY_DIR,
    cwd: "str | os.PathLike | None" = None,
) -> dict:
    """Real check: `ruff check factory/` via uv. Exit 0 is `"pass"`, anything else `"fail"`."""
    cmd = ["uv", "run", "--with", "ruff", "ruff", "check", "factory/"]
    return _run_command_check("lint", cmd, story_slug, run_id, state_base=state_base, cwd=cwd)


def run_security(
    story_slug: str,
    run_id: str,
    *,
    state_base: "str | os.PathLike" = state_io.FACTORY_DIR,
    cwd: "str | os.PathLike | None" = None,
) -> dict:
    """Always a placeholder -- never runs a command, never reports `"pass"` (see
    module docstring and deferred-work.md)."""
    result = {"status": "skipped", "command": None, "detail": PLACEHOLDER_DETAIL}
    _write_evidence("security", story_slug, run_id, result, state_base=state_base)
    return result


_RUNNERS = {"build": run_build, "test": run_test, "lint": run_lint, "security": run_security}


# --- CLI ---------------------------------------------------------------------


def _add_check_subparser(sub, name: str):
    pc = sub.add_parser(name, help=f"run the {name} check")
    pc.add_argument("--story-slug", required=True)
    pc.add_argument("--run-id", required=True)
    pc.set_defaults(check=name)
    return pc


def main(argv: "list[str] | None" = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in CHECK_NAMES:
        _add_check_subparser(sub, name)

    args = p.parse_args(argv)

    result = _RUNNERS[args.check](args.story_slug, args.run_id)
    print(json.dumps(result))
    return 1 if result["status"] == "fail" else 0


if __name__ == "__main__":
    sys.exit(main())

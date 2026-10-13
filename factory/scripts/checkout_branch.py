#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""checkout_branch -- the implementation/checks/review jobs' deterministic
branch-checkout step.

Checks out the exact branch the `analysis` job's `open_implementation_pr.py` already
opened (AD-12) -- never creates one. Branch name formula matches AD-8/AD-12/AD-15
exactly: `software-factory/<story-slug>/<run-id>`.

Defensive, not expected to fail in the normal path (the analysis stage already opened
the branch before the implementation job ever runs) -- but raises a distinct
`CheckoutError` if it does, so a missing/unreachable branch is never silently conflated with a `claude`
CLI tooling failure or a commit/push failure (see story-implementation-agent-plan.md's
I/O & Edge-Case Matrix).

`_run` is a standalone helper, deliberately duplicated from `open_implementation_pr.py`'s
rather than imported -- established convention in this codebase (each deterministic
script owns its own subprocess-wrapping, per its own exception type).

Also a thin CLI (`--story-slug`/`--run-id`): the `checks`/`review` jobs run on fresh
runners and have no in-process call into `checkout_branch()` the way
`implementation_graph.py` does, so they invoke this module directly as a workflow
step instead.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys


class CheckoutError(RuntimeError):
    """A `git` subprocess call failed while checking out the implementation branch."""


def _run(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise CheckoutError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise CheckoutError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout.strip()


def checkout_branch(
    story_slug: str,
    run_id: str,
    *,
    cwd: str | os.PathLike | None = None,
) -> str:
    """Fetch and check out the branch the analysis stage already opened. Never creates a branch.

    Returns the branch name. Raises CheckoutError on any git failure.
    """
    branch = f"software-factory/{story_slug}/{run_id}"
    _run(["git", "fetch", "origin", branch], cwd=cwd)
    _run(["git", "checkout", branch], cwd=cwd)
    return branch


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    args = p.parse_args(argv)

    try:
        branch = checkout_branch(args.story_slug, args.run_id)
    except CheckoutError as e:
        print(f"branch checkout failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "branch": branch}))
    return 0


if __name__ == "__main__":
    sys.exit(main())

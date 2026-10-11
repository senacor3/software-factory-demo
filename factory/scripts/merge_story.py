#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# ///
"""merge_story -- the merge job's merge step (CAP-9, AD-14): a deterministic pipeline script,
never an agent action.

Triggered automatically once the `evidence-approval` gate is approved. Finds the PR via
`open_implementation_pr.find_open_pr` (same branch-name formula every other stage uses:
`light-factory/<story-slug>/<run-id>`) and runs `gh pr merge --squash --delete-branch`
(user's call, 2026-10-02).

Merge-conflict auto-resolution is explicitly out of scope (the spec's own open
question) -- any `gh` failure, including a conflict, just raises `MergeError` and fails
the step; the human resolves out-of-band and re-triggers, consistent with every other
terminal-failure path in this pipeline. No open PR for this branch is treated the same
way -- `MergeError`, since both mean "could not complete the merge".
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import open_implementation_pr


class MergeError(RuntimeError):
    """The merge could not be completed -- no open PR was found for this story/run, or
    the `gh pr merge` subprocess call itself failed (conflict or other `gh` failure)."""


def _run(cmd: list[str], *, cwd: str | os.PathLike | None = None) -> str:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    except OSError as e:
        raise MergeError(f"failed to run {cmd!r}: {e}") from e

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise MergeError(f"{cmd!r} exited {proc.returncode}: {detail}")

    return proc.stdout.strip()


def merge_story(
    story_slug: str,
    run_id: str,
    *,
    cwd: str | os.PathLike | None = None,
) -> dict:
    """Find the PR and squash-merge it with branch deletion. Returns `{"pr": dict}`.
    Raises MergeError if no open PR is found or the merge itself fails (conflict or
    other `gh` failure)."""
    branch = f"light-factory/{story_slug}/{run_id}"

    try:
        pr = open_implementation_pr.find_open_pr(branch, cwd=cwd)
    except open_implementation_pr.PROpenError as e:
        raise MergeError(str(e)) from e
    if pr is None:
        raise MergeError(f"no open PR found for branch {branch!r}")

    _run(["gh", "pr", "merge", str(pr["pr_number"]), "--squash", "--delete-branch"], cwd=cwd)

    return {"pr": pr}


# --- CLI ---------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--story-slug", required=True)
    p.add_argument("--run-id", required=True)
    args = p.parse_args(argv)

    try:
        outcome = merge_story(args.story_slug, args.run_id)
    except MergeError as e:
        print(f"merge failed: {e}", file=sys.stderr)
        return 1

    print(json.dumps({"ok": True, "pr_number": outcome["pr"]["pr_number"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
